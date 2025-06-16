from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from scrapers.api import TenderViewSet

router = DefaultRouter()
router.register(r'tenders', TenderViewSet, basename='tender')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
