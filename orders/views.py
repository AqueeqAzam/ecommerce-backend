# orders/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Order
from .serializers import OrderSerializer


class OrderCreateView(APIView):
    permission_classes = [AllowAny]  # No login required

    def post(self, request):
        # Accept FormData (with image)
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            # Optional: Change status after you verify screenshot
            # order.status = 'payment_done'
            # order.save()

            return Response({
                "message": "Order placed successfully! We will confirm after checking ₹5 payment.",
                "order_number": order.order_number,
                "total": str(order.total_amount),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    permission_classes = [AllowAny]  # Public order tracking

    def get(self, request, order_number):
        order = Order.objects.get(order_number=order_number)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    

class MyOrdersListView(APIView):
    permission_classes = [IsAuthenticated]  # Must be logged in

    def get(self, request):
        # We identify user by mobile number (since you don't use email/password login yet)
        mobile = request.user.mobile  # assuming you attach mobile to user on login
        # OR if you're using session/phone login, maybe: mobile = request.session.get('mobile')

        orders = Order.objects.filter(mobile=mobile).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)