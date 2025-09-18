from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        token = str(uuid.uuid4())
        instance.activation_code = token
        instance.save()

        activation_link = f"http://127.0.0.1:8000/auth/activate/?token={token}"
        subject = "Активация аккаунта"
        message = f"Привет, {instance.username}!\n\nПерейди по ссылке, чтобы активировать аккаунт:\n{activation_link}"

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )