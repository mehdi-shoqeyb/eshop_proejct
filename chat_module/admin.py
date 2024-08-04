from django.contrib import admin
from .models import Message,ChatRoom
# Register your models here.

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'user', 'created_at')  # Include 'user' here
    search_fields = ('room_id', 'user__username')     # Optional: For searching by username
    fields = ('user', 'room_id', 'support_user')

admin.site.register(Message)