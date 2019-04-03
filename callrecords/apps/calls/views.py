from decimal import Decimal
from django.db.models import Q
from dateutil.parser import parse
from dateutil import relativedelta
from .models import CallStart, CallEnd
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import time, datetime, timedelta
from .serializers import CallStartSerializer, CallEndSerializer
from apps.bills.models import MinuteFee, FixedFee, Bill, MinuteFeeBill


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
                end_date = serializer.save()

                start = parse(str(result.first().timestamp.replace(tzinfo=None)))
                end = parse(serializer.data['timestamp']).replace(tzinfo=None)

                fixed_fee = search_fixed_fee(str(result.first().timestamp.time()))

                if fixed_fee is None:
                    price_fixed_fee = Decimal()
                else:
                    price_fixed_fee = fixed_fee.price

                if start.date() == end.date():
                    price = one_day(start, end)
                    bill = Bill.objects.create(price=price['price'] + price_fixed_fee, fixed_fee=fixed_fee, call_start=result.first(), call_end=end_date)
                elif (start.date() + timedelta(days=1)) != end.date():
                    price = several_days(start, end)
                    bill = Bill.objects.create(price=price['price'] + price_fixed_fee, fixed_fee=fixed_fee, call_start=result.first(), call_end=end_date)
                else:
                    price = two_days(start, end)
                    bill = Bill.objects.create(price=price['price'] + price_fixed_fee, fixed_fee=fixed_fee, call_start=result.first(), call_end=end_date)

                for p in price['periods']:
                    MinuteFeeBill.objects.create(minute_fee=p, bill=bill)

                return Response(data=serializer.data, status=201)
            return Response(data=serializer.errors, status=400)
        else:
            return Response(status=400, data={'Type of Call Record is invalid'})


def one_day(start, end):
    result = search_periods_in_time(start, end)
    duration = relativedelta.relativedelta(end, start)

    if result.first() is None:
        # If you do not find any period, the price will be set to zero
        final_price = Decimal()

    # if only one period is found
    elif len(result) == 1:
        # If the start of the connection is shorter than the period and if the end is greater than the period found
        # will be calculated total time of the period
        if start.time() < result.first().start and end.time() > result.first().end:
            final_price = result.first().price * Decimal(int(calculate_total_time(result.first().start, result.first().end).seconds / 60))
        # If the call is within the time of the period,
        # the total call time is calculated and used to calculate the price
        elif start.time() > result.first().start and end.time() < result.first().end:
            tm = total_minutes(days=duration.days, hours=duration.hours, minutes=duration.minutes)
            final_price = result.first().price * tm
        # If the connection start is shorter than the period, the time from the start times to the result end is calculated.
        elif start.time() > result.first().start:
            duration = time_to_relativedelta(start.time(), result.first().end)
            tm = total_minutes(hours=duration.hours, minutes=duration.minutes)
            final_price = result.first().price * tm
        # If the End time is less than the result, the time with the result start and end of the connection will be calculated
        elif end.time() < result.first().end:
            duration = time_to_relativedelta(result.first().start, end.time())
            tm = total_minutes(hours=duration.hours, minutes=duration.minutes)
            final_price = result.first().price * tm

    # If I found several periods.
    # It will be necessary to calculate the time of the first and the last indefinitely
    else:
        # If the start of the connection is greater
        if start.time() > result.first().start:
            duration_start = time_to_relativedelta(start.time(), result.first().end)
            tm = total_minutes(hours=duration_start.hours, minutes=duration_start.minutes)
            final_price = result.first().price * tm
        else:
            final_price = result.first().price * int(calculate_total_time(result.first().start, result.first().end).seconds / 60)
        # Final time case is greater than the connection time
        if result.last().end > end.time():
            duration_end = time_to_relativedelta(result.last().start, end.time())
            tm = total_minutes(hours=duration_end.hours, minutes=duration_end.minutes)
            final_price += result.last().price * tm
        else:
            final_price += result.last().price * int(calculate_total_time(result.last().start, result.last().end).seconds / 60)
        p = list_calculate_price(list(result)[1:-1])
        final_price += p

    # transform in type list
    periods = result if type(result) is list else list(result)

    return {'price': final_price, 'periods': periods}


