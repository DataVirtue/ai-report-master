from ai.models import SavedReport
from .views import (
    SavedReportCreateView,
    SavedReportView,
    StreamChatView,
    ConversationViewsSet,
    ReportView,
    SavedReportViewSet,
)
from django.urls import path
from rest_framework.routers import DefaultRouter

# routers
conversation_router = DefaultRouter()
conversation_router.register(
    r"conversations", ConversationViewsSet, basename="conversation"
)

saved_report_router = DefaultRouter()
saved_report_router.register(
    r"saved-reports", SavedReportViewSet, basename="saved_report"
)

urlpatterns = [
    path("chat/", StreamChatView.as_view()),  # no ID
    path("chat/<conversation_id>", StreamChatView.as_view()),
    path("report/<report_id>/<page_no>", ReportView.as_view()),
    path("saved-report/<report_id>/<page_no>", SavedReportView.as_view()),
    path("report/save/<report_id>/", SavedReportCreateView.as_view()),
]

urlpatterns += conversation_router.urls
urlpatterns += saved_report_router.urls
