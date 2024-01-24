from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from ..forms import RequestForm
from ..models import RequestModel
from ..utils.network import get_user_ip_address


class RequestFormView(FormView):
    """
    The Request form view.

    When a request submit succeed, response is a redirection to ``RequestSuccessView``.
    """
    template_name = "request_form/request/form.html"
    model = RequestModel
    form_class = RequestForm
    success_url = reverse_lazy("request_form:request-success")

    def form_valid(self, form):
        # NOTE: May not be the best place, get_user_ip_address may be part of form
        # instead
        form.instance.ip_address = get_user_ip_address(request=self.request)
        form.save()

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if not form.is_valid():
            return self.form_invalid(form)

        return self.form_valid(form)


class RequestSuccessView(TemplateView):
    """
    Basic template view to respond to form submit success.
    """
    template_name = "request_form/request/form_success.html"
