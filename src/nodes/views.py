from django.http import HttpResponseNotAllowed
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from nodes.services import LLMService, ChatGraphService

from .models import Chat, Node, NodeType
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model

from asgiref.sync import sync_to_async

def create_chat(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    user = request.user
    print(user)
    if not user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    chat = Chat.create_chat(owner=user)

    if not request.POST.get('system_message'):
        system_message = "You are a helpful assistant. Answer the user's questions as best as you can."
    else:
        system_message = request.POST.get('system_message')

    parent_node = Node.create_node(content=system_message, node_type=NodeType.SYSTEM)

    chat.set_parent_node(parent_node)

    return JsonResponse({'status': 'Chat created successfully', 'chat_id': chat.id})

def change_chat_title(request, chat_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    try:
        chat = Chat.objects.get(id=chat_id, owner=user)
    except Chat.DoesNotExist:
        return JsonResponse({'error': 'Chat not found'}, status=404)

    new_title = request.POST.get('title')
    if new_title:
        chat.title = new_title
        chat.save()
        return JsonResponse({'status': 'Chat title updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid title'}, status=400)
    
def get_user_chats(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    chats = Chat.objects.filter(owner=user).values('id', 'title', 'created_at', 'updated_at')
    return JsonResponse({'chats': list(chats)})
    
def get_chat_details(request, chat_id):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    try:
        chat = Chat.objects.get(id=chat_id, owner=user)
    except Chat.DoesNotExist:
        return JsonResponse({'error': 'Chat not found'}, status=404)

    chat_data = {
        'id': chat.id,
        'title': chat.title,
        'parent_node_id': chat.parent_node.id if chat.parent_node else None,
        'created_at': chat.created_at,
        'updated_at': chat.updated_at,
    }

    return JsonResponse({'chat': chat_data})

@login_required
async def get_response(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    user = request.user
    if not sync_to_async(lambda: user.is_authenticated)():
        return JsonResponse({'error': 'Authentication required'}, status=401)

    prompt = request.POST.get('prompt')
    parent_node_id = request.POST.get('node_id')

    parent = await sync_to_async(lambda: Node.objects.filter(id=parent_node_id).first())()

    if not prompt or not parent_node_id:
        return JsonResponse({'error': 'Prompt and node_id are required'}, status=400)

    user_node = await sync_to_async(lambda: Node.create_node(content=prompt, node_type=NodeType.USER, parent=parent))()
    print("User ID:", user_node.id)
    print("User node parent ID:", user_node.parent.id)
    lineage = ChatGraphService.get_lineage(node=user_node)
    
    llm_service = LLMService()
    print("Lineage retrieved for LLM:", lineage)
    linear_history = llm_service.generate_history(lineage)
    print("Linear history generated for LLM:", linear_history)
    llm_response = await llm_service.get_response(linear_history)
    print("LLM Response:", llm_response)
    ai_message = llm_response.get("messages")[-1].content

    llm_node = await sync_to_async(lambda: Node.create_node(content=ai_message, node_type=NodeType.LLM, parent=user_node))()

    return JsonResponse({'response': ai_message})

@ensure_csrf_cookie
def get_csrf_token(request):
    """
    Get CSRF token for the frontend
    """
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

def register(request):
    """Register a new user. Expects POST with 'username' and 'password'."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    username = request.POST.get('username')
    password = request.POST.get('password')

    if not username or not password:
        return JsonResponse({'error': 'username and password are required'}, status=400)

    User = get_user_model()
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'user already exists'}, status=400)

    user = User(username=username)
    user.set_password(password)
    user.save()

    # Log the user in immediately so the session cookie is created for the client
    try:
        auth_login(request, user)
        print(f"[register] session_key={request.session.session_key} user={request.user} is_authenticated={request.user.is_authenticated}")
    except Exception:
        # If login fails for any reason, still return registered but client may need to call login
        return JsonResponse({'status': 'registered', 'username': user.username})

    return JsonResponse({'status': 'logged_in', 'username': user.username})

def login_view(request):
    """Login user. Expects POST with 'username' and 'password'. Sets session cookie."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    username = request.POST.get('username')
    password = request.POST.get('password')

    if not username or not password:
        return JsonResponse({'error': 'username and password are required'}, status=400)

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'error': 'invalid credentials'}, status=401)

    auth_login(request, user)
    print(f"[login] session_key={request.session.session_key} user={request.user} is_authenticated={request.user.is_authenticated}")
    return JsonResponse({'status': 'logged_in', 'username': user.username})

def logout_view(request):
    """Log out current user (POST)."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    auth_logout(request)
    return JsonResponse({'status': 'logged_out'})


def current_user(request):
    """Return current authenticated user's basic info."""
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    user = request.user
    print(f"[create_chat] session_key={request.session.session_key} user={user} is_authenticated={user.is_authenticated}")
    return JsonResponse({'user': None})