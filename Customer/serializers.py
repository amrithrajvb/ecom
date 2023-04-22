from rest_framework.serializers import ModelSerializer

from .models import MyUser,Product,Order,OrderItems
from rest_framework import serializers


class UserCreationSerializer(ModelSerializer):
    class Meta:
        model=MyUser
        fields=["email","role","password"]
    def create(self, validated_data):
        return MyUser.objects.create_user(email=validated_data["email"],
                                          role="customer",
                                          password=validated_data["password"])
    def update(self, instance, validated_data):
        return MyUser.objects.create_user(email=validated_data["email"],
                                          role="customer",
                                          password=validated_data["password"])


class AddProductSerializer(ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"


class AddOrdersSerializer(ModelSerializer):
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Order
        fields=["id","price","payment_method","order_status","user"]

class OrderItemSerializer(ModelSerializer):
    class Meta:
        model=OrderItems
        fields="__all__"