# api/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        # Check if a token already exists for the user
        existing_token = Token.objects.filter(user=instance).first()

        if existing_token:
            # If a token already exists, you can choose to update it or handle it based on your requirements
            # For example, you might want to refresh the token or log a message
            existing_token.key = 'new_key'  # Update the key or refresh the token
            existing_token.save()
        else:
            # If no token exists, create a new one
            Token.objects.create(user=instance)
