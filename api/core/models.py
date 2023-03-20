from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


# ===={ Юзер }====
class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, default=None)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        Profile.objects.create(user=user).save()


# ===={ Чат }====
class Chat(models.Model):
    image = models.ImageField(blank=True, null=True, default=None)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=255, null=True, default=None, blank=True)
    count_user = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.pk}) {self.title}"


class PositionChat(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title


class ProfileToChat(models.Model):
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE)
    profile = models.ForeignKey(to=Profile, on_delete=models.SET_NULL, null=True)
    position_chat = models.ForeignKey(to=PositionChat, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.pk}) '{self.chat.title}' {self.profile.user.username} [{self.position_chat.title}]"


@receiver(post_save, sender=ProfileToChat)
def add_profile_to_chat(sender, instance, **kwargs):
    if kwargs['origin']:
        chat = kwargs['instance'].chat
        chat.count_user += 1
        chat.save()


@receiver(post_delete, sender=ProfileToChat)
def pop_profile_to_chat(sender, **kwargs):
    if kwargs['origin']:
        chat = kwargs['instance'].chat
        chat.count_user -= 1
        chat.save()


# ===={ Сообщение }====
class Message(models.Model):
    profile_to_chat = models.ForeignKey(to=ProfileToChat, on_delete=models.SET_NULL, null=True)
    text = models.TextField()

    def __str__(self):
        return f"'{self.profile_to_chat.chat.title}' {self.profile_to_chat.profile.user.username} " \
               f"[{self.text}]"


# ===={ Реакции на сообщения }====
class Reaction(models.Model):
    emoji = models.CharField(max_length=16)

    def __str__(self):
        return self.emoji


class ReactionToMessage(models.Model):
    message = models.ForeignKey(to=Message, on_delete=models.CASCADE)
    profile_to_chat = models.ForeignKey(to=ProfileToChat, on_delete=models.CASCADE)
    reaction = models.ForeignKey(to=Reaction, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.pk}) '{self.chat.title}' {self.profile.user.username} [{self.position_chat.title}]"
