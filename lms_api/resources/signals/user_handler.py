from django.dispatch import receiver

from lms_api.apps.core import models

from . import user_create


@receiver(user_create)
def on_user_create(sender, **kwargs):
    """Handle post-user creation tasks"""
    user_data = kwargs["user"]
    address_data = kwargs["address"]

    user = models.User.objects.create(**user_data)
    models.Address.objects.create(**address_data, user=user)
