from django.urls import path
from .views import ListReviewsView, AddReviewView, DeleteReviewView

app_name = 'reviews'

urlpatterns = [
    path('list/<int:product_id>/', ListReviewsView.as_view(), name='list_reviews'),
    path('add/<int:product_id>/', AddReviewView.as_view(), name='add_review'),
    path('delete/<int:review_id>/',
         DeleteReviewView.as_view(), name='delete_review'),
]
