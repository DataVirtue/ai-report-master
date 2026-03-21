from .views import ChatView
from django.urls import path

urlpatterns = [
    path("api/chat/", ChatView.as_view()),
]
