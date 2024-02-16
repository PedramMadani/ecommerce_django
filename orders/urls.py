from django.urls import path
from .views import OrderListCreateAPIView, OrderDetailAPIView

app_name = 'orders'

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
]
