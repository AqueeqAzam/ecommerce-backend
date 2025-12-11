# views.py → ABSOLUTE FINAL PRODUCTION VERSION
from django.db.models import F
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import Product
from .serializers import ProductSerializer
from .pagination import GuestLimitedPagination


# ====================
# 1. Tiny admin check
# ====================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_admin(request):
    return Response({"is_admin": request.user.is_staff or request.user.is_superuser})


# ====================
# 2. List + Create (public read, admin only write)
# ====================
from rest_framework.pagination import PageNumberPagination

class ProductView(APIView):
    pagination_class = GuestLimitedPagination

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsAdminUser()]

    def get(self, request):
        queryset = Product.objects.active().select_related('category')

        # Search
        search = request.query_params.get('search')
        if search:
            queryset = queryset.search(search)

        # Multiple category filter → ?category=books&category=electronics
        category_slugs = request.query_params.getlist('category')
        if category_slugs:
            queryset = queryset.by_category(category_slugs)

        # Safe ordering
        ordering = request.query_params.get('ordering', '-created_at')
        allowed_ordering = [
            'price', '-price',
            'created_at', '-created_at',
            'name', '-name',
            'click_count', '-click_count',
        ]
        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-created_at')

        # ✅ Proper Pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)  # notice view=self
        serializer = ProductSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ====================
# 3. Detail – works with BOTH pk AND slug
# ====================
class ProductDetailView(APIView):
    def get(self, request, pk):  # renamed lookup_value → pk
        product = self.get_object(pk)  # still uses get_object
        Product.objects.filter(pk=product.pk).update(click_count=F('click_count') + 1)
        product.refresh_from_db(fields=['click_count'])
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, lookup_value):
        if isinstance(lookup_value, str) and len(lookup_value) > 10:
            return get_object_or_404(Product, slug=lookup_value, is_active=True)
        return get_object_or_404(Product, pk=lookup_value, is_active=True)

# ====================
# 4. Trending endpoint (your favorite, now perfect)
# ====================
class TrendingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            limit = int(request.query_params.get('limit', 10))
            limit = max(1, min(limit, 50))  # clamp 1–50
        except (TypeError, ValueError):
            limit = 10

        trending = (
            Product.objects
            .active()
            .select_related('category')
            .order_by('-click_count')[:limit]
        )

        serializer = ProductSerializer(trending, many=True, context={'request': request})
        return Response(serializer.data)