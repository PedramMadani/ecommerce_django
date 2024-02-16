from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Review, Product
from django.shortcuts import get_object_or_404
import json


class ListReviewsView(View):
    def get(self, request, product_id):
        reviews = Review.objects.filter(product_id=product_id).values(
            'id', 'user__username', 'content', 'rating', 'created_at')
        return JsonResponse(list(reviews), safe=False)


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        try:
            data = json.loads(request.body)
            product = get_object_or_404(Product, id=product_id)
            review = Review.objects.create(
                user=request.user, product=product, **data)
            return JsonResponse({"status": "success", "review_id": review.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)


class DeleteReviewView(LoginRequiredMixin, View):
    def delete(self, request, review_id):
        try:
            review = get_object_or_404(Review, id=review_id, user=request.user)
            review.delete()
            return JsonResponse({"status": "success", "message": "Review deleted"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
