from django.urls import path
from .views import ListShippingOptionsView, CalculateShippingCostView

app_name = 'shipping'

urlpatterns = [
    path('options/', ListShippingOptionsView.as_view(),
         name='list_shipping_options'),
    path('calculate/<int:option_id>/<int:order_id>/',
         CalculateShippingCostView.as_view(), name='calculate_shipping_cost'),
]
