from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Member, Savings


@receiver(post_save, sender=Member)
def create_savings_account(sender, instance, created, **kwargs):
    """Auto-create Savings account saat Member baru dibuat."""
    if created:
        Savings.objects.get_or_create(member=instance)
