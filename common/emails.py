"""Centralized email helpers."""
from typing import Iterable

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def render_email_template(template_name: str, context: dict) -> str:
    return render_to_string(template_name, context)


def send_email(subject: str, message: str, recipient_list: Iterable[str]) -> int:
    return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, list(recipient_list), fail_silently=False)


def send_html_email(subject: str, template_name: str, context: dict, recipient_list: Iterable[str]) -> int:
    html = render_email_template(template_name, context)
    email = EmailMessage(subject, strip_tags(html), settings.DEFAULT_FROM_EMAIL, list(recipient_list))
    email.content_subtype = "html"
    return email.send(fail_silently=False)
