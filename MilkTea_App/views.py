from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from MilkTea_App.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


# Create your views here.
# class GetAllProduct(APIView):
@api_view(["GET"])
def getProduct(request):
    list = Product.objects.all()
    mydata = GetAllProductSerializer(list, many=True)
    return Response(data=mydata.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    info = User.objects.filter(username=request.data.get("username"))
    serializer = UserSerializer(info, many=True)

    if user is not None:
        # Đăng nhập thành công, trả về thông tin user hoặc token JWT
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)
        # payload = {
        #     "user": user,
        #     "exp": datetime.utcnow() + timedelta(days=1),  # Token hết hạn sau 1 ngày
        # }
        # token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return Response(
            {
                "message": "Đăng nhập thành công",
                "accessToken": str(access),
                "refreshToken": str(refresh),
                "user": serializer.data,
            },
        )
    else:
        # Đăng nhập thất bại
        return Response({"error": "Tài khoản hoặc mật khẩu của bạn không đúng!"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response({"message": "Đăng xuất thành công"}, status=status.HTTP_200_OK)
    return Response(
        {"message": "Không tìm thấy refresh token"},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Đăng ký thành công"}, status=201)
    else:
        return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrder(request):
    order = Order.objects.filter(customer=request.user)
    order2 = Order.objects.get(customer=request.user)
    order_item = OrderItem.objects.filter(Order=order2)
    dataOrder = OrderSerializer(order, many=True)
    dataOrderItem = OrderItemSerializer(order_item, many=True)
    return Response(data={"order": dataOrder.data, "orderItem": dataOrderItem.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])  # Yêu cầu xác thực bằng Access Token
def create_order(request):
    order_data = {
        "customer": request.user.id,
        # Thêm các trường dữ liệu khác của Order tùy theo model và serializer của bạn
    }
    order_serializer = OrderSerializer(data=order_data)

    if order_serializer.is_valid():
        # Gán người dùng hiện tại vào Order
        order = order_serializer.save()
        order_item_data = {
            "Order": order.id,
            "product": request.data.get("id"),
            "quantity": request.data.get("quantity"),
            # Thêm các trường dữ liệu khác của OrderItem tùy theo model và serializer của bạn
        }

        order_item_serializer = OrderItemSerializer(data=order_item_data)
        if order_item_serializer.is_valid():
            order_item_serializer.save()
            return Response({"message": "Đặt hàng thành công"}, status=201)
        else:
            order.delete()
            # return Response(order_item_serializer.errors, status=400)
            return print("xin chao")
    else:
        # return Response(order_serializer.errors, status=400)
        return print("hello")


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])  # Yêu cầu xác thực bằng Access Token
def delete_order_item(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.customer != request.user:
            return Response(
                {"message": "Bạn không có quyền xóa OrderItem này"},
                status=status.HTTP_403_FORBIDDEN,
            )

        order.delete()
        return Response(
            {"message": "Xóa OrderItem thành công"}, status=status.HTTP_204_NO_CONTENT
        )
    except OrderItem.DoesNotExist:
        return Response(
            {"message": "OrderItem không tồn tại"}, status=status.HTTP_404_NOT_FOUND
        )
