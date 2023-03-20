from rest_framework import serializers

from .models import Message, Profile, Chat, ProfileToChat


class DetailProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ("id", "username", "email", "image")

    @staticmethod
    def get_username(model):
        return model.user.username

    @staticmethod
    def get_email(model):
        return model.user.email


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

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data, **self.context)


class ShortMessageSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ("id", "username", "text")

    @staticmethod
    def get_username(model):
        return model.profile_to_chat.profile.user.username


class ChatSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ("id", "image", "title", "last_message")

    @staticmethod
    def get_last_message(model):
        pk_ptc = ProfileToChat.objects.filter(chat=model)[0].pk
        qs = Message.objects.filter(profile_to_chat=pk_ptc)
        return ShortMessageSerializer(qs[len(qs)-1]).data
