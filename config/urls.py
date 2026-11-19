from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
import os

def serve_frontend(request):
    """Serve Vue.js frontend index.html"""
    index_path = settings.BASE_DIR / 'frontend' / 'dist' / 'index.html'
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            return HttpResponse(f.read(), content_type='text/html')
    return HttpResponse("Frontend not built. Run: cd frontend && npm run build", status=503)

def serve_asset(request, path):
    """Serve static assets from frontend/dist/assets"""
    asset_path = settings.BASE_DIR / 'frontend' / 'dist' / 'assets' / path
    if asset_path.exists():
        return FileResponse(asset_path)
    return HttpResponse("Asset not found", status=404)

def serve_root_file(request, filename):
    """Serve root-level files from frontend/dist (favicon.svg, etc.)"""
    # Only serve specific known files
    allowed_files = ['favicon.svg', 'icons.svg', 'no-image.svg']
    if filename not in allowed_files:
        return HttpResponse("File not found", status=404)
    file_path = settings.BASE_DIR / 'frontend' / 'dist' / filename
    if file_path.exists():
        return FileResponse(file_path)
    return HttpResponse("File not found", status=404)

urlpatterns = [
    # Frontend assets (CSS, JS, etc.)
    path('assets/<path:path>', serve_asset, name='frontend-assets'),

    # Root-level files (favicon, icons, etc.)
    path('favicon.svg', serve_root_file, name='frontend-favicon'),
    path('icons.svg', serve_root_file, name='frontend-icons'),
    path('no-image.svg', serve_root_file, name='frontend-no-image'),

    # Frontend (Vue.js SPA)
    path('', serve_frontend, name='frontend'),

    # Django built-in admin (baza boshqaruvi)
    path('django-admin/', admin.site.urls),

    # API v1
    path('api/', include('main.urls')),

    # OpenAPI / Swagger dokumentatsiya
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
