from django.urls import path
from .views import tank_create, tank_info

urlpatterns = [
    # другие URL-адреса
    path('create/', tank_create, name='tank_create'),
    path('info/<int:tank_id>/', tank_info, name='tank_info'),
]
