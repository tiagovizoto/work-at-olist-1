from django.contrib import admin
from .models import MinuteFee, FixedFee, Bill


class MinuteFeeAdmin(admin.ModelAdmin):
    list_display = ('price', 'start', 'end', 'time_total',)


class FixedFeeAdmin(admin.ModelAdmin):
    list_display = ('price', 'start', 'end', 'time_total',)


class BillAdmin(admin.ModelAdmin):
    list_display = ('price', 'call_start', 'call_end', 'fixed_fee',)


admin.site.register(MinuteFee, MinuteFeeAdmin)
admin.site.register(FixedFee, FixedFeeAdmin)
admin.site.register(Bill, BillAdmin)
