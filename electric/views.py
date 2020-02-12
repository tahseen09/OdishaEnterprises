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
        brand = request.POST.get("brand")
        date = request.POST.get("date")
        amount = Decimal(request.POST.get("amount"))
        comment = request.POST.get("comment")

        t = Transaction(vendor=vendor, date=date, comment=comment)
        
        if brand=="ajanta":
            if category=="sale":
                vendor.ajantaBalance = vendor.ajantaBalance+amount
                t.debit = amount
            elif category=="payment":
                vendor.ajantaBalance = vendor.ajantaBalance-amount
                t.credit = amount
            t.balance = vendor.ajantaBalance
            t.brand = "Ajanta"

        elif brand=="cpl":
            if category=="sale":
                vendor.cplBalance = vendor.cplBalance+amount
                t.debit = amount
            elif category=="payment":
                vendor.cplBalance = vendor.cplBalance-amount
                t.credit = amount
            t.balance = vendor.cplBalance
            t.brand = "CPL"

        elif brand=="orient":
            if category=="sale":
                vendor.orientBalance = vendor.orientBalance+amount
                t.debit = amount
            elif category=="payment":
                vendor.orientBalance = vendor.orientBalance-amount
                t.credit = amount
            t.balance = vendor.orientBalance
            t.brand = "Orient"
        
        t.save()
        vendor.save()
        # msg = "New Balance of "+vendor.name+": "+str(vendor.balance)
        return redirect('index')

    context = {'vendors':vendors}
    return render(request, 'transactionForm.html', context)


@login_required
def ledger(request):
    vendors = Vendor.objects.all()
    transactions = Transaction.objects.all()

    if request.method == "POST":
        start_date = request.POST.get("from")
        end_date = request.POST.get("to")

        if start_date == '':
            start_date = None
        if end_date == '':
            end_date = None

        if start_date:
            transactions = transactions.filter(date__gte=start_date)
        if end_date:
            transactions = transactions.filter(date__lte=end_date)

    else:
        now = datetime.now()
        transactions = Transaction.objects.filter(date=now)
    
    net_debit = round(sum(transactions.values_list('debit', flat=True)), 2)
    net_credit = round(sum(transactions.values_list('credit', flat=True)), 2)

    context = {'transactions':transactions, 'net_credit':net_credit, 'net_debit':net_debit, 'vendors':vendors}
    return render(request, 'ledger.html', context)


def partyLedger(request, vendorID):
    vendor = Vendor.objects.get(pk=vendorID)
    transactions = Transaction.objects.filter(vendor=vendor)
    if request.method=="POST":
        start_date = request.POST.get("from")
        end_date = request.POST.get("to")
        brand = request.POST.get("brand")
        if start_date:
            transactions = transactions.filter(date__gte=start_date)
        if end_date:
            transactions = transactions.filter(date__lte=end_date)
        if brand:
            transactions = transactions.filter(brand=brand)

    net_debit = round(sum(transactions.values_list('debit', flat=True)), 2)
    net_credit = round(sum(transactions.values_list('credit', flat=True)), 2)

    context = {'vendor':vendor, 'transactions':transactions, 'net_credit':net_credit, 'net_debit':net_debit}
    return render(request, 'partyledger.html', context)


def showBalance(request):
    vendors = Vendor.objects.all()
    context = {'vendors': vendors}
    return render(request, 'showbalance.html', context)