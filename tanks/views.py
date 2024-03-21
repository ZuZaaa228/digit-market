from authenticate.models import CustomUser
from .forms import TankCreateForm


def tank_create(request):
    if request.method == 'POST':
        form = TankCreateForm(request.POST, request.FILES, initial={'owner': request.user})
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = TankCreateForm(initial={'owner': request.user})
    return render(request, 'tank_forms/tank_form.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Tank, TankSale
from .forms import TankTransferForm, TankSaleForm


def tank_info(request, tank_id):
    tank = get_object_or_404(Tank, id=tank_id)
    if tank.is_for_sale:
        sales = get_object_or_404(TankSale, tank=tank.id, buyer=None)
    else:
        sales = TankSale.objects.filter(tank=tank.id, buyer=None)
    if request.method == 'POST':
        if 'transfer' in request.POST:
            form_transfer = TankTransferForm(request.POST, initial={'from_user': tank.owner, 'tank': tank})
            transfer = form_transfer.save(commit=False)
            transfer.from_user = request.user
            transfer.tank = tank
            transfer.save()
            tank.owner = transfer.to_user
            tank.save()
            return redirect('tank_info', tank_id=tank_id)
        if "sell" in request.POST:
            form_sell = TankSaleForm(request.POST, initial={'seller': tank.owner, 'tank': tank})
            sell = form_sell.save(commit=False)
            sell.seller = request.user
            sell.tank = tank
            sell.save()
            tank.is_for_sale = True
            tank.owner = sell.seller
            tank.save()

            return redirect('tank_info', tank_id=tank_id)
        if 'buy' in request.POST:
            if request.user.balance > sales.price:
                seller = get_object_or_404(CustomUser, id=sales.seller.id)
                seller.balance += sales.price
                seller.save()
                sales.buyer = request.user
                sales.save()
                request.user.balance -= sales.price

                request.user.save()
                tank.is_for_sale = False
                tank.owner = request.user
                tank.save()

            return redirect('tank_info', tank_id=tank_id)


    else:
        form_transfer = TankTransferForm(initial={'from_user': tank.owner, 'tank': tank})
        form_sell = TankSaleForm(initial={'from_user': tank.owner, 'tank': tank})
    context = {'tank': tank,
               'form_transfer': form_transfer,
               "form_sell": form_sell,
               'sales': sales}
    return render(request, 'tank_forms/tank_info.html',
                  context=context)
