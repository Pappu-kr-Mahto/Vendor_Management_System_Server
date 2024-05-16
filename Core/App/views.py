from django.shortcuts import HttpResponse
from .serializer import * 
from django.contrib.auth import authenticate

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
# from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from datetime import datetime
from drf_spectacular.utils import extend_schema
# Create your views here.

def home(request):
    return HttpResponse("<h1> Vendor Management System : Server is running.</h1> \\n For testing the API's visit (/api/schema/swagger/)")

@extend_schema(
        request=UserSerializer,
        responses={201: None},
        description="Enter the username, email and password to create an account."
    )
@api_view(['POST'])
def signup(request):
    try:
        print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"Account Created successfully","username":request.data['username'],"email":request.data['email']},status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":'Internal server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
        request=LoginSerializer,
        responses={200: None},
        description="Enter the email and password for login. And do Authorization with the 'access key' given in response body in login."
    )
@api_view(['POST'])
def login(request):
    try:
        email= request.data.get('email')
        password = request.data.get('password')
        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email).first()
        if user is not None:
            temp = authenticate(username=user.username, password=password)
            if temp is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                        'user':email,
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    })
        return Response({"error":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({"error":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)


class VendorsViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','post','put','delete']

    def list(self, request):
        queryset = Vendor.objects.all()
        serializer = self.serializer_class(queryset,many=True)
        return Response({'success': serializer.data},status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': serializer.validated_data})
        else:
            return Response({'error': serializer.errors})
                
    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response({'success': serializer.data},status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'error':serializer.errors},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success': "Succssfully Deleted.."},status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["get"], url_path=r'performance')
    def performance(self, request, pk=None):
        instance = self.get_object()
        serializer = VendorPerformanceSerializer(instance)
        return Response({'success':serializer.data},status=status.HTTP_200_OK)
    

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','post','put','delete']

    def list(self, request):
        vendor_param = request.GET.get('vendor')
        if vendor_param:
            queryset = PurchaseOrder.objects.filter(vendor = vendor_param)
            serializer = self.serializer_class(queryset,many=True)
            return Response({'success': serializer.data},status=status.HTTP_200_OK)
        else:
            queryset = PurchaseOrder.objects.all()
            serializer = self.serializer_class(queryset,many=True)
            return Response({'success': serializer.data},status=status.HTTP_200_OK)

    @extend_schema(
        responses={201: None},
        description=" Enter the item names and quantity and the vendor id"
    )
    def create(self, request):
        try:
            serializer = self.serializer_class(data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'success':'Purchase Order placed successfully'},status=status.HTTP_201_CREATED)
            else:
                return Response({'error':serializer.errors},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error":'Internal server error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response({'success': serializer.data},status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'error',serializer.errors},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success': 'Succssfully Deleted.'},status=status.HTTP_200_OK)
    
    @extend_schema(
        responses={200: None},
        description="Only Enter the expected date of delivery."
    )
    @action(detail=True, methods=["POST"], url_path=r'acknowledge')
    def acknowledge(self, request, pk=None):
        instance = self.get_object()
        data = request.data
        if 'expected_delivery_date' not in data.keys():
            return Response({'error':'Please provide the expected date of delivery'})
        else:
            instance.acknowledgement_date = datetime.now()
            instance.expected_delivery_date = data['expected_delivery_date']
            instance.save()
            return Response({'success':"Purchase order is acknowledge successfully"})
    