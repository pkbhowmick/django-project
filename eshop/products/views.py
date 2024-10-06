from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from .serializers import ProductSerializers
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .permissions import IsAdmin, IsStaff
from rest_framework.permissions import IsAuthenticated


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the product index.")

class ProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Override get_permissions to apply custom permissions based on request method.
        """
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdmin()]
        elif self.request.method == 'POST':
            return [IsStaff()]
        return super().get_permissions()
    
    def post(self, request):
        serializer = ProductSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ### get all products
    ## 200 - OK, 401 - Skip, 500 - server error
    def get(self, request, id=None):
        if id:
            try:
                product = Product.objects.get(id=id)
            except Product.DoesNotExist:
                raise Http404
            serializer = ProductSerializers(product)
            return Response(serializer.data)
        else:
            products = Product.objects.all()
            serializer = ProductSerializers(products, many=True)
            return Response(serializer.data)
    
    def put(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404
        serializer = ProductSerializers(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404
        
        product.delete()
        serializer = ProductSerializers(product)
        return Response(serializer.data)

    def patch(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404
        serializer = ProductSerializers(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)