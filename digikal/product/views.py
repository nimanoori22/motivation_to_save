from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Product
from rest_framework import viewsets
from rest_framework import permissions, status
from .serializers import ProductSerializer, UserSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.contrib.auth import get_user_model
# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]



class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # queryset = Product.objects.filter(user=request.user)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        products = Product.objects.filter(user=user)
        return products

    def create(self, request, *args, **kwargs):
        product = Product(user=self.request.user)
        serializer = self.serializer_class(product, context={'request':request}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

