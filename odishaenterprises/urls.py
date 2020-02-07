from django.contrib import admin
from django.urls import path, include
from electric.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', index, name='index'),
    path('ledger', ledger, name='ledger')
]

admin.site.site_header = 'Odisha Enterprises'
admin.site.site_title = 'Odisha Enterprises'
admin.site.index_title = 'Odisha Enterprises'