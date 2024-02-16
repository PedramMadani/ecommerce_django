from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Product
import json


class ListProductsView(ListView):
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(available=True)

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(list(context['products'].values('id', 'name', 'price', 'stock')), safe=False)


class ProductDetailView(DetailView):
    model = Product

    def render_to_response(self, context, **response_kwargs):
        product = context['object']
        product_data = {
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock,
        }
        return JsonResponse(product_data)


@method_decorator(csrf_exempt, name='dispatch')
class CreateProductView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'stock', 'category']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        product = Product.objects.create(**data)
        return JsonResponse({"status": "success", "product_id": product.id})


@method_decorator(csrf_exempt, name='dispatch')
class UpdateProductView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'stock', 'category']

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return JsonResponse({"status": "success", "product_id": product.id})


@method_decorator(csrf_exempt, name='dispatch')
class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Product

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return JsonResponse({"status": "success", "message": "Product deleted"})

# The update_inventory_on_order function and related functions can be part of a signals.py or utils.py,
# triggered by signals after order creation or update.
