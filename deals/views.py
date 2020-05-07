from django.db.models import Sum, Max
from django.shortcuts import render
from django.views import View

from .forms import MainForm
from .models import DealStatus, Deal


def get_actual_status(request):
    actual_statuses = Deal.objects.filter(status__expected_deal_date__range=[request.POST['start_date'],
                                                                      request.POST['end_date']],
                                   status__stage__in=request.POST.getlist('deals_stages')).values('id'). \
        annotate(Max('status__created'))
    created = []
    for actual_status in actual_statuses:
        created.append(actual_status['status__created__max'])
    return created


class DealsGetView(View):
    def get(self, request):
        form = MainForm
        deals_message = 'Данные появятся после рассчета'
        note_list = 'Данные появятся после рассчета'
        return render(request, 'deals/index.html',
                      {'form': form, 'deals_message': deals_message, 'note_list': note_list})

    def post(self, request):
        form = MainForm(request.POST)
        created = get_actual_status(request)
        deals = DealStatus.objects.filter(expected_deal_date__range=[request.POST['start_date'],
                                                                     request.POST['end_date']],
                                          stage__in=request.POST.getlist('deals_stages'),
                                          created__in=created). \
            order_by('-stage__probability_of_success', '-expected_deal_date'). \
            select_related('deal', 'stage', 'deal__contact', 'deal__contact__company')

        note_list = {
            'RUB': deals.filter(stage__in=request.POST.getlist('deals_stages'), currency='RUB').\
                values('stage__name', 'stage__probability_of_success').annotate(Sum('summ')),
            'EUR': deals.filter(stage__in=request.POST.getlist('deals_stages'), currency='EUR').\
                values('stage__name', 'stage__probability_of_success').annotate(Sum('summ')),
            'USD': deals.filter(stage__in=request.POST.getlist('deals_stages'), currency='USD').\
                values('stage__name', 'stage__probability_of_success').annotate(Sum('summ')),
        }
        return render(request, 'deals/index.html', {'form': form, 'deals': deals, 'note_list': note_list})
