from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler400, handler403, handler404, handler500
from django.http import JsonResponse

def custom_bad_request(request, exception=None):
    return JsonResponse({"error": "Bad Request"}, status=400)

handler400 = custom_bad_request

schema_view = get_schema_view(
   openapi.Info(
      title="SMM Analytic API",
      default_version='v1',
      description="SMM Analytic API — Ijtimoiy tarmoqlar bo‘yicha faoliyat yuritayotgan kanallarni markazlashgan tarzda boshqarish, ularning statistik ko‘rsatkichlarini yig‘ish, tahlil qilish va SMM xodimlarning ish samaradorligini kuzatish uchun mo‘ljallangan backend xizmatidir",
    #   terms_of_service="https://www.google.com/policies/terms/",
    #   contact=openapi.Contact(email="contact@snippets.local"),
    #   license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
