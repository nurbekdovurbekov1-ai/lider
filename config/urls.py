from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def serve_frontend(request):
    """Serve Vue.js frontend index.html"""
    index_path = settings.BASE_DIR / 'frontend' / 'dist' / 'index.html'
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            return HttpResponse(f.read(), content_type='text/html')
    return HttpResponse("Frontend not built. Run: cd frontend && npm run build", status=503)

urlpatterns = [
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
