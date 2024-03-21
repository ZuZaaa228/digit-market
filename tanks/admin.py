from django.contrib import admin
from .models import Tank, TankTransfer, TankSale

admin.site.register(Tank)
admin.site.register(TankTransfer)
admin.site.register(TankSale)
