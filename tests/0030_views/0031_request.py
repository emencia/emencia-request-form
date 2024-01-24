from django.urls import reverse

from request_form.models import RequestModel
from request_form.utils.tests import html_pyquery


def test_initial_form_view(client, db, settings):
    """
    View should respond with success and contain the form.
    """
    settings.LANGUAGE_CODE = "en"

    url = reverse("request_form:request-form")

    response = client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    assert len(dom.find("#request-form form")) == 1


def test_initial_success_view(client, db, settings):
    """
    Just ensure the static view is responding with success.
    """
    settings.LANGUAGE_CODE = "en"

    url = reverse("request_form:request-success")

    response = client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200


def test_post_valid(client, db, settings):
    """
    View should respond to POST request and save form request when it is valid.

    Also check the ip_address field is correctly filled.
    """
    settings.LANGUAGE_CODE = "en"

    request_form = {
        "first_name": "Edward",
        "last_name": "Snowden",
        "phone": "+33 1 48 74 52 32",
        "email": "ed@snowden.com",
        "message": "Hello, world!",
        "data_confidentiality_policy": True,
        "captcha_0": "PASSED",
        "captcha_1": "PASSED",
    }

    response = client.post(
        reverse("request_form:request-form"),
        request_form,
        follow=True
    )
    assert response.redirect_chain == [
        (reverse("request_form:request-success"), 302)
    ]
    assert response.status_code == 200
    assert RequestModel.objects.count() == 1

    request = RequestModel.objects.all()[0]
    assert request.ip_address == "127.0.0.1"


def test_post_invalid(client, db, settings):
    """
    View should respond to POST request and raise field errors when form request is
    invalid.
    """
    settings.LANGUAGE_CODE = "en"

    response = client.post(reverse("request_form:request-form"), {}, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200
    assert RequestModel.objects.count() == 0

    dom = html_pyquery(response)
    assert len(dom.find("#request-form form .form-control.is-invalid")) > 1
