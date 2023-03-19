from django.contrib import admin

from .models import Profile, Chat, PositionChat, ProfileToChat, Message, Reaction, ReactionToMessage


class ProfileAdmin(admin.ModelAdmin):
    pass


class ChatAdmin(admin.ModelAdmin):
    pass


class PositionChatAdmin(admin.ModelAdmin):
    pass


class ProfileToChatAdmin(admin.ModelAdmin):
    pass


class MessageAdmin(admin.ModelAdmin):
    pass


class ReactionAdmin(admin.ModelAdmin):
    pass


class ReactionToMessageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(PositionChat, PositionChatAdmin)
admin.site.register(ProfileToChat, ProfileToChatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Reaction, ReactionAdmin)
admin.site.register(ReactionToMessage, ReactionToMessageAdmin)
