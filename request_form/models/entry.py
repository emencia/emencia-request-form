from django.db import models
from django.utils.translation import gettext_lazy as _


class Entry(models.Model):
    """
    Entry contains user submitted data from a request on a controller
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
        _("name"),
        max_length=100,
    )
    """
    Required unique label string. This is the named showed to users to labelize the
    slot.
    """

    request = models.JSONField(null=True)
    """
    Where is saved data from a request
    """

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = _("Form slot")
        verbose_name_plural = _("Form slots")

    def __str__(self):
        return self.label
