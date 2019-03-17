from django.urls import path
from .views import MinuteFeeListEndpoint, MinuteFeeDetailEndpoint, FixedFeeListEndpoint, FixedFeeDetailEndpoint, BillLastEndPoint, BillEndPoint


urlpatterns = [
    path('fee/minute/', MinuteFeeListEndpoint.as_view(), name='minute_fee_list'),
    path('fee/minute/<int:pk>/', MinuteFeeDetailEndpoint.as_view(), name='minute_fee_detail'),
    path('fee/fixed/', FixedFeeListEndpoint.as_view(), name='fixed_fee_list'),
    path('fee/fixed/<int:pk>/', FixedFeeDetailEndpoint.as_view(), name='fixed_fee_detail'),
    path('<int:client_number>/', BillLastEndPoint.as_view(), name='bill_last_endpoint'),
    path('<int:client_number>/<int:year>/<int:month>/', BillEndPoint.as_view(), name='bill__year_month_endpoint'),
    path('<int:client_number>/<int:year>/', BillEndPoint.as_view(), name='bill_year_endpoint'),
]
