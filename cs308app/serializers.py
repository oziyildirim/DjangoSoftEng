from rest_framework import serializers
from .models import User, Product, Order, OrderItem, BasketItem, Comments, Category, Photos, Favourites, Address, ProductCategory,OrderAddressChange,CampaignInfo,Campaignitems,OrderCancel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name',
                  'email', 'verified', 'user_type','user_exists']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCancel
        fields = '__all__'


class CampaignInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignInfo
        fields = '__all__'


class CampaignitemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaignitems
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderAddressChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddressChange
        fields = '__all__'


class OrderItemStatusSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    class Meta:
        model = OrderItem
        fields = '__all__'
        


class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = '__all__'


class PhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
