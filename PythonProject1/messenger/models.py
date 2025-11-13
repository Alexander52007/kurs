from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    full_name = models.CharField("ФИО", max_length=150, blank=True)
    position = models.CharField("Должность", max_length=100, blank=True)
    department = models.CharField("Отделение", max_length=100, blank=True)
    photo = models.ImageField("Фотография", upload_to="profile_photos/", blank=True, null=True)
    medical_specialization = models.CharField("Медицинская специализация", max_length=200, blank=True)
    experience_years = models.PositiveIntegerField("Стаж (лет)", blank=True, null=True)
    bio = models.TextField("О себе", blank=True)

    def __str__(self):
        return f"Профиль: {self.full_name or self.user.username}"


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        participants = self.participants.all()
        if participants.count() == 2:
            return f"Чат между {participants[0].username} и {participants[1].username}"
        return f"Чат с {participants.count()} участниками"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField("Содержание")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()