from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Message
from .serializers import MessageSerializer


class MessageView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False)
    def get_last_messages(self, request, pk):
        # COUNT_LAST_MESSAGES
        qs = self.queryset.filter(profile_to_chat__chat__pk=pk)
        return Response(
            self.serializer_class(qs, many=True).data,
            status=status.HTTP_200_OK,
        )