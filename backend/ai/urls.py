from .views import StreamChatView
from django.urls import path

urlpatterns = [
    path("api/chat/", StreamChatView.as_view()),
]
