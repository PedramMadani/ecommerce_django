from django.urls import path
from .views import ListSettingsView, UpdateSettingView

app_name = 'config'

urlpatterns = [
    path('settings/', ListSettingsView.as_view(), name='list_settings'),
    path('settings/update/', UpdateSettingView.as_view(), name='update_setting'),
]
