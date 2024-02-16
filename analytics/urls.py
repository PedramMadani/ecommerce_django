from django.urls import path
from .views import RecordProductView, ListUserActivities, RecordUserActivity

app_name = 'analytics'

urlpatterns = [
    path('record-product-view/<int:product_id>/',
         RecordProductView.as_view(), name='record_product_view'),
    path('list-user-activities/', ListUserActivities.as_view(),
         name='list_user_activities'),
    path('record-user-activity/', RecordUserActivity.as_view(),
         name='record_user_activity'),
]
