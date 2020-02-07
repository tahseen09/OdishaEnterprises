from django.shortcuts import render
from .models import *
from decimal import Decimal

def index(request):
    vendors = Vendor.objects.all()
    msg = None
    
    if request.method == "POST":
        vendor = Vendor.objects.get(pk=request.POST.get("vendor"))
        category = request.POST.get("category")
        date = request.POST.get("date")
        amount = Decimal(request.POST.get("amount"))
        comment = request.POST.get("comment")

        t = Transaction(vendor=vendor, date=date, comment=comment)
        # t.save()

        if category=="sale":
            vendor.balance = vendor.balance + amount
            t.debit = amount
        
        if category=="payment":
            vendor.balance = vendor.balance-amount
            t.credit = amount
        
        t.save()
        vendor.save()
        msg = "New Balance of "+vendor.name+": "+str(vendor.balance)

    context = {'vendors':vendors, 'msg':msg}
    return render(request, 'transactionForm.html', context)