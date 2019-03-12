from rest_framework import serializers
from .models import CallStart, CallEnd


class CallStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallStart


class CallEndSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallEnd
