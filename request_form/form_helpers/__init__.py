from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
# from crispy_forms.layout import Button, Submit


class RequestDefaultFormHelper(FormHelper):
    """
    A crispy form class helper used as default form layout helper.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.form_action = reverse("request_form:request-form")
        self.form_tag = True

        # TODO: Disabled until related Javascript code has been retrieved
        # self.add_input(
        #     Button(
        #         "new-captcha",
        #         _("Get a new captcha code"),
        #         css_id="request-form-new-captcha",
        #         css_class="btn-light",
        #     ),
        # )
        self.add_input(
            Submit("save", _("Submit"), css_id="request-form-submit"),
        )
