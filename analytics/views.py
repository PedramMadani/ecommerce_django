# Django imports
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Local application imports
from .models import ProductView, UserActivity
from products.models import Product


class RecordProductView(View):
    """
    Records a view of a product identified by product_id.
    """

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        ProductView.objects.create(
            product=product,
            ip_address=request.META.get('REMOTE_ADDR'),
            session=request.session.session_key
        )
        return JsonResponse({"status": "success"})


class ListUserActivities(LoginRequiredMixin, View):
    """
    Lists activities for the logged-in user, ordered by timestamp.
    """

    def get(self, request):
        activities = UserActivity.objects.filter(
            user=request.user).order_by('-timestamp')
        activities_data = [{"action": activity.action,
                            "timestamp": activity.timestamp} for activity in activities]
        return JsonResponse({"activities": activities_data})


class RecordUserActivity(View):
    """
    Class-based view to record user activities. Requires user to be authenticated.
    """
    @method_decorator(login_required)
    def post(self, request):
        # Provide a default to avoid None
        action = request.POST.get('action', '')
        # Provide a default to avoid None
        details = request.POST.get('details', '')
        if not action:
            return JsonResponse({"error": "Action must be provided."}, status=400)
        UserActivity.objects.create(
            user=request.user, action=action, details=details)
        return JsonResponse({"status": "success"})
