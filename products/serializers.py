from rest_framework import serializers
from django.templatetags.static import static
from django.utils.html import format_html
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    """Simple read-only category serializer (used nested in Product)"""
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
        read_only_fields = ["id", "name", "slug"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    # Public absolute URLs (work with Django storage backends – local, S3, etc.)
    thumbnail_url = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    
    # Legacy alias for frontends that expect "image" field
    image = serializers.SerializerMethodField()

    # Optional trending field – you can remove if you don't want to expose raw clicks
    trending_score = serializers.ReadOnlyField(source="click_count")

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "description",
            "price",
            "stock",
            "is_active",
            "thumbnail",
            "thumbnail_url",
            "image",           # alias
            "file",
            "file_url",
            "click_count",
            "trending_score",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "slug",
            "thumbnail_url",
            "file_url",
            "image",
            "click_count",
            "trending_score",
            "created_at",
            "updated_at",
        ]
        # If you ever allow PATCH/PUT from trusted sources (admin API), you can open these:
        extra_kwargs = {
            "thumbnail": {"write_only": True, "required": False},
            "file": {"write_only": True, "required": False},
        }

    # ------------------------------------------------------------------
    # URL Methods – safe for any storage backend (local, S3, GCS, etc.)
    # ------------------------------------------------------------------
    def get_thumbnail_url(self, obj) -> str | None:
        if not obj.thumbnail:
            # Optional: return a nice placeholder instead of None
            return self._placeholder_url("images/placeholder-product.svg")
        request = self.context.get("request")
        return request.build_absolute_uri(obj.thumbnail.url) if request else obj.thumbnail.url

    def get_file_url(self, obj) -> str | None:
        if not obj.file:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(obj.file.url) if request else obj.file.url

    def get_image(self, obj):
        """Keeps backward compatibility with frontends expecting 'image'"""
        return self.get_thumbnail_url(obj)

    # ------------------------------------------------------------------
    # Helper for placeholder (optional but highly recommended)
    # ------------------------------------------------------------------
    def _placeholder_url(self, path: str) -> str:
        request = self.context.get("request")
        placeholder = static(path)
        return request.build_absolute_uri(placeholder) if request else placeholder