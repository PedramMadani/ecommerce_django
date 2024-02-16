from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),

    # JWT Auth URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App-specific URLs
    path('api/accounts/', include('accounts.urls', namespace='accounts')),
    path('api/analytics/', include('analytics.urls', namespace='analytics')),
    path('api/config/', include('config.urls', namespace='config')),
    path('api/orders/', include('orders.urls', namespace='orders')),
    path('api/payment/', include('payment.urls', namespace='payment')),
    path('api/products/', include('products.urls', namespace='products')),
    path('api/promotions/', include('promotions.urls', namespace='promotions')),
    path('api/reviews/', include('reviews.urls', namespace='reviews')),
    path('api/shipping/', include('shipping.urls', namespace='shipping')),
    path('api/support/', include('support.urls', namespace='support')),

]

# Optional: Serve static files in development

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
