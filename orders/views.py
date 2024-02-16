from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .models import Order
from .serializers import OrderSerializer
from django.shortcuts import get_object_or_404


class OrderListCreateAPIView(APIView):
    """
    List all orders for the logged-in user or create a new order.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    """
    Retrieve, update, or delete an order instance for the logged-in user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk, user=self.request.user)
        except Order.DoesNotExist:
            raise Http404("Order does not exist")

    def get(self, request, pk, *args, **kwargs):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        order = self.get_object(pk)
        serializer = OrderSerializer(
            order, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
