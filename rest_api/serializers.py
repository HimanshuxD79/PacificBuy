from rest_framework import serializers
from base.models import Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields =['id','title','selling_price','discounted_price','description','brand','category','product_image']
