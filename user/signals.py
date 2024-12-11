from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MessageSupport, Ticket
from django.utils import timezone

@receiver(post_save, sender = MessageSupport)
def update_ticket_update_time(sender, instance, **kwargs):
    ticket = instance.ticket
    ticket.update_at = timezone.now()
    ticket.save()
