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
    start_call = CallStartSerializer()
    end_call = CallEndSerializer()
    fixed_fee = FixedFeeSerializer()

    class Meta:
        model = Bill
        fields = ('id', 'price', 'fixed_fee', 'call_start', 'call_end',)
