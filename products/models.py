# models.py → FINAL 100% PRODUCTION-READY (copy-paste this exact file)
import os
from .managers import ProductManager   # ← THIS LINE WAS MISSING
from django.db import models, transaction, IntegrityError
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db.models import F
from django.db import models

User = get_user_model()


def validate_image_size(value):
    limit_mb = 5
    if value.size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Image size cannot exceed {limit_mb} MB.")


def validate_file_size(value):
    limit_mb = 500
    # You can lower this later (e.g. 100 MB) when you go to S3
    if value.size > limit_mb * 1024 * 1024:
        raise ValidationError(f"File size cannot exceed {limit_mb} MB.")


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, db_index=True)

    class Meta:
        verbose_name_plural = "Categories"
        indexes = [models.Index(fields=['slug'])]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True)
    slug = models.SlugField(max_length=300, unique=True, editable=False, db_index=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="products",
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(999999999.99)],
    )
    stock = models.PositiveIntegerField(default=1)

    is_active = models.BooleanField(default=True, db_index=True)

    thumbnail = models.ImageField(
        upload_to="products/thumbnails/%Y/%m/%d/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png", "webp", "JPG", "JPEG", "PNG", "WEBP"]),
            validate_image_size,
        ],
    )
    file = models.FileField(
        upload_to="products/files/%Y/%m/%d/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(["pdf", "zip", "mp4", "mp3", "rar", "PDF", "ZIP", "MP4", "MP3", "RAR"]),
            validate_file_size,
        ],
    )

    click_count = models.PositiveBigIntegerField(default=0, db_index=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # YOUR CUSTOM MANAGER
    objects = ProductManager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["price"]),
            models.Index(fields=["click_count"]),
            models.Index(fields=["category"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while True:
                try:
                    with transaction.atomic():
                        if not Product.objects.filter(slug=slug).exists():
                            self.slug = slug
                            break
                        if counter > 10000:
                            raise ValidationError("Unable to generate unique slug.")
                        slug = f"{base_slug}-{counter}"
                        counter += 1
                except IntegrityError:
                    continue  # retry

        super().save(*args, **kwargs)

    # BETTER: use manager method instead of instance method
    # → removed increment_click_count() here (see note below)