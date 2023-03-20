from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProfileView, MessageView

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),

    path("user/<int:pk>/", ProfileView.as_view({'get': 'get_detail_profile'})),
    path("chat/<int:pk>/", MessageView.as_view({'get': 'get_last_messages'})),
    path("chat/<int:pk>/message/send/", MessageView.as_view({'post': 'send_message'})),
]
