from datetime import datetime
from django.db.models import Q
from rest_framework import generics
from .models import MinuteFee, FixedFee
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FixedFeeSerializer, MinuteFeeSerializer


class FeeCreate:
    model = None

    def post(self, request, *args, **kwargs):
        if 'start' in request.data and 'end' in request.data:
            start = datetime.strptime(request.data['start'], "%H:%M:%S").time()
            end = datetime.strptime(request.data['end'], "%H:%M:%S").time()

            result = self.model.objects.filter(Q(start__range=[start, end]) | Q(end__range=[start, end]))

            if result.first() is not None:
                return Response(status=400, data={"Exist conflicts of times"})
        return super().post(request, *args, **kwargs)


class MinuteFeeListEndpoint(FeeCreate, generics.ListCreateAPIView):
    queryset = MinuteFee.objects.all()
    serializer_class = MinuteFeeSerializer
    model = MinuteFee


class MinuteFeeDetailEndpoint(generics.RetrieveDestroyAPIView):
    queryset = MinuteFee.objects.all()
    serializer_class = MinuteFeeSerializer


class FixedFeeListEndpoint(FeeCreate, generics.ListCreateAPIView):
    queryset = FixedFee.objects.all()
    serializer_class = FixedFeeSerializer
    model = FixedFee


class FixedFeeDetailEndpoint(generics.RetrieveDestroyAPIView):
    queryset = FixedFee.objects.all()
    serializer_class = FixedFeeSerializer


class BillEndPoint(APIView):
    def get(self, request, client_number, year, month=None):
        pass


class BillLastEndPoint(APIView):
    def get(self, request, client_number):
        pass
