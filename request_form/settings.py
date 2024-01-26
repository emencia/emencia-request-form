"""
Default application settings
----------------------------

These are the default settings you can override in your own project settings
right after the line which load the default app settings.

"""
from django.utils.translation import gettext_lazy as _


REQUEST_FORM_BANNED_TLD = tuple()
"""
All email addresses that end with these strings are not allowed to submit forms by
email.

Example : ::

    REQUEST_FORM_BANNED_TLD = (".ru", "qq.com")
"""

REQUEST_FROM_EMAIL = "request-form-from@localhost"
"""
Address used to send email notification.
"""

REQUEST_TO_EMAIL = ("request-form-to@localhost",)
"""
List of addresses used as recipients for email notification. Set it to ``None`` or
``False`` to disable email sending.
"""

REQUEST_EMAIL_SUBJECT = _("Website request form")
"""
Subject to add to email message.
"""

REQUEST_FORM_HELPER = None
"""
Python path to a crispy-form class helper instead of default one.

This must be a class compatible with
`FormHelper <https://django-crispy-forms.readthedocs.io/en/latest/api_helpers.html>`_.

Your class helper will have to manage attribute ``form_action``, ``form_tag`` and
buttons itself.
"""

REQUEST_FORM_SLOT_DEFINITIONS = "request_form.slot_definitions.BASE_DEFINITIONS"
"""
Python path to slot definitions dict variable. Default use the one included from this
applications. Give another valid Python path to dict with your custom definitions.
"""
