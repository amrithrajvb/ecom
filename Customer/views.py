from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ViewSet

from .models import MyUser,Product,Order,OrderItems
from .serializers import UserCreationSerializer,AddProductSerializer,AddOrdersSerializer,OrderItemSerializer
from rest_framework import mixins,generics
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# Create your views here.
import datetime
from django.db.models import Q
from dateutil.relativedelta import relativedelta

class UserCreationView(ViewSet):
    model=MyUser
    serializer_class = UserCreationSerializer
    # permission_classes = [IsAuthenticated]

    def create(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=self.model.objects.get(id=request.user.id)
        serializer=self.serializer_class(qs,many=False)
        return Response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        qs = self.model.objects.get(id=request.user.id)
        serializer = self.serializer_class(instance=qs,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
           return Response(data=serializer.errors)

    def destroy(self,request,*args,**kwargs):
        qs = self.model.objects.get(id=request.user.id).delete()
        return Response(data="deleted")

class ProductAddView(ViewSet):
    model = Product
    serializer_class = AddProductSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def list(self,request,*args,**kwargs):
        today = datetime.date.today()
        two_m_ago = today - relativedelta(months=2)
        print(two_m_ago)
        # qs1_date=qs1.date
        # if ((two_m_ago==qs1_date) or (qs1_date >=two_m_ago)):
        #     qs1.status="inactive"
        #     qs1.save()


        qs=self.model.objects.filter(status="Active")
        serializer=self.serializer_class(qs,many=True,initial=request.data)
        print("date",serializer.data)

        for i in serializer.data:
            print(i["date"])

            if ((two_m_ago == i["date"])):
                print("pass")
                i["status"]="inactive"


        return Response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        print("id",id)
        qs = self.model.objects.get(id=id)
        user=qs.user
        if user==request.user:
            serializer = self.serializer_class(instance=qs, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        else:
            return Response({"message":"you are not allowed to update"})
        # print("qss",qs.user)


class OrderView(ViewSet):
    model=Order
    serializer_class = AddOrdersSerializer
    queryset = Order.objects.all()

    # def get_queryset(self):
    #     return self.model.objects.filter(user=self.request.user)

    def list(self,request,*args,**kwargs):
        order_serializer = AddOrdersSerializer(Order.objects.filter(user=request.user),many=True)
        print("orders",order_serializer.data)
        for order in order_serializer.data:

            orderitem_queryset=OrderItems.objects.filter(order_id=order['id'])

            order_item_serializer = OrderItemSerializer(orderitem_queryset,many=True)
            for product in order_item_serializer.data:
                products = Product.objects.filter(id=product["product"],user=request.user.id)
                product_serializer=AddProductSerializer(products,many=True)
                print("data",product_serializer.data)
                # products["myorders"]=product_serializer.data
            order['orderitems'] = order_item_serializer.data
        return Response({
            'response_code': 200,
            'status': 'Ok',
            'orders': order_serializer.data
        })



    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # order = {}
            data = request.data
            # data['id'] = self.request.user.id
            # order['user'] = data['user']
            # order['payment_method'] = data['payment_method']
            # order['price'] = data['price']
            # # order['discount'] = data['discount']
            # # order['final_amount'] = data['final_amount']
            # order['order_status'] = 'failed'
            # # order['ordered_on'] = datetime.now().date()
            # print(order)
            print(data)
            order_serializer = AddOrdersSerializer(data=data)
            print("hai",order_serializer)
            if order_serializer.is_valid():
                order_serializer_data = order_serializer.save(user=self.request.user)
                print("error",order_serializer_data)
                order_id = order_serializer_data.id
                for product in data['products']:
                    product['order'] = order_id

                    order_item_serializer = OrderItemSerializer(data=product)
                    if order_item_serializer.is_valid():
                        order_item_serializer.save()
                return Response({
                    'response_code': 200,
                    'status': 'Ok',
                    'message': 'Order Completed'
                })
            return Response({
                'response_code': 400,
                'status': 'Bad request',
                'message': 'Order Failed'
            }, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message":"sorry you don't have the permission "},status=status.HTTP_400_BAD_REQUEST)





