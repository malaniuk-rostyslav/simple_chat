from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Thread(models.Model):
    participants = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


@receiver(m2m_changed, sender=Thread.participants.through)
def participants_changed(sender, instance, **kwargs):
    if kwargs['action'] == 'pre_add':
        participant_count = instance.participants.count() + len(kwargs['pk_set'])
        if participant_count > 2:
            raise ValidationError('A Thread can have only up to 2 participants.')
