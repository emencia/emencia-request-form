from django.urls import path

from .views import ControllerFormView, RequestFormView, RequestSuccessView

app_name = "request_form"


urlpatterns = [
    path("", RequestFormView.as_view(), name="request-form"),
    path("success/", RequestSuccessView.as_view(), name="request-success"),
    path("controller-sample/", ControllerFormView.as_view(), name="controller-sample"),
]
