from rest_framework import serializers
from .models import Car, Wishlist
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CarSerializer(serializers.ModelSerializer):
    is_wishlisted = serializers.SerializerMethodField()
    
    class Meta:
        model = Car
        fields = '__all__'
        
    def get_is_wishlisted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Wishlist.objects.filter(user=request.user, car=obj).exists()
        return False

class WishlistSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    
    class Meta:
        model = Wishlist
        fields = ('id', 'car', 'created_at') 