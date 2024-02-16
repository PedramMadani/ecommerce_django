from django.urls import path
from .views import ListCouponsView, ListBundlesView, ApplyCouponView

app_name = 'promotions'

urlpatterns = [
    path('coupons/', ListCouponsView.as_view(), name='list_coupons'),
    path('bundles/', ListBundlesView.as_view(), name='list_bundles'),
    path('apply-coupon/', ApplyCouponView.as_view(), name='apply_coupon'),
]
