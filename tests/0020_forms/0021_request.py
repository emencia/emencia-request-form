from request_form.forms import RequestForm
from request_form.models import RequestModel
from request_form.utils.tests import flatten_form_errors


def test_empty(db):
    """
    Empty form should not be valid because of required fields.
    """
    f = RequestForm({})

    validation = f.is_valid()
    assert validation is False
    assert flatten_form_errors(f) == {
        "first_name": [
            "This field is required."
        ],
        "last_name": [
            "This field is required."
        ],
        "email": [
            "This field is required."
        ],
        "message": [
            "This field is required."
        ],
        "data_confidentiality_policy": [
            "You must accept data confidentiality policy."
        ],
        "captcha": [
            "This field is required."
        ],
    }
    assert RequestModel.objects.count() == 0


def test_invalid(db):
    """
    Invalid field values should raises specific errors.
    """
    f = RequestForm({
        "first_name": "Vladimir",
        "last_name": "Botchneko",
        "phone": "01 48 74 52 32",
        "email": "plop@mail.ru",
        "message": "Lorem Самовольная ipsum",
        "data_confidentiality_policy": False,
        "captcha_0": "foo",
        "captcha_1": "bar",
    })

    validation = f.is_valid()
    assert validation is False

    # import json
    # print(json.dumps(flatten_form_errors(f), indent=4))

    assert flatten_form_errors(f) == {
        "phone": [
            (
                "Enter a valid phone number (e.g. +12125552368)."
            )
        ],
        "email": ["This email address isn't allowed."],
        "message": ["Cyrillic characters are not allowed."],
        "data_confidentiality_policy": ["You must accept data confidentiality policy."],
        'captcha': ['Invalid CAPTCHA'],
    }


def test_valid(client, db, mailoutbox, settings):
    """
    Form should save request object and send email if enabled.
    """
    settings.REQUEST_FROM_EMAIL = "donald@localhost"
    settings.REQUEST_TO_EMAIL = ("diasy@localhost",)
    settings.REQUEST_EMAIL_SUBJECT = "Coin coin"

    f = RequestForm({
        "first_name": "Edward",
        "last_name": "Snowden",
        "phone": "+33 1 48 74 52 32",
        "email": "ed@snowden.com",
        "message": "Hello, world!",
        "data_confidentiality_policy": True,
        "captcha_0": "PASSED",
        "captcha_1": "PASSED",
    })
    validation = f.is_valid()
    assert validation is True

    # Patch object to insert ip to simulate current view behavior
    created = f.save(commit=False)
    created.ip_address = "127.0.0.1"
    created.save()
    assert RequestModel.objects.count() == 1

    assert len(mailoutbox) == 1

    m = mailoutbox[0]
    assert m.subject == "Coin coin"
    assert m.from_email == "donald@localhost"
    assert list(m.to) == ["diasy@localhost"]
    assert m.body == "\n".join([
        "Emencia request form",
        "",
        "Last name: Edward",
        "First name: Snowden",
        "Phone: 01 48 74 52 32",
        "E-mail: ed@snowden.com",
        "",
        "Message:",
        "Hello, world!",
    ])


def test_valid_no_email(client, db, mailoutbox, settings):
    """
    Form should save request object without sending email if disabled.
    """
    # Empty recipient adress disable email sending.
    settings.REQUEST_TO_EMAIL = None

    f = RequestForm({
        "first_name": "Edward",
        "last_name": "Snowden",
        "phone": "+33 1 48 74 52 32",
        "email": "ed@snowden.com",
        "message": "Hello, world!",
        "data_confidentiality_policy": True,
        "captcha_0": "PASSED",
        "captcha_1": "PASSED",
    })
    validation = f.is_valid()
    assert validation is True

    # Patch object to insert ip to simulate current view behavior
    created = f.save(commit=False)
    created.ip_address = "127.0.0.1"
    created.save()
    assert RequestModel.objects.count() == 1

    assert len(mailoutbox) == 0
