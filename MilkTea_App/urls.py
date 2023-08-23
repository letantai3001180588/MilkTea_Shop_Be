from django.urls import path

# from MilkTea_App.views import *
from . import views


urlpatterns = [
    # path("docs", views.GetAllProduct.as_view()),
    path("api/product/", views.getProduct, name="product"),
    path("api/login/", views.login_view, name="login"),
    path("api/register/", views.registration_view, name="register"),
    path("api/order/", views.getOrder, name="order"),
    path("api/order/create", views.create_order, name="createOrder"),
    path(
        "api/order/delete/<int:order_id>/",
        views.delete_order_item,
        name="DeleteOrder",
    ),
]
