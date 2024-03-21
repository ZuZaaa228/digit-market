from django import forms

from authenticate.models import CustomUser
from .models import Tank, TankTransfer, TankSale


class BalanceForm(forms.Form):
    amount = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2, label='Amount')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].label = 'Цена'

class TankBuyForm(forms.ModelForm):
    class Meta:
        model = TankSale
        fields = ()


class TankSaleForm(forms.ModelForm):
    class Meta:
        model = TankSale
        fields = ('price',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].label = 'Цена'


class TankTransferForm(forms.ModelForm):
    class Meta:
        model = TankTransfer
        fields = ('to_user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['to_user'].queryset = CustomUser.objects.exclude(id=self.initial['from_user'].id)

    def clean_to_user(self):
        to_user = self.cleaned_data['to_user']
        if to_user is None:
            raise forms.ValidationError('You must select a user to transfer the tank to.')
        return to_user


class TankCreateForm(forms.ModelForm):
    class Meta:
        model = Tank
        fields = ['name', 'description', 'image']

    def save(self, commit=True):
        tank = super().save(commit=False)
        tank.owner = self.initial['owner']
        if commit:
            tank.save()
        return tank
