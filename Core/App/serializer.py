from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password' ]
    
    def validate(self,data):
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError({'error': 'User already exists with this username/email '})
            return data

    def create(self,validated_data):
        user=User.objects.create_user(username=validated_data['username'] , email=validated_data['email'],password=validated_data['password'])
        return validated_data
    

class VendorSerializer(serializers.ModelSerializer):
    
     class Meta:
          model = Vendor
          fields = '__all__'
    
     def create(self, validated_data):
          return super().create(validated_data)

     def update(self, instance, validated_data):
          return super().update(instance, validated_data)
    
class VendorPerformanceSerializer(serializers.ModelSerializer):
     
     class Meta:
          model = Vendor
          fields = ['on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate']

class PurchaseOrderSerializer(serializers.ModelSerializer):
     
     class Meta:
          model = PurchaseOrder
          fields= '__all__'

     def create(self, validated_data):
          return super().create(validated_data)
        
     def update(self, instance, validated_data):
          if 'status' in validated_data.keys():
               validated_data['delivery_date'] = datetime.now()
          return super().update(instance, validated_data)
     
