from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from core.views import ThreadViewSet, MessageCreateAPIView, MarkMessageAsRead, UnreadMessagesCount

router = DefaultRouter()
router.register(r'thread', ThreadViewSet, basename='thread')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
    path('threads/<int:thread_id>/message/', MessageCreateAPIView.as_view(), name='create_message'),
    path('threads/<int:thread_id>/message/<int:message_id>/read/', MarkMessageAsRead.as_view(), name='read_message'),
    path('unread_messages/', UnreadMessagesCount.as_view(), name="unread_messages_count")
]
