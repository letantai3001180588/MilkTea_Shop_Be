from django.db import models
from django.db.models import PositiveIntegerField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# Create your models here.
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.IntegerField(blank=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(max_length=10000, null=True)
    quantity = PositiveIntegerField()


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    products = models.ManyToManyField("Product", through="OrderItem")
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True)
    data_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)


class Shipping(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
