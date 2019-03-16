from rest_framework import serializers
from .models import CallStart, CallEnd


class CallStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallStart
        fields = ('id', 'timestamp', 'source', 'destination',)


class CallEndSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallEnd
        fields = ('id', 'timestamp',)
