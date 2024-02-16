from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import SupportTicket
import json


class CreateTicketView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            ticket = SupportTicket.objects.create(user=request.user, **data)
            return JsonResponse({"status": "success", "ticket_id": ticket.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)


class ListTicketsView(LoginRequiredMixin, View):
    def get(self, request):
        tickets = SupportTicket.objects.filter(user=request.user).values(
            'id', 'subject', 'status', 'created_at')
        return JsonResponse(list(tickets), safe=False)


class UpdateTicketStatusView(LoginRequiredMixin, View):
    def post(self, request, ticket_id):
        try:
            ticket = SupportTicket.objects.get(id=ticket_id, user=request.user)
            data = json.loads(request.body)
            ticket.status = data.get('status', ticket.status)
            ticket.save()
            return JsonResponse({"status": "success", "ticket_id": ticket.id, "new_status": ticket.status})
        except SupportTicket.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Ticket not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
