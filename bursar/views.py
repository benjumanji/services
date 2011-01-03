import datetime as dt

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from bursar.models import User,Transaction

def home(request):
    users = User.objects.all()
    txs = Transaction.objects.all()
    return render_to_response('bursar/index.html',{'users':users, 'txs':txs})

def add(request):
    post = request.POST
    payer_id = post['payer']
    payee_id = post['payee']
    value = post['value']
    reference = post['reference']
    dba = map(int,post['due_by'].split('/'))
    dba.reverse()

    tx = Transaction()
    tx.payer_id = payer_id
    tx.value = value
    tx.due_by = dt.date(*dba)
    tx.payee_id = payee_id
    tx.reference = reference
    tx.save()

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
