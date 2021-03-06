from django.db import models
from utils.models import BaseModel
from apps.calls.models import CallStart, CallEnd
from model_utils.models import TimeStampedModel, SoftDeletableModel


class Fee(TimeStampedModel, SoftDeletableModel, BaseModel):
    price = models.DecimalField(decimal_places=2, max_digits=12)
    start = models.TimeField()
    end = models.TimeField()

    class Meta:
        abstract = True


class MinuteFee(Fee):
    pass


class FixedFee(Fee):
    pass


class Bill(TimeStampedModel, SoftDeletableModel, BaseModel):
    price = models.DecimalField(decimal_places=2, max_digits=12)
    fixed_fee = models.ForeignKey(FixedFee, on_delete=models.CASCADE, null=True)
    call_start = models.ForeignKey(CallStart, on_delete=models.CASCADE)
    call_end = models.ForeignKey(CallEnd, on_delete=models.CASCADE)


class MinuteFeeBill(BaseModel):
    minute_fee = models.ForeignKey(MinuteFee, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
