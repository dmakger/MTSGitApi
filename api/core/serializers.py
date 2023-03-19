from rest_framework import serializers

from .models import Message, Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ("id", "username", "image")

    @staticmethod
    def get_username(model):
        return model.user.username


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ("id", "user", "text")

    @staticmethod
    def get_user(model):
        return ProfileSerializer(model.profile_to_chat.profile).data
