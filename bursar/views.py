import datetime as dt

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from bursar.models import User, Transaction, TransactionForm

def home(request):
    users = User.objects.all()
    txs = Transaction.objects.all()
    tx_form = TransactionForm()
    return render_to_response('bursar/index.html',{'users':users, 'txs':txs, 'tx_form':tx_form})

def add(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        tx = Transaction()
        tx.payer = data['payer']
        tx.payee = data['payee']
        tx.value = data['value']
        tx.reference = data['reference']
        tx.due_by = data['due_by']
        tx.save()
    else:
        pass
        #TODO: Add form errors!
    return HttpResponseRedirect(reverse('services.bursar.views.home'))

def update(request):
    post = request.POST
    ids = filter(lambda x: x[:2] == "tx",post.keys())
    #import pdb;pdb.set_trace()
    for i in ids:
        tx = Transaction.objects.get(pk=i[2:]) 
        tx.paid = True
        tx.save()

    return HttpResponseRedirect(reverse('services.bursar.views.home'))
