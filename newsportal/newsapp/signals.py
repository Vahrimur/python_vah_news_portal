from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory
from .tasks import email_after_new_post


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(instance, **kwargs):
    if kwargs['action'] == 'post_add':
        email_after_new_post(instance.pk)
