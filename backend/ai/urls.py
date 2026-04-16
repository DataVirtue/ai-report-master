from .views import StreamChatView, ConversationViewsSet
from django.urls import path
from rest_framework.routers import DefaultRouter

# routers
conversation_router = DefaultRouter()
conversation_router.register(
    r"conversations", ConversationViewsSet, basename="conversation"
)

urlpatterns = [
    path("api/chat/", StreamChatView.as_view()),
]

urlpatterns += conversation_router.urls
