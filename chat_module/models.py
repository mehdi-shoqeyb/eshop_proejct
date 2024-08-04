from django.db import models
from account_module.models import User
import uuid

class ChatRoom(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=False,null=False, limit_choices_to={'is_superuser': False},verbose_name='کاربر')
    room_id = models.CharField(max_length=32,unique=True,verbose_name='آیدی چت')
    created_at = models.DateTimeField(auto_now_add=True)
    support_user = models.ManyToManyField(User, related_name='support_users',limit_choices_to={'is_superuser': True},verbose_name='پشتیبانی')
    
    def __str__(self):
        return self.room_id
    
    def save(self, *args, **kwargs):
        if not self.room_id:
            self.room_id = uuid.uuid4().hex
        super(ChatRoom, self).save(*args, **kwargs)

class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    athor = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def last_message(self,room_id):
        return Message.objects.filter(chatroom__room_id=room_id)
    
    def __str__(self):
        return self.athor.username