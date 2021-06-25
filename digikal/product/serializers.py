from rest_framework import serializers
from django.contrib.auth.models import User
from . import models
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from .models import Product
# from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):

    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    email = serializers.EmailField()

    def validate_email(self, value):
        User = get_user_model()
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Duplicate")
        return lower_email

    class Meta:
        model = User(models.User)
        fields = ['url', 'id', 'email', 'products']



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['url', 'img', 'price', 
        'features', 'title']



