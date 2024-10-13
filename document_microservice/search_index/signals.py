from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django_elasticsearch_dsl.registries import registry
from api.models import Visit


@receiver(post_save, sender=Visit)
def update_document(sender, instance, **kwargs):
    """Update Visit document on added/changed Visit."""
    # instance = kwargs['instance']

    instances = instance.objects.all()
    for _instance in instances:
        registry.update(_instance)


@receiver(post_delete, sender=Visit)
def delete_document(sender, instance, **kwargs):
    """Update Visit document on deleted Visit."""

    instances = instance.objects.all()
    for _instance in instances:
        registry.update(_instance)
