from django import forms

from request_form.utils.tests import flatten_form_errors
from request_form.forms.controller import FormClassBuilder
from request_form.factories import ControllerFactory, SlotFactory


def test_construct_class_attrs(db):
    """
    R&D to demonstrate usage of type to build class with attributes.
    """
    attrs = {
        "your-name": forms.CharField(max_length=50, required=True),
        "your-number": forms.IntegerField(min_value=5, max_value=15),
    }

    Weirdo = type("Weirdo", (forms.Form,), attrs)

    f = Weirdo()
    # print(f.as_p())

    validation = f.is_valid()
    assert validation is False
    assert flatten_form_errors(f) == {}

    assert ("id_your-name" in f.as_p()) is True


def test_get_slot_scheme(db):
    """
    Method get_slot_scheme should return a slot scheme either from a dict, list or
    Controller object.
    """
    builder = FormClassBuilder()

    # Directly from a dict
    assert builder.get_slot_scheme({
        "foo": {
            "kind": "text-simple",
            "label": "Foo",
            "name": "foo",
            "required": False,
            "position": 1,
            "help_text": "",
            "initial": ""
        },
    }) == {
        "foo": {
            "kind": "text-simple",
            "label": "Foo",
            "name": "foo",
            "required": False,
            "position": 1,
            "help_text": "",
            "initial": ""
        },
    }

    # From a list than can be turned to a dict
    assert builder.get_slot_scheme((
        (
            "foo", {
                "kind": "text-simple",
                "label": "Foo",
                "name": "foo",
                "required": False,
                "position": 1,
                "help_text": "",
                "initial": ""
            },
        ),
    )) == {
        "foo": {
            "kind": "text-simple",
            "label": "Foo",
            "name": "foo",
            "required": False,
            "position": 1,
            "help_text": "",
            "initial": ""
        },
    }

    # From a controller with slots
    control = ControllerFactory()
    SlotFactory(label="Foo", name="foo", controller=control, position=1)
    SlotFactory(label="Bar", name="bar", controller=control, position=2)
    assert builder.get_slot_scheme(control) == {
        "foo": {
            "kind": "text-simple",
            "label": "Foo",
            "name": "foo",
            "required": False,
            "position": 1,
            "help_text": "",
            "initial": ""
        },
        "bar": {
            "kind": "text-simple",
            "label": "Bar",
            "name": "bar",
            "required": False,
            "position": 2,
            "help_text": "",
            "initial": ""
        }
    }


def test_get_formfields(db):
    """
    Method should return a dict of form fields built from given slot scheme.
    """
    builder = FormClassBuilder()

    # Directly from a dict
    fields = builder.get_formfields({
        "foo": {
            "kind": "text-simple",
            "label": "Foo",
            "name": "foo",
            "required": False,
            "position": 1,
            "help_text": "Helping",
            "initial": "Lorem ipsum",
        },
    })

    assert isinstance(fields["foo"], forms.Field) is True
    assert fields["foo"].label == "Foo"
    assert fields["foo"].help_text == "Helping"
    assert fields["foo"].required is False
    assert fields["foo"].initial == "Lorem ipsum"