def several_days(start, end):
    final_price = Decimal()
    p = int(0)

    new_s = datetime.combine(start.date() + timedelta(days=1), time(hour=0))
    new_e = datetime.combine(end.date() - timedelta(days=1), time(hour=23, minute=59, second=59))

    # Quantities of days that lasted the call, not counting the first and last day.
    total_days = relativedelta.relativedelta(new_e + timedelta(seconds=1), new_s).days

    # Search for start-up periods until the end of the day
    result_start = search_periods_in_time(start=start, end=datetime.combine(start.date(), time(hour=23, minute=59, second=59)))

    # Search for periods from the beginning of the day to the end time of the call
    result_end = search_periods_in_time(start=datetime.combine(end.date(), time(hour=0)), end=end)

    # Calculates the price of the first day.
    if result_start.first():
        # p is the total price of the first day, not counting the first period
        p = list_calculate_price(result_start[1:])
        if start.time() > result_start.first().start:
            duration_start = time_to_relativedelta(start.time(), result_start.first().end)
            tm = total_minutes(hours=duration_start.hours, minutes=duration_start.minutes)
            final_price += result_start.first().price * tm
        else:
            final_price += result_start.first().price * int(calculate_total_time(result_start.first().start, result_start.first().end).seconds / 60)

    # Calculate the price of the last day.
    if result_end.last():
        # p represents the total value of the last day, not counting the last period
        p = list_calculate_price(list(result_end)[:-1])
        if result_end.last().end > end.time():
            duration_end = time_to_relativedelta(result_end.last().start, end.time())
            tm = total_minutes(hours=duration_end.hours, minutes=duration_end.minutes)
            final_price += result_end.last().price * tm
        else:
            final_price += result_end.last().price * int(calculate_total_time(result_end.last().start, result_end.last().end).seconds / 60)

    result = MinuteFee.objects.all()
    price_in_day = Decimal()

    # Here is the calculation of price of each period within a day,
    # and added to price_in_day and then multiplied by the number of days.
    for r in result:
        price_in_day += calculate_price(calculate_total_time(r.start, r.end).seconds / 60, r.price)

    final_price += price_in_day * total_days
    final_price += p
    periods = result if type(result) is list else list(result)
    return {'price': final_price, 'periods': periods}


def two_days(start, end):
    final_price = Decimal()
    p = int(0)

    # result_start and result_end search the periods
    result_start = search_periods_in_time(start=start, end=datetime.combine(start.date(), time(hour=23, minute=59, second=59)))
    result_end = search_periods_in_time(start=datetime.combine(end.date(), time(hour=0)), end=end)

    # Here it transforms the two lists into one, but without repeating the values
    result = list(result_start) + list(set(result_end) - set(result_start))

    if result_start.first():
        p = list_calculate_price(result_start[1:])
        if start.time() > result_start.first().start:
            duration_start = time_to_relativedelta(start.time(), result_start.first().end)
            tm = total_minutes(hours=duration_start.hours, minutes=duration_start.minutes)
            final_price += result_start.first().price * tm
        else:
            final_price += result_start.first().price * int(calculate_total_time(result_start.first().start, result_start.first().end).seconds / 60)

    if result_end.last():
        p = list_calculate_price(list(result_end)[:-1])
        if result_end.last().end > end.time():
            duration_end = time_to_relativedelta(result_end.last().start, end.time())
            tm = total_minutes(hours=duration_end.hours, minutes=duration_end.minutes)
            final_price += result_end.last().price * tm
        else:
            final_price += result_end.last().price * int(calculate_total_time(result_end.last().start, result_end.last().end).seconds / 60)

    final_price += p
    periods = result if type(result) is list else list(result)
    return {'price': final_price, 'periods': periods}


def time_to_relativedelta(start, end):
    return relativedelta.relativedelta(datetime.combine(datetime.today(), end),
                                       datetime.combine(datetime.today(), start))


def list_calculate_price(result):
    price = Decimal()
    for r in result:
        price += calculate_price(calculate_total_time(result.start, result.end).seconds / 60, r.price)
    return price


def total_minutes(days=None, hours=None, minutes=None):
    total = 0
    if days:
        total += days * 24 * 60
    if hours:
        total += hours * 60
    if minutes:
        total += minutes
    return total


def calculate_price(minutes, minute_fee):
    return Decimal(minute_fee * int(minutes))


def search_periods_in_time(start, end):
    result = MinuteFee.objects.filter(
        Q(start__range=[start, end]) | Q(end__range=[start, end])
    ).order_by('start')
    if not result.first():
        result = MinuteFee.objects.filter(start__lte=start.time(), end__gte=end.time())
        return result
    return result


def search_fixed_fee(s_time):
    # result = FixedFee.objects.filter(start__gte=time, end__lte=time)
    # Search for a period that contains a certain time..
    result = FixedFee.objects.raw("select * from bills_fixedfee where %s >= start and %s <= bills_fixedfee.end and is_removed = 'f'", [s_time, s_time])
    try:
        r = result[0]
    except IndexError:
        r = None
    return r


def calculate_total_time(start, end):
    return datetime.combine(datetime.today().date(), end) - datetime.combine(datetime.today().date(), start)
