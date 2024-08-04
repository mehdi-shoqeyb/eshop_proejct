from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from .models import ChatRoom

def index(request):
        chatrooms = ChatRoom.objects.filter(support_user=request.user)
        context = {
            'chatrooms':chatrooms
        }
        return render(request, 'chat_module/index.html',context)

class SupportChat(TemplateView):
    template_name = 'chat_module/support_chat.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs,)
        
        if not self.request.user.is_authenticated and not self.request.user.is_superuser:
            return redirect(reverse('home_page'))
        else:
            context['username'] = self.request.user.username
            context['current_room_id'] = self.kwargs['room_id']
            current_chat_room = ChatRoom.objects.filter(room_id=self.kwargs['room_id']).first()
            context['chtaroom_user'] = current_chat_room.user
            context['chatrooms'] = ChatRoom.objects.filter(support_user=self.request.user)
            return context
    