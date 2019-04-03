from datetime import datetime
from django.db.models import Q
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MinuteFee, FixedFee, Bill
from .serializers import FixedFeeSerializer, MinuteFeeSerializer, BillSerializer


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
        dt = datetime.today()
        price_total = 0.0

        if month:
            if month > 12:
                return JsonResponse({"Error": "Month must be less or equal than 12"}, status=400)
            if dt.year == year:
                if month < dt.month:
                    bill = Bill.objects.filter(
                        Q(call_start__source=client_number) & Q(call_end__timestamp__year=year) & Q(
                            call_end__timestamp__month__lte=month))
                    b = BillSerializer(bill, many=True)

                    for d in b.data:
                        price_total += float(d['price'])

                    data = {
                        'price': price_total,
                        'calls_count': len(bill),
                        'records': [b.data]
                    }

                    return JsonResponse(data)
                else:
                    return JsonResponse({"Error": "Month must be less than current month"}, status=400)
            elif year < dt.year:
                bill = Bill.objects.filter(Q(call_start__source=client_number) & Q(call_end__timestamp__year=year) & Q(
                    call_end__timestamp__month=month))

                call_count = len(bill)

                b = BillSerializer(bill, many=True)

                for d in b.data:
                    price_total += float(d['price'])

                data = {
                    'price': price_total,
                    'calls_count': call_count,
                    'records': [b.data]
                }

                return JsonResponse(data, safe=False)
            else:
                return JsonResponse({'error': f"The year {year} isn't lower or equal {dt.year}"}, status=400)
        else:
            if dt.year == year:
                months = dt.month - 1
                data = []
                for m in range(1, months + 1):
                    bill = Bill.objects.filter(
                        Q(call_start__source=client_number) & Q(call_end__timestamp__year=year) & Q(
                            call_end__timestamp__month=m)
                    )
                    b = BillSerializer(bill, many=True)
                    for d in b.data:
                        price_total += float(d['price'])

                    data.append(
                        {
                            'month': m,
                            'price': price_total,
                            'count_records': len(bill),
                            'records': [b.data]
                        }
                    )

                return JsonResponse(data, safe=False)
            elif year < dt.year:
                data = []
                for m in range(1, 13):
                    bill = Bill.objects.filter(
                        Q(call_start__source=client_number) & Q(call_end__timestamp__year=year) & Q(call_end__timestamp__month=m))
                    b = BillSerializer(bill, many=True)
                    for d in b.data:
                        price_total += float(d['price'])

                    data.append(
                        {
                            'month': m,
                            'price': price_total,
                            'count_records': len(bill),
                            'records': [b.data]
                        }
                    )
                    price_total = 0.00
                return JsonResponse(data, safe=False)
            else:
                return JsonResponse({'error': f"The year {year} isn't lower or equal {dt.year}"}, status=400)


class BillLastEndPoint(APIView):
    def get(self, request, client_number):
        dt = datetime.today()
        price_total = 0.0
        bill = Bill.objects.filter(Q(call_start__source=client_number) & Q(call_end__timestamp__year=dt.year) & Q(
            call_end__timestamp__month=dt.month - 1 if dt.month > 1 else 1))
        b = BillSerializer(bill, many=True)
        for d in b.data:
            price_total += float(d['price'])
        data = {'price': price_total, 'calls_count': len(bill), 'records': [b.data]}
        return JsonResponse(data, safe=False)
