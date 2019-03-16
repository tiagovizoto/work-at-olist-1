import factory
from apps.calls.models import CallStart, CallEnd
from django.utils.dateparse import parse_datetime, parse_time
from apps.bills.models import Bill, FixedFee, MinuteFee, MinuteFeeBill


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


class MinuteFeeFactory(factory.django.DjangoModelFactory):
    price = 0.09
    start = parse_time('06:00:00')
    end = parse_time('22:00:00')

    class Meta:
        model = MinuteFee


class FixedFeeFactory(factory.django.DjangoModelFactory):
    price = 0.34
    start = parse_time('00:00:00')
    end = parse_time('23:59:59')

    class Meta:
        model = FixedFee


class BillFactory(factory.django.DjangoModelFactory):
    fixed_fee = factory.SubFactory(FixedFeeFactory)
    price = 56.00
    call_start = factory.SubFactory(CallStartFactory)
    call_end = factory.SubFactory(CallEndFactory)

    class Meta:
        model = Bill


class MinuteFeeBill(factory.django.DjangoModelFactory):
    minute_fee = factory.SubFactory(MinuteFeeFactory)
    bill = factory.SubFactory(BillFactory)

    class Meta:
        model = MinuteFeeBill
