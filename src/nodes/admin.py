from django.contrib import admin

# Register your models here.
from .models import Node, Chat, UserSettings

admin.site.register(Node)
admin.site.register(Chat)
admin.site.register(UserSettings)
