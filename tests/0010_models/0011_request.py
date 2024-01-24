import pytest

from django.core.exceptions import ValidationError

from request_form.factories import RequestFactory
from request_form.models import RequestModel


def test_model_basic(settings, db):
    """
    Basic model validation with required fields should not fail.
    """
    request = RequestModel(
        first_name="Donald",
        last_name="McDuck",
        phone="+33 6 12 34 56 78",
        email="donald@mcduck.com",
        message="coin coin",
        data_confidentiality_policy=True,
        ip_address="127.0.0.1",
    )
    request.full_clean()
    request.save()

    assert RequestModel.objects.filter(pk=request.id).count() == 1
    assert request.email == "donald@mcduck.com"


def test_model_required_fields(db):
    """
    Basic model validation with missing required fields should fail.
    """
    request = RequestModel()

    with pytest.raises(ValidationError) as excinfo:
        request.full_clean()

    assert excinfo.value.message_dict == {
        "first_name": [
            "This field cannot be blank."
        ],
        "last_name": [
            "This field cannot be blank."
        ],
        "email": [
            "This field cannot be blank."
        ],
        "message": [
            "This field cannot be blank."
        ],
        "data_confidentiality_policy": [
            "“None” value must be either True or False."
        ],
        "ip_address": [
            "This field cannot be null."
        ]
    }


def test_model_phone_validation(db, settings):
    """
    Allowed phone number format can be defined from settings.
    """
    # Valid payload data to use everytime
    base_payload = {
        "first_name": "Donald",
        "last_name": "McDuck",
        "email": "donald@mcduck.com",
        "message": "coin coin",
        "data_confidentiality_policy": True,
        "ip_address": "127.0.0.1",
    }

    # With default settings, international number is allowed
    request = RequestModel(phone="+33 1 12 34 56 78", **base_payload)
    request.full_clean()

    request = RequestModel(phone="+33112345678", **base_payload)
    request.full_clean()

    request = RequestModel(phone="+1 604-401-1234,987", **base_payload)
    request.full_clean()

    # National is not allowed
    request = RequestModel(phone="6044011234", **base_payload)
    with pytest.raises(ValidationError):
        request.full_clean()
    request = RequestModel(phone="01 12 34 56 78", **base_payload)
    with pytest.raises(ValidationError):
        request.full_clean()

    # Enable national number format as default representation
    settings.PHONENUMBER_DEFAULT_FORMAT = "NATIONAL"
    # Store numbers in national format
    settings.PHONENUMBER_DB_FORMAT = "NATIONAL"
    # Only accept for french numbers
    settings.PHONENUMBER_DEFAULT_REGION = "FR"

    # National number is allowed for french number
    request = RequestModel(phone="01 12 34 56 78", **base_payload)
    request.full_clean()
    request = RequestModel(phone="0112345678", **base_payload)
    request.full_clean()

    # International number is allowed
    request = RequestModel(phone="+33 1 12 34 56 78", **base_payload)
    request.full_clean()

    # Non french number is not allowed, international or not
    request = RequestModel(phone="+1 604-401-1234", **base_payload)
    with pytest.raises(ValidationError):
        request.full_clean()

    # Non french number is not allowed, national or not
    request = RequestModel(phone="6044011234", **base_payload)
    with pytest.raises(ValidationError):
        request.full_clean()


def test_factory_basic(db, settings):
    """
    Factory should create Request object without any required arguments.
    """
    request = RequestFactory()
    # Force model validation since factory bypass it
    request.full_clean()
    assert RequestModel.objects.filter(pk=request.id).count() == 1
