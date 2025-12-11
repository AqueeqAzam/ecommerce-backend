# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from products.views import check_admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # App Routes
    path('products/', include('products.urls')),
    
    path('orders/', include('orders.urls')),

    # Admin Permission Check
    path('api/auth/check-admin/', check_admin, name='check-admin'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
