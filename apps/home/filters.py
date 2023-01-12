import  django_filters




from .models import *
from ..users.models import Persons


class ShowMeResidentsFilter(django_filters.FilterSet):
    class Meta:
        model = Persons
        fields ="__all__"



def build_fields(model_type):

    fields = [
        f.name for f in model_type._meta.get_fields()
        if type(f) in SUPPORTED
    ]

    return fields


def generate_filterset(model_type):

    class FilterSet(django_filters.FilterSet):
        class Meta:
            model = model_type
            fields = build_fields(model_type)

    return FilterSet

