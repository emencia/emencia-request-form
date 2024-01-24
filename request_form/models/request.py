from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.translation import gettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from phonenumber_field.modelfields import PhoneNumberField


class RequestModel(models.Model):
    first_name = models.CharField(
        _("First name"), blank=False, null=False, max_length=100
    )
    last_name = models.CharField(
        _("Last name"), blank=False, null=False, max_length=100
    )
    phone = PhoneNumberField(_("Phone"), null=True, blank=True)
    email = models.EmailField(_("E-mail"), blank=False, null=False)
    message = models.TextField(_("Message"), blank=False, null=False)
    data_confidentiality_policy = models.BooleanField(
        _("Data confidentiality policy"), blank=False, null=False
    )
    ip_address = models.GenericIPAddressField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("request")
        verbose_name_plural = _("requests")

    def __str__(self):
        return "[{email}] - {full_name}".format(
            email=self.email,
            full_name=self.full_name
        )

    @property
    def full_name(self):
        return "{last_name} {first_name}".format(
            last_name=self.last_name,
            first_name=self.first_name,
        )

    @property
    def short_message(self):
        return truncatechars(self.message, 70)


class RequestPluginModel(CMSPlugin):
    """
    Plugin model.

    This is a very basic model since it has no defined fields except placeholder slot
    relation implied by ``CMSPlugin`` inheritance.
    """

    def __str__(self):
        return "Form include #{}".format(self.id)
