from django.conf.urls import url
from django.urls import path
from Bigflow.inward import views

urlpatterns = [
    path('inward_summary/', views.inward_summary, name='inward_summary'),
    path('setinwardentry/',views.inward_create,name='setinwardentry'),
    path('get_inwardsummary/',views.get_inwardsummary,name='get_inwardsummary'),
    path('setinwarddetails/', views.setinwarddetails, name='setinwarddetails'),
    path('invoice/',views.invoice_crt, name='createinvoice')
    ];
