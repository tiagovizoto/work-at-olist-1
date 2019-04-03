from dateutil import relativedelta
from rest_framework import serializers
from .models import FixedFee, MinuteFee, Bill
from apps.calls.serializers import CallStartSerializer, CallEndSerializer


class FixedFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedFee
        fields = ('id', 'price', 'start', 'end',)


class MinuteFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinuteFee
        fields = ('id', 'price', 'start', 'end',)


class BillSerializer(serializers.ModelSerializer):
    call_start = CallStartSerializer()
    call_end = CallEndSerializer()
    fixed_fee = FixedFeeSerializer()
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = ('id', 'price', 'fixed_fee', 'call_start', 'call_end', 'duration',)

    def get_duration(self, obj):
        duration = relativedelta.relativedelta(obj.call_end.timestamp, obj.call_start.timestamp)
        return f"{duration.days}d{duration.hours}h{duration.minutes}m{duration.seconds}s"
