from django.urls import path
from .views import index,SupportChat

urlpatterns = [
    path('',index,name='index'),
    path("<str:room_id>/", SupportChat.as_view(), name="support-pannel"),
]
