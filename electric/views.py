from django.shortcuts import render, redirect
from .models import *
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    vendors = Vendor.objects.all()
    
    if request.method == "POST":
        vendor = Vendor.objects.get(pk=request.POST.get("vendor"))
        category = request.POST.get("category")
        date = request.POST.get("date")
        amount = Decimal(request.POST.get("amount"))
        comment = request.POST.get("comment")

        t = Transaction(vendor=vendor, date=date, comment=comment)

        if category=="sale":
            vendor.balance = vendor.balance+amount
            t.debit = amount
        
        if category=="payment":
            vendor.balance = vendor.balance-amount
            t.credit = amount
        t.balance = vendor.balance
        t.save()
        vendor.save()
        msg = "New Balance of "+vendor.name+": "+str(vendor.balance)
        return redirect('index')

    context = {'vendors':vendors}
    return render(request, 'transactionForm.html', context)


@login_required
def ledger(request):
    vendors = Vendor.objects.all()

    if request.method == "POST":
        start_date = request.POST.get("from")
        end_date = request.POST.get("to")
        name = request.POST.get("name")
        vendor = Vendor.objects.get(pk=name)
        if start_date == '':
            start_date = None
        if end_date == '':
            end_date = None
        if name == "None":
            name = None

        if start_date and end_date and name:
            transactions = Transaction.objects.filter(date__gte=start_date,
                                                      date__lte=end_date,
                                                      vendor=vendor)

        elif start_date and end_date:
            transactions = Transaction.objects.filter(date__gte=start_date,
                                                      date__lte=end_date)

        elif start_date and name:
            transactions = Transaction.objects.filter(date__gte=start_date,
                                                      vendor=vendor)

        elif end_date and name:
            transactions = Transaction.objects.filter(date__lte=end_date,
                                                      vendor=vendor)

        elif start_date:
            transactions = Transaction.objects.filter(date__gte=start_date)

        elif end_date:
            transactions = Transaction.objects.filter(date__lte=end_date)

        elif name:
            transactions = Transaction.objects.filter(vendor=vendor)

        else:
            return redirect('ledger')
    
    else:
        now = datetime.now()
        transactions = Transaction.objects.filter(date=now)
    
    net_debit = round(sum(transactions.values_list('debit', flat=True)), 2)
    net_credit = round(sum(transactions.values_list('credit', flat=True)), 2)

    context = {'transactions':transactions, 'net_credit':net_credit, 'net_debit':net_debit, 'vendors':vendors}
    return render(request, 'ledger.html', context)