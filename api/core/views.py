from rest_framework import viewsets, status, permissions
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .helper.views_helper import ERROR_USER_NOT_FOUND, ERROR_CHAT_NOT_FOUND, get_error
from .models import Message, ProfileToChat, Chat, Profile
from .serializers import MessageSerializer, ChatSerializer, DetailProfileSerializer


class ProfileView(viewsets.ModelViewSet):
    serializer_class = DetailProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(methods=['get'], detail=False)
    def get_detail_profile(self, request, pk):
        qs = self.queryset.filter(pk=pk)
        if len(qs) == 0:
            return get_error(**ERROR_CHAT_NOT_FOUND)
        return Response(
            self.serializer_class(qs[0]).data,
            status=status.HTTP_200_OK,
        )


class MessageView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False)
    def get_last_messages(self, request, pk):
        qs_chat = ProfileToChat.objects.filter(chat__pk=pk)
        if len(qs_chat) == 0:
            return get_error(**ERROR_CHAT_NOT_FOUND)
        if len(qs_chat.filter(profile__user=request.user)) == 0:
            return get_error(**ERROR_USER_NOT_FOUND)
        qs = self.queryset.filter(profile_to_chat=qs_chat[0])
        return Response(
            self.serializer_class(qs, many=True).data,
            status=status.HTTP_200_OK,
        )

    @action(methods=['post'], detail=False)
    def send_message(self, request, pk):
        qs_chat = ProfileToChat.objects.filter(chat__pk=pk)
        if len(qs_chat) == 0:
            return get_error(**ERROR_CHAT_NOT_FOUND)
        qs_cur_user = qs_chat.filter(profile__user=request.user)
        if len(qs_cur_user) == 0:
            return get_error(**ERROR_USER_NOT_FOUND)

        serializer = self.serializer_class(data=request.data, context={
            'profile_to_chat': qs_cur_user[0]
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': "Сообщение добавлено",
            **serializer.data
        }, status=status.HTTP_200_OK)


class ChatView(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False)
    def get_chats(self, request):
        qs = []
        for ptc in ProfileToChat.objects.filter(profile__user=request.user):
            qs.append(self.serializer_class(ptc.chat).data)
        return Response(qs, status=status.HTTP_200_OK,)
