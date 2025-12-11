from django.urls import path
from .views import (
    ProductDetailView,
    TrendingView,
    ProductView
)

urlpatterns = [
    # 🔥 Static routes first
    path('trending/', TrendingView.as_view(), name='trending-products'),

    # 🛍 Get all or create product
    path('', ProductView.as_view(), name='product-list-create'),

    # 🔍 Single product detail (edit/delete allowed for admin)
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]
