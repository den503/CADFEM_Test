from django.urls import path

from .views import DealsGetView

app_name = 'deals'

urlpatterns = [
    path('', DealsGetView.as_view(), name='index'),
]
