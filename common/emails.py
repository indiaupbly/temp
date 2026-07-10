"""Centralized synchronous and asynchronous email helpers."""
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)
_executor = ThreadPoolExecutor(max_workers=getattr(settings, "EMAIL_ASYNC_WORKERS", 4))


def render_email_template(template_name: str, context: dict) -> str:
    return render_to_string(template_name, context)


def _submit_email(func: Callable, *args, **kwargs) -> None:
    def runner() -> None:
        try:
            func(*args, **kwargs)
        except Exception:
            logger.exception("Async email delivery failed.")
    _executor.submit(runner)


def send_email(subject: str, message: str, recipient_list: Iterable[str]) -> int:
    return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, list(recipient_list), fail_silently=False)


def send_email_async(subject: str, message: str, recipient_list: Iterable[str]) -> None:
    _submit_email(send_email, subject, message, list(recipient_list))


def send_html_email(subject: str, template_name: str, context: dict, recipient_list: Iterable[str]) -> int:
    html = render_email_template(template_name, context)
    email = EmailMessage(subject, strip_tags(html), settings.DEFAULT_FROM_EMAIL, list(recipient_list))
    email.content_subtype = "html"
    return email.send(fail_silently=False)


def send_html_email_async(subject: str, template_name: str, context: dict, recipient_list: Iterable[str]) -> None:
    _submit_email(send_html_email, subject, template_name, context, list(recipient_list))
