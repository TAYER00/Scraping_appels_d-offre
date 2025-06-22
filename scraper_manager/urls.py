from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from scrapers.api import TenderViewSet
from scrapers.views import TenderListView, TenderDetailView, StatisticsView, external_link_view

router = DefaultRouter()
router.register(r'tenders', TenderViewSet, basename='tender')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', TenderListView.as_view(), name='tender-list'),
    path('tender/<int:pk>/', TenderDetailView.as_view(), name='tender-detail'),
    path('statistics/', StatisticsView.as_view(), name='tender-statistics'),
    path('<path:path>', external_link_view, name='external-link'),
]
