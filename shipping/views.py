from django.http import JsonResponse
from django.views.generic import ListView
from .models import ShippingOption
from django.views import View


class ListShippingOptionsView(ListView):
    model = ShippingOption

    def render_to_response(self, context, **response_kwargs):
        options = context['object_list'].values(
            'id', 'name', 'cost', 'duration')
        return JsonResponse(list(options), safe=False)


class CalculateShippingCostView(View):
    def get(self, request, option_id, order_id):
        shipping_option = get_object_or_404(ShippingOption, id=option_id)
        # Simulated cost calculation
        cost = shipping_option.cost
        return JsonResponse({"shipping_option": shipping_option.name, "cost": cost})
