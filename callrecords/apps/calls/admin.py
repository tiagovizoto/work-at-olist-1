from django.contrib import admin
from .models import CallStart, CallEnd


class CallStartAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'destination', 'timestamp', 'created', 'modified',)


class CallEndAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'created', 'modified',)


admin.site.register(CallStart, CallStartAdmin)
admin.site.register(CallEnd, CallEndAdmin)
