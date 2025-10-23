from django.db import models
from django.conf import settings
from enum import Enum

class NodeType(models.TextChoices):
    SYSTEM = 'SYS', 'System'
    USER = 'USR', 'User'
    LLM = 'LLM', 'llm'

# Create your models here.
class Node(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='Unnamed Node')
    content = models.TextField()
    node_type = models.CharField(
        max_length=3,
        choices=NodeType.choices,
    )
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @classmethod
    def create_node(cls, name, content, node_type, parent=None):
        node = cls(name=name, content=content, node_type=node_type, parent=parent)
        node.save()
        return node
    
    def get_parent(self):
        return self.parent
    
    def get_children(self):
        return self.children.all()

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, default='Untitled Chat')
    parent_node = models.ForeignKey(Node, blank=True, null=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chats'          # author.chats.all() -> all chats owned by user
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @classmethod
    def create_chat(cls, title, parent_node, owner):
        chat = cls(title=title, parent_node=parent_node, owner=owner)
        chat.save()
        return chat

class UserSettings(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, default='Anonymous')
    email = models.EmailField(blank=True, null=True)
    chats = models.ManyToManyField(Chat, blank=True)
    preferences = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name

    @classmethod
    def create_user_settings(cls, user_name, email, preferences):
        user_settings = cls(user_name=user_name, email=email, preferences=preferences)
        user_settings.save()
        return user_settings
    
    def get_chats(self):
        return self.chats.all()
