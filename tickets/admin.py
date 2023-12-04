from django.contrib import admin
from . models import Ticket
# Register your models here.

class TicketsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ticket, TicketsAdmin)