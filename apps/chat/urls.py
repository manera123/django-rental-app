from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'chat'
urlpatterns = [
    path('messages', views.index, name='index'),
    path('messages/chat/<int:id>', views.view_messages, name='chat_with_user'),
    path('ajax/handle-unseen-messages/',views.handle_unseen_messages,name='handle-unseen-messages'),
    path('ajax/handle-message-liking/',views.handle_message_liking,name='handle-message-liking'),

    path('ajax/view-typing-box/',views.view_typing_box,name='view-typing-box'),
    path('ajax/send-message/<int:id>/',views.send_message,name='send-message'),
	path('ajax/send-image-message/<int:id>/',views.handle_image_messages,name='send-image'),   
]