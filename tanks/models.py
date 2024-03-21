import os

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify


class TankTransfer(models.Model):
    tank = models.ForeignKey('Tank', on_delete=models.CASCADE)
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='отправитель')
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='получатель')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tank.name} передан от {self.from_user.username} к {self.to_user.username}'

    def save(self, *args, **kwargs):
        self.tank.owner = self.to_user
        self.tank.save()
        super().save(*args, **kwargs)


class TankSale(models.Model):
    tank = models.ForeignKey('Tank', on_delete=models.CASCADE)
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='продавец')
    buyer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='покупатель', blank=True,
                              null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tank.name} был продан {self.seller.username} для {self.buyer.username if self.buyer != None else "NoOne"} за {self.price}'

    def save(self, *args, **kwargs):
        self.tank.owner = self.buyer
        self.tank.save()
        super().save(*args, **kwargs)


def upload_to(instance, filename):
    extension = filename.split('.')[-1]
    filename = f'{slugify(instance.name)}_{get_random_string(10)}.{extension}'
    return f'tank/{filename}'


class Tank(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_to)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='tanks_owned', null=True,
                              blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_for_sale = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        print(self.image, self.image.name)
        if self.image:
            image_path = os.path.join(self.image.name)
            print(image_path, os.path.isfile(f"media/{image_path}"))
            if os.path.isfile(f"media/{image_path}"):
                os.remove(f"media/{image_path}")
        super().delete(*args, **kwargs)
