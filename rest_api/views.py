from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from .serializers import ProductSerializer
from base.models import Product
from rest_framework.response import Response

@api_view(['GET','POST'])
def api_products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


    


#for individual products
@api_view(['GET','PUT'])
def api_product(request,pk):
    product = get_object_or_404(Product,id=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    if request.method =='PUT':
        serializer = ProductSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)    
        return Response(serializer.data)


