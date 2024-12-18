from rest_framework import serializers
from .models import Customer, Ticket, Seller, Order

# Customer Serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'  # Якщо хочете вибрати конкретні поля, замініть '__all__' на список полів, наприклад: ['id', 'name', 'email']

# Ticket Serializer
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

# Seller Serializer
class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())
    seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all())

    class Meta:
        model = Order
        fields = ['id', 'customer', 'ticket', 'seller', 'order_date']
