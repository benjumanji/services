from django.db import models
from django.db.models import Sum
from django.forms import ModelForm
from datetime import datetime
from bursar.widgets import DatePickerWidget

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __unicode__(self):
        return '%s %s' % (self.first_name,self.last_name)

    def get_payments_owing(self):
        return self.payer.filter(paid=False).aggregate(Sum('value'))["value__sum"]

    def get_payments_owed(self):
        return self.payee.filter(paid=False).aggregate(Sum('value'))["value__sum"]

    def get_payments_owing_od(self):
        today = datetime.now()
        return self.payer.filter(paid=False,due_by__lt=today).aggregate(Sum('value'))['value__sum']

    def get_payments_owed_od(self):
        today = datetime.now()
        return self.payee.filter(paid=False,due_by__lt=today).aggregate(Sum('value'))['value__sum']

    @classmethod
    def get_annotated(cls):
        today = datetime.now()
        q1 = cls.objects.filter(payer__paid=False).annotate(payments_owing=Sum('payer__value'))
        q2 = q1.filter(payee__paid=False).annotate(payments_owed=Sum('payee__value'))
        q3 = q2.filter(payer__paid=False,payer__due_by__lt=today).annotate(payments_owing_od=Sum('payer__value'))
        q4 = q3.filter(payee__paid=False,payee__due_by__lt=today).annotate(payments_owed_od=Sum('payee__value'))
        return q4


class Transaction(models.Model):
    payer = models.ForeignKey(User, related_name='payer')
    payee = models.ForeignKey(User, related_name='payee')
    value = models.DecimalField(max_digits=7, decimal_places=2)
    reference = models.SlugField()
    due_by = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    disputed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    def __unicode__(self):
        return '<Tx:%s/%i>' % (self.reference,self.value)


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        widgets = {'due_by':DatePickerWidget(format='%d/%m/%Y')}
        exclude = ('disputed','paid')
