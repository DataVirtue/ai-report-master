from .views import StreamChatView, ConversationViewsSet, ReportView
from django.urls import path
from rest_framework.routers import DefaultRouter

# routers
conversation_router = DefaultRouter()
conversation_router.register(
    r"conversations", ConversationViewsSet, basename="conversation"
)

urlpatterns = [
    path("chat/", StreamChatView.as_view()),  # no ID
    path("chat/<conversation_id>", StreamChatView.as_view()),
    path("report/<report_id>/<page_no>", ReportView.as_view()),
]

urlpatterns += conversation_router.urls
