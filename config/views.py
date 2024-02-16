from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import SiteSetting
import json


class ListSettingsView(View):
    """
    A view to list all site settings in JSON format.
    """

    def get(self, request, *args, **kwargs):
        settings = SiteSetting.objects.all()
        settings_data = {setting.key: setting.get_value()
                         for setting in settings}
        return JsonResponse(settings_data)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateSettingView(View):
    """
    A view to update a specific site setting identified by a key in the request.
    """

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            key = data.get('key')
            value = data.get('value')
            setting = SiteSetting.objects.get(key=key)
            setting.value = value
            setting.save()
            return JsonResponse({"status": "success", "key": key, "value": value})
        except SiteSetting.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Setting not found"}, status=404)
        except Exception as e:
            # Consider logging the exception e here for debugging purposes
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
