from django.urls import path
from .views import CallEndpoint

urlpatterns = [
    path('', CallEndpoint.as_view()),
]
