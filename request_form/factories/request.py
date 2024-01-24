import factory

from ..models import RequestModel


class RequestFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a RequestModel.
    """
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Sequence(lambda n: "request-%d@test.com" % n)
    message = factory.Faker("text", max_nb_chars=150)
    data_confidentiality_policy = True
    ip_address = factory.Faker("ipv4")
    # TODO: Until we fix the local region schism we still with hardcoded
    # valid number
    # phone = factory.Faker("phone_number")
    phone = "+33 6 12 34 56 78"

    class Meta:
        model = RequestModel
