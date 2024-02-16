from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import stripe
from django.conf import settings

from .models import Payment, Order

# Ensure Stripe's API key is securely configured
stripe.api_key = settings.STRIPE_SECRET_KEY


class ListUserPayments(LoginRequiredMixin, View):
    """
    List all payments made by the logged-in user.
    """

    def get(self, request):
        payments = Payment.objects.filter(order__user=request.user).values(
            'id', 'amount', 'payment_method', 'status', 'created_at')
        return JsonResponse(list(payments), safe=False)


class InitiatePayment(LoginRequiredMixin, View):
    """
    Initiate a payment process for an order.
    """
    @method_decorator(csrf_exempt)
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        data = json.loads(request.body)

        # Here, integrate with Stripe or another payment service securely
        # For demonstration, we're directly creating the payment record
        payment = Payment.objects.create(
            order=order,
            amount=data.get('amount'),
            payment_method=data.get(
                'payment_method', 'Stripe'),  # Default to Stripe
            # Generate or obtain from payment service
            transaction_id=data.get('transaction_id', ''),
            status=Payment.Status.PENDING  # Initially, all payments are pending
        )

        return JsonResponse({"status": "success", "payment_id": payment.id, "order_id": order_id})


class UpdatePaymentStatus(LoginRequiredMixin, View):
    """
    Securely update the status of an existing payment.
    """
    @method_decorator(csrf_exempt)
    def post(self, request, payment_id):
        payment = get_object_or_404(
            Payment, id=payment_id, order__user=request.user)
        data = json.loads(request.body)
        # Safely default to PENDING
        payment.status = data.get('status', Payment.Status.PENDING)
        payment.save()

        return JsonResponse({"status": "success", "payment_id": payment.id, "new_status": payment.status})


def create_checkout_session(request):
    """
    Create a Stripe checkout session for a payment.
    """
    # Ensure this endpoint is protected by authentication
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=403)

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'T-shirt',  # Example product name
                    },
                    'unit_amount': 2000,  # Example amount ($20.00)
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/') + '?success=true',
            cancel_url=request.build_absolute_uri('/') + '?canceled=true',
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
