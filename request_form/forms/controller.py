import copy

from django import forms
from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from ..exceptions import ControllerError
from ..models import Controller


class ControllerBaseForm(forms.Form):
    """
    TODO: Should be an abstract to inherit instead of directly forms.Form so we can
    include internal controller stuff if needed.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Save request object.
        """
        return


class FormClassBuilder:
    """
    TODO: Should be able to build a form from given slot scheme.
    """
    def __init__(self, default_klass=None):
        self.default_klass = default_klass or ControllerBaseForm

    def get_slot_scheme(self, slots):
        """
        Normalize given content as a slot scheme.

        TODO: This should perform some validation on dict or list.

        Arguments:
            slots (object): Either a dict, a list or a Controller instance. Dict or
                list format must be a valid slot scheme.

        Returns:
            dict:
        """
        if isinstance(slots, list) or isinstance(slots, tuple):
            slots = dict(slots)
        elif isinstance(slots, Controller):
            slots = slots.as_scheme()

        return slots

    def get_formfields(self, slots):
        """
        TODO: Should return a dict of form fields for given slots.
        """
        fields = {}
        definitions = import_string(settings.REQUEST_FORM_SLOT_DEFINITIONS)

        for name, slot in slots.items():
            if slot["kind"] not in definitions:
                msg = _("Slot definition does not exists for given name: {}")
                raise ControllerError(msg.format(slot["kind"]))

            print("- Slot:", name, slot["kind"])
            definition = definitions[slot["kind"]]

            # Get the base defined options and update them with some slot attributes
            field_options = copy.deepcopy(definition["kwargs"])
            field_options.update({
                "label": slot["label"],
                "initial": slot["initial"],
                "help_text": slot["help_text"],
                "required": slot["required"],
            })

            # Register built field in field map
            fields[name] = definition["field"](**field_options)

        return fields

    def get_form(self, scheme, klass=None):
        """
        TODO: Should return the form class built from given slot scheme.
        """
        self.klass = klass or self.default_klass

        slots = self.get_slots(scheme)
        fields = self.get_formfields(slots)

        return type("ControllerForm", (forms.Form,), fields)
