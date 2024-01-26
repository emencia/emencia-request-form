from django.db import models
from django.utils.translation import gettext_lazy as _


class Slot(models.Model):
    """
    Slot defines a field for a Controller, generally a form input.
    """
    controller = models.ForeignKey(
        "request_form.controller",
        null=True,
        default=None,
        on_delete=models.CASCADE,
    )
    """
    Required controller relation.
    """

    kind = models.CharField(
        _("element type"),
        max_length=50,
    )
    """
    Required unique label string. This is the named showed to users to labelize the
    slot.
    """

    label = models.CharField(
        _("label"),
        max_length=100,
    )
    """
    Required unique label string. This is the named showed to users to labelize the
    slot.
    """

    name = models.SlugField(
        _("name"),
        max_length=100,
    )
    """
    Required unique name string. This is the input name used in HTML and slot
    representation.
    """

    required = models.BooleanField(
        verbose_name=_("required"),
        default=False,
        blank=True,
    )
    """
    Optional boolean to make slot required.
    """

    position = models.IntegerField(
        _("Position"),
        default=0
    )
    """
    Required position order in slot list.
    """

    help_text = models.TextField(_("help text"), blank=True, null=False)
    """
    Optional help text to show.
    """

    initial = models.CharField(
        _("initial"),
        blank=True,
        max_length=100,
    )
    """
    Optional initial value.
    """

    class Meta:
        ordering = ["label"]
        verbose_name = _("Form slot")
        verbose_name_plural = _("Form slots")

    def __str__(self):
        return self.label
