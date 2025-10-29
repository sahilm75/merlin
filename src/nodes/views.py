from django.shortcuts import render
from django.http import HttpResponseNotAllowed
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from nodes.services import LLMService, ChatGraphService
from langchain.messages import SystemMessage, HumanMessage, AIMessage

from .models import Chat, Node, NodeType

def create_chat(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    user = request.user
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
    if not user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    prompt = request.POST.get('prompt')
    parent_node_id = request.POST.get('node_id')

    if not prompt or not parent_node_id:
        return JsonResponse({'error': 'Prompt and node_id are required'}, status=400)
    
    user_node = Node.create_node(content=prompt, node_type=NodeType.USER, parent_id=parent_node_id)
    lineage = ChatGraphService.get_lineage(node=user_node)
    
    llm_service = LLMService()
    state = llm_service.generate_history(lineage)
    llm_response = await llm_service.get_response(state)
    ai_message = llm_response.messages.messages[-1].content

    llm_node = Node.create_node(content=ai_message, node_type=NodeType.LLM, parent=user_node)

    return JsonResponse({'response': ai_message})