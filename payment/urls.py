from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('payments/', views.ListUserPayments.as_view(), name='list_user_payments'),
    path('payments/initiate/<int:order_id>/',
         views.InitiatePayment.as_view(), name='initiate_payment'),
    path('payments/update-status/<int:payment_id>/',
         views.UpdatePaymentStatus.as_view(), name='update_payment_status'),
    path('payments/create-checkout-session/',
         views.create_checkout_session, name='create_checkout_session'),
]
