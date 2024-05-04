from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'vendors',views.VendorsViewSet,basename="vendors")
router.register(r'purchase_orders',views.PurchaseOrderViewSet,basename="purchase_orders")


urlpatterns = [
    path('', views.home,name='home'),

    path('api/signup/',views.signup,name="signup"),
    path('api/login/',views.login,name="login"),

    path('api/',include(router.urls)),
]