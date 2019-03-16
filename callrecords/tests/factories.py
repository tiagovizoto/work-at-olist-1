import factory
from apps.calls.models import CallStart, CallEnd
from django.utils.dateparse import parse_datetime


class CallStartFactory(factory.django.DjangoModelFactory):
    id = 9999
    source = 56999997878
    destination = 45979797474
    timestamp = parse_datetime('2017-07-29T12:00:00Z')

    class Meta:
        model = CallStart


class CallEndFactory(factory.django.DjangoModelFactory):
    id = 9999
    timestamp = parse_datetime('2016-02-29T14:00:00Z')

    class Meta:
        model = CallEnd
