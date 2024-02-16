from django.urls import path
from .views import ListProductsView, ProductDetailView, CreateProductView, UpdateProductView, DeleteProductView

app_name = 'products'

urlpatterns = [
    path('list/', ListProductsView.as_view(), name='list_products'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', CreateProductView.as_view(), name='create_product'),
    path('update/<int:pk>/', UpdateProductView.as_view(), name='update_product'),
    path('delete/<int:pk>/', DeleteProductView.as_view(), name='delete_product'),
]
