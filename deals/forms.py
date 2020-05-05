from django import forms
from datetime import datetime, date
import math

from .models import DealStage


def get_start_date():
    start_quarter = date(1, 1, 1)
    current_date = datetime.now()
    quarter = math.ceil(current_date.month / 3.)
    if quarter == 1:
        start_quarter = date(current_date.year, 1, 1)
    elif quarter == 2:
        start_quarter = date(current_date.year, 4, 1)
    elif quarter == 3:
        start_quarter = date(current_date.year, 7, 1)
    elif quarter == 4:
        start_quarter = date(current_date.year, 10, 1)
    return start_quarter


def get_end_date():
    end_quarter = date(1, 1, 1)
    current_date = datetime.now()
    quarter = math.ceil(current_date.month / 3.)
    if quarter == 1:
        end_quarter = date(current_date.year, 3, 31)
    elif quarter == 2:
        end_quarter = date(current_date.year, 6, 30)
    elif quarter == 3:
        end_quarter = date(current_date.year, 9, 30)
    elif quarter == 4:
        end_quarter = date(current_date.year, 12, 31)
    return end_quarter


def get_choices():
    stages = []
    for stage in DealStage.objects.all().order_by('-probability_of_success'):
        stage_object = [stage.id, stage.name + ' ' + str(stage.probability_of_success) + '%']
        stages.append(stage_object)
    return stages


def get_initial():
    initial = []
    for stage in DealStage.objects.filter(probability_of_success__gt=30):
        initial.append(stage.id)
    return initial


class MainForm(forms.Form):
    start_date = forms.DateField(label='Дата начала отбора',
                                 widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                 initial=get_start_date().strftime("%Y-%m-%d"))
    end_date = forms.DateField(label='Дата конца отбора',
                               widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                               initial=get_end_date().strftime("%Y-%m-%d"))
    deals_stages = forms.MultipleChoiceField(label='Стадии сделок',
                                             choices=get_choices(),
                                             initial=get_initial(),
                                             widget=forms.SelectMultiple(attrs={'class': 'custom-select'}))
