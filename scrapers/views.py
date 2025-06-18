from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count
from .models import Tender
from .services import TenderService

class TenderListView(ListView):
    model = Tender
    template_name = 'scrapers/tender_list.html'
    context_object_name = 'tenders'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get unique sites for the filter dropdown
        context['sites'] = Tender.objects.values_list('site', flat=True).distinct()
        return context

    def get_queryset(self):
        # Import latest data before displaying
        TenderService.import_from_json()
        queryset = super().get_queryset()

        # Get filter parameters from request
        search_query = self.request.GET.get('search', '')
        site_filter = self.request.GET.get('site', '')
        date_filter = self.request.GET.get('date', '')

        # Apply filters
        if search_query:
            queryset = queryset.filter(objet__icontains=search_query)
        if site_filter:
            queryset = queryset.filter(site=site_filter)
        if date_filter:
            queryset = queryset.filter(date_limite=date_filter)

        return queryset

class TenderDetailView(DetailView):
    model = Tender
    template_name = 'scrapers/tender_detail.html'
    context_object_name = 'tender'

class StatisticsView(TemplateView):
    template_name = 'scrapers/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = TenderService.get_statistics()
        return context
