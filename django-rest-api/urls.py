from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Helm CRUD Django",
        default_version='v1',
        description="A basic crud app that shows what different URLS do",
    ),
    public=True,
)

urlpatterns = [
    # a basic swagger view
    path('', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc'), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('dummy_predictions_model/', include('dummy_predictions_model.urls'))


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
