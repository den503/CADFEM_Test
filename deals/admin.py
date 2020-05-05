from django.contrib import admin
from .models import Company, Contact, Deal, DealStage, DealStatus


class ContactInline(admin.TabularInline):
    model = Contact
    fields = ['surname', 'name', 'patronymic']
    extra = 1


class DealStatusInline(admin.StackedInline):
    model = DealStatus
    fields = ['deal', 'summ', 'currency', 'stage', 'expected_deal_date', 'created']
    readonly_fields = ('created', )
    extra = 1


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'form_of_ownership']
    inlines = [ContactInline, ]


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [DealStatusInline, ]


@admin.register(DealStage)
class DealStageAdmin(admin.ModelAdmin):
    list_display = ['name', 'probability_of_success']
