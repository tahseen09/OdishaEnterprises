from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100, null=True, blank=True)
    contact = models.BigIntegerField(null=True, blank=True)
    balance = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    date = models.DateField(null=True)
    debit = models.FloatField(default=0.00)
    credit = models.FloatField(default=0.00)
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, null=True)
    comment = models.CharField(null=True, blank=True, max_length=100)
    balance = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.date)+'|'+self.vendor.name