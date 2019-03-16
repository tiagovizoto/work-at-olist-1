from dateutil.parser import parse
from .models import CallStart, CallEnd
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CallStartSerializer, CallEndSerializer


class CallEndpoint(APIView):
    def post(self, request):
        if 'type' not in request.data:
            return Response(status=400, data={'Type of Call Record not informed'})

        if request.data['type'] == 'start':
            serializer = CallStartSerializer(data=request.data)
            if serializer.is_valid():
                result = CallStart.objects.filter(source=request.data['source']).order_by('-id').first()
                if result:
                    r = CallEnd.objects.filter(id=result.id).first()
                    if not r:
                        return Response(status=400, data={f"Call {result.id} not finalized"})
                    if r.timestamp > parse(request.data['timestamp']):
                        Response(data={"The Call time starting in last call. Call time must start after last call."}, status=400)
                serializer.save()
                return Response(data=serializer.data, status=201)
            return Response(data=serializer.errors, status=400)
        elif request.data['type'] == 'end':
            serializer = CallEndSerializer(data=request.data)
            if serializer.is_valid():
                result = CallStart.objects.filter(id=request.data['id'])
                if not result.first():
                    return Response(status=400, data={f"No exist the call id {request.data['id']} in start call records"})
                serializer.save()
                return Response(data=serializer.data, status=201)
            return Response(data=serializer.errors, status=400)
        else:
            return Response(status=400, data={'Type of Call Record is invalid'})
