from cms.api import add_plugin
from cms.utils.urlutils import admin_reverse

from request_form.factories import PageFactory, UserFactory
from request_form.plugins.request import RequestPlugin
from request_form.utils.tests import html_pyquery


def test_form_view_add(db, client, settings):
    """
    Plugin creation form should return a success status code and every
    expected field should be present in HTML.
    """
    settings.LANGUAGE_CODE = "en"

    client.force_login(
        UserFactory(is_staff=True, is_superuser=True)
    )

    # Create dummy page where to insert plugin
    page = PageFactory(
        title__language=settings.LANGUAGE_CODE,
        template=settings.TEST_PAGE_TEMPLATES
    )

    # Get placeholder destination
    placeholder = page.placeholders.get(slot="content")

    # Get the edition plugin form url and open it
    response = client.get(admin_reverse("cms_page_add_plugin"), {
        "plugin_type": "RequestPlugin",
        "placeholder_id": placeholder.pk,
        "target_language": "en",
        "plugin_language": "en",
    })

    # Expected http success status
    assert response.status_code == 200

    # Parse resulting plugin fields
    dom = html_pyquery(response)

    # There is currently no input except the internal ones from DjangoCMS
    assert sorted([
        item.get("name")
        for item in dom.find("#requestpluginmodel_form input")
    ]) == ["_popup", "_save", "csrfmiddlewaretoken"]


def test_render_in_page(db, client, settings):
    """
    Plugin should be properly rendered in a Page.
    """
    settings.LANGUAGE_CODE = "en"

    # Create dummy page where to insert plugin
    page = PageFactory(
        title__language=settings.LANGUAGE_CODE,
        template=settings.TEST_PAGE_TEMPLATES
    )

    # Add plugin to page placeholder and publish
    add_plugin(
        page.placeholders.get(slot="content"),
        RequestPlugin,
        settings.LANGUAGE_CODE,
    )

    # Get the rendered page with expected plugin
    page.publish(settings.LANGUAGE_CODE)
    url = page.get_absolute_url(language=settings.LANGUAGE_CODE)
    response = client.get(url)
    # print()
    # print(response.content.decode())
    # print()

    # Request form should be here with its inputs
    dom = html_pyquery(response)
    assert len(dom.find(".request-form-plugin form")) == 1
    assert len(dom.find(".request-form-plugin form input")) > 1
