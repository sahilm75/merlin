from django.contrib import admin

# Register your models here.
from .models import Node, Chat

admin.site.register(Node)
admin.site.register(Chat)
