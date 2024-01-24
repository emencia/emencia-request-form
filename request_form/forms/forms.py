from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from django.forms import ModelForm
from django.template.loader import render_to_string
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from captcha.fields import CaptchaField

from ..models import RequestModel
from ..form_helpers import RequestDefaultFormHelper
from ..utils.parsers import text_has_cyrillic_characters


class RequestForm(ModelForm):
    """
    Request form save data from valid submit and possibly send email.

    Form layout is managed through a Crispy form class helper, a basic one is used as
    default but you can define a custom one from setting ``REQUEST_FORM_HELPER``.
    """
    captcha = CaptchaField()
    data_confidentiality_policy = forms.BooleanField(
        required=True,
        error_messages={"required": _("You must accept data confidentiality policy.")},
    )

    class Meta:
        model = RequestModel
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "message",
            "data_confidentiality_policy",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Optionally load helper module from given python path if any
        if settings.REQUEST_FORM_HELPER:
            self.helper = import_string(settings.REQUEST_FORM_HELPER)(self)
        # Else fallback to a default one
        else:
            self.helper = RequestDefaultFormHelper(self)

    def clean_email(self):
        """
        Check email against filters.
        """
        email = self.cleaned_data.get("email").lower()

        if email.endswith(settings.REQUEST_FORM_BANNED_TLD):
            raise forms.ValidationError(_("This email address isn't allowed."))

        return email

    def clean_message(self):
        """
        Check message against filters.
        """
        message = self.cleaned_data.get("message")

        if text_has_cyrillic_characters(message):
            raise forms.ValidationError(_("Cyrillic characters are not allowed."))

        return message

    def send_email(self, from_email, to, saved):
        """
        Email sending.
        """
        plain_body = render_to_string(
            "request_form/request/email.txt",
            {
                "first_name": saved.first_name,
                "last_name": saved.last_name,
                "phone": (
                    saved.phone.as_national
                    if saved.phone
                    else ""
                ),
                "email": saved.email,
                "message": saved.message,
            }
        )

        email = EmailMessage(
            subject=settings.REQUEST_EMAIL_SUBJECT,
            body=plain_body,
            from_email=from_email,
            to=to,
        )

        # TODO: Add optional HTML rendering (depending setting)
        # msg.attach_alternative(html_content, "text/html")

        email.send()

    def save(self, *args, **kwargs):
        """
        Save request object.

        Keyword Arguments:
            email_sending_enabled (boolean): If value is True it enables email sending
                else no email is sent. Defaut is ``True``.

                Email sending activation depends also from setting ``REQUEST_TO_EMAIL``
                that must not be an empty value.
        """
        email_sending_enabled = kwargs.pop("email_sending_enabled", True)
        request = super().save(*args, **kwargs)

        if settings.REQUEST_TO_EMAIL and email_sending_enabled:
            self.send_email(
                settings.REQUEST_FROM_EMAIL,
                settings.REQUEST_TO_EMAIL,
                request
            )

        return request
