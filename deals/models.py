from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Company(models.Model):
    OWNERSHIP_OOO = 'ООО'
    OWNERSHIP_PAO = 'ПАО'
    OWNERSHIP_AO = 'АО'

    OWNERSHIP_CHOICES = [
        (OWNERSHIP_OOO, 'ООО'),
        (OWNERSHIP_PAO, 'ПАО'),
        (OWNERSHIP_AO, 'АО'),
    ]

    form_of_ownership = models.CharField(verbose_name='Форма собственности', choices=OWNERSHIP_CHOICES,
                                         default=OWNERSHIP_OOO, max_length=100)
    name = models.CharField(verbose_name='Название компании', max_length=100)

    def __str__(self):
        return self.form_of_ownership + ' ' + self.name

    class Meta:
        verbose_name = 'Компанию'
        verbose_name_plural = 'Компании'


class Contact(models.Model):
    surname = models.CharField(verbose_name='Фамилия', max_length=100)
    name = models.CharField(verbose_name='Имя', max_length=100)
    patronymic = models.CharField(verbose_name='Отчество', max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='contacts', verbose_name='Компания')

    def __str__(self):
        return self.surname

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Deal(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='deals', verbose_name='Контакт')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сделку'
        verbose_name_plural = 'Сделки'


class DealStage(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100, db_index=True)
    probability_of_success = models.IntegerField(verbose_name='Вероятность успеха сделки',
                                                 validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                 db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Стадию сделки'
        verbose_name_plural = 'Стадии сделок'


class DealStatus(models.Model):
    CURRENCY_RUB = 'RUB'
    CURRENCY_USD = 'USD'
    CURRENCY_EUR = 'EUR'

    CURRENCY_CHOICES = [
        (CURRENCY_RUB, 'RUB'),
        (CURRENCY_USD, 'USD'),
        (CURRENCY_EUR, 'EUR'),
    ]

    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='status', verbose_name='Сделка')
    summ = models.FloatField(verbose_name='Сумма', validators=[MinValueValidator(0)])
    currency = models.CharField(verbose_name='Валюта',choices=CURRENCY_CHOICES, default=CURRENCY_RUB, max_length=100,
                                db_index=True)
    stage = models.ForeignKey(DealStage, on_delete=models.CASCADE, related_name='status', verbose_name='Стадия',
                              db_index=True)
    expected_deal_date = models.DateField(verbose_name='Дата предполагаемого совершения сделки', db_index=True)
    created = models.DateTimeField(verbose_name='Дата создания текущей записи', auto_now_add=True, editable=True)

    def __str__(self):
        return self.deal.name

    class Meta:
        verbose_name = 'Состояние сделки'
        verbose_name_plural = 'Состояния сделок'
