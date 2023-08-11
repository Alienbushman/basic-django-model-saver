from django.conf import settings
from django.urls import path

from .views import ModelUsedView, PredictionView

urlpatterns = [
    path('models/', ModelUsedView.as_view()),
    path('predictions/', PredictionView.as_view())
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
