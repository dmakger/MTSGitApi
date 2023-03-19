from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MessageView

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),

    path("chat/<int:pk>/", MessageView.as_view({'get': 'get_last_messages'})),
]
