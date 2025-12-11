from django.urls import path
from .views import OrderCreateView, OrderDetailView, MyOrdersListView

urlpatterns = [
    path('', OrderCreateView.as_view(), name='order-create'),  # POST /orders/
    path('<str:order_number>/', OrderDetailView.as_view(), name='order-detail'),  # For admin
    path('list/', MyOrdersListView.as_view(), name='my-orders'),  # For admin
]
