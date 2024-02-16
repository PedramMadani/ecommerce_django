from django.urls import path
from .views import CreateTicketView, ListTicketsView, UpdateTicketStatusView

app_name = 'support'

urlpatterns = [
    path('create/', CreateTicketView.as_view(), name='create_ticket'),
    path('list/', ListTicketsView.as_view(), name='list_tickets'),
    path('update-status/<int:ticket_id>/',
         UpdateTicketStatusView.as_view(), name='update_ticket_status'),
]
