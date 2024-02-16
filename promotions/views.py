from django.http import JsonResponse
from django.views.generic import View
from django.utils import timezone
from .models import Coupon, Bundle
from orders.models import Order
from django.contrib.auth.mixins import LoginRequiredMixin
import json


class ListCouponsView(View):
    """
    List all active coupons.
    """

    def get(self, request):
        now = timezone.now()
        coupons = Coupon.objects.filter(valid_from__lte=now, valid_to__gte=now, active=True).values(
            'code', 'discount', 'valid_from', 'valid_to')
        return JsonResponse(list(coupons), safe=False)


class ListBundlesView(View):
    """
    List all available bundles.
    """

    def get(self, request):
        bundles = Bundle.objects.filter(validity_period__gte=timezone.now()).values(
            'name', 'price', 'discount_rate', 'validity_period')
        return JsonResponse(list(bundles), safe=False)


class ApplyCouponView(LoginRequiredMixin, View):
    """
    Apply a coupon to the user's order. Assumes coupon can be applied directly to the order total.
    """

    def post(self, request):
        try:
            data = json.loads(request.body)
            coupon_code = data.get('coupon_code')
            order_id = data.get('order_id')

            # Validate the coupon
            now = timezone.now()
            coupon = get_object_or_404(
                Coupon, code=coupon_code, valid_from__lte=now, valid_to__gte=now, active=True)

            # Validate the order
            order = get_object_or_404(Order, id=order_id, user=request.user)

            # Check if the coupon has already been applied
            if order.coupon:
                return JsonResponse({"status": "error", "message": "A coupon has already been applied to this order."}, status=400)

            # Assuming Order model has method to apply discount and calculate final price
            success_message, new_total = order.apply_coupon(coupon)

            return JsonResponse({"status": "success", "message": success_message, "new_total": new_total})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
