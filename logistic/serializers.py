from rest_framework import serializers
from rest_framework.serializers import Serializer

from logistic.models import StockProduct, Product, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for i in positions:
            new_stock_product = StockProduct.objects.create(product=i['product'], stock=stock, quantity=i['quantity'],
                                                            price=i['price'])
            stock.positions.add(new_stock_product)
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for i in positions:
            StockProduct.objects.update_or_create(defaults={'quantity': i['quantity'], 'price': i['price']},
                                                  product=i['product'], stock=stock)
        return stock

    class Meta:
        model = Stock
        fields = ["address", "positions"]
