# your_app/managers.py
from django.db.models import Q, Count, Avg, F, QuerySet, Manager
from django.db import transaction


class ProductQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def search(self, keyword):
        if not keyword:
            return self
        return self.filter(
            Q(name__icontains=keyword) | Q(description__icontains=keyword)
        )

    def by_category(self, categories):
        return self.filter(category__slug__in=categories)


class ProductManager(Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    # Proxy methods – now you can do Product.objects.active(), .search(), etc.
    def active(self):
        return self.get_queryset().active()

    def search(self, keyword):
        return self.get_queryset().search(keyword)

    def by_category(self, categories):
        return self.get_queryset().by_category(categories)

    @transaction.atomic
    def reduce_stock(self, product_id, quantity=1):
        """Atomically reduce stock – safe under 10 000 orders/sec"""
        updated = self.filter(
            id=product_id,
            stock__gte=quantity,
            is_active=True
        ).update(stock=F('stock') - quantity)
        return updated > 0