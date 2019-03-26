from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__} {self.id}"

    def __repr__(self):
        return f"<self.__repr__()>"
