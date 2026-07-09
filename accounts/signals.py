"""Domain signals emitted by the accounts app."""
from django.dispatch import Signal

password_changed = Signal()
user_created = Signal()
