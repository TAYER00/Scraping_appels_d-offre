from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count
from django.shortcuts import render
import json
import os
from .models import Tender
from .services import TenderService

class TenderListView(TemplateView):
    template_name = 'scrapers/tender_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        json_path = os.path.join('data', 'consolidated', 'tenders.json')
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                tenders_data = json.load(f)
            
            # Get filter parameters from request
            search_query = self.request.GET.get('search', '')
            site_filter = self.request.GET.get('site', '')
            date_filter = self.request.GET.get('date', '')
            
            # Apply filters if needed
            if search_query or site_filter or date_filter:
                filtered_data = {}
                for source, tenders in tenders_data.items():
                    if site_filter and source.lower() != site_filter.lower():
                        continue
                        
                    filtered_tenders = []
                    for tender in tenders:
                        if search_query and search_query.lower() not in tender['objet'].lower():
                            continue
                        if date_filter and date_filter not in tender.get('date_limite', ''):
                            continue
                        filtered_tenders.append(tender)
                        
                    if filtered_tenders:
                        filtered_data[source] = filtered_tenders
                        
                tenders_data = filtered_data
            
            context['tenders_data'] = tenders_data
            context['sites'] = list(tenders_data.keys())
            
        except Exception as e:
            context['error'] = str(e)
            context['tenders_data'] = {}
            context['sites'] = []
            
        return context

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

def consolidated_tenders_view(request):
    json_path = os.path.join('data', 'consolidated', 'tenders.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            tenders_data = json.load(f)
        return render(request, 'scrapers/index.html', {'tenders_data': tenders_data})
    except Exception as e:
        return render(request, 'scrapers/index.html', {'error': str(e), 'tenders_data': {}})

from django.shortcuts import redirect

def external_link_view(request, path):
    """Redirect to external tender links while preserving the full URL path."""
    return redirect(f"http://{path}")
