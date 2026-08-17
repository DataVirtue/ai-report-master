from typing import List
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import io


class EmailService:
    def send_email(
        self,
        to: List[str],
        subject: str,
        message: str,
        attachment: io.BytesIO,
        filename: str,
        mimetype: str,
    ):
        mail = EmailMultiAlternatives(
            to=to,
            subject=subject,
            from_email=settings.DEFAULT_FROM_EMAIL,
            body=message,
        )
        mail.attach(filename, attachment, mimetype)
        mail.send()
