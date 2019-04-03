from django.db import models
from utils.models import BaseModel
from django.core.exceptions import ValidationError
from model_utils.models import TimeStampedModel, SoftDeletableModel


class Call(TimeStampedModel, SoftDeletableModel, BaseModel):
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        abstract = True


class CallStart(Call):
    source = models.BigIntegerField()
    destination = models.BigIntegerField()

    def validate(self):
        if not 10 <= len(str(self.source)) <= 11:
            raise ValidationError("The source number phone should in between 10 ans]d 11 length!")
        if not 10 <= len(str(self.source)) <= 11:
            raise ValidationError("The destination number phone should in between 10 ans]d 11 length!")

    def save(self, *args, **kwargs):
        self.validate()
        return super().save(*args, **kwargs)


class CallEnd(Call):
    pass
