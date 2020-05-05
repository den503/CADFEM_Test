from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from .forms import MainForm
from .models import DealStatus


class DealsGetView(View):
    def get(self, request):
        form = MainForm
        deals_message = 'Данные появятся после рассчета'
        note_list = 'Данные появятся после рассчета'
        return render(request, 'deals/index.html',
                      {'form': form, 'deals_message': deals_message, 'note_list': note_list})

    def post(self, request):
        form = MainForm(request.POST)
        deals = DealStatus.objects.filter(expected_deal_date__range=[request.POST['start_date'],
                                                                     request.POST['end_date']],
                                          stage__in=request.POST.getlist('deals_stages')).\
            order_by('-stage__probability_of_success', '-expected_deal_date').\
            select_related('deal', 'stage', 'deal__contact', 'deal__contact__company')
        note_list = {
            'RUB': DealStatus.objects.filter(stage__in=request.POST.getlist('deals_stages'), currency='RUB').\
                values('stage__name', 'stage__probability_of_success').annotate(Sum('summ')),
            'EUR': DealStatus.objects.filter(stage__in=request.POST.getlist('deals_stages'), currency='EUR').\
                values('stage__name', 'stage__probability_of_success').annotate(Sum('summ')),
            'USD': DealStatus.objects.filter(stage__in=request.POST.getlist('deals_stages'), currency='USD').\
                values('stage__name', 'stage__probability_of_success').annotate(Sum('summ')),
        }
        return render(request, 'deals/index.html', {'form': form, 'deals': deals, 'note_list': note_list})
