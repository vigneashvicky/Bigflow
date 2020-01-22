from django.urls import path
from Bigflow.BranchExp import views
from django.conf.urls import url, include


urlpatterns = [
    url(r'^BranchExp/(?P<template_name>[\w-]+)/$', views.Branch_Template , name='Branch_Template'),
    #url(r'^BranchExp/(?P<template_name>[\w-]+)/$', views.Branch_Template , name='Branch_Template'),
    path('Get_expense/', views.Get_expense , name='Get_expense'),
    path('Set_expense/', views.Set_expense , name='Set_expense'),
    path('test/', views.test, name='Invoiceheader_set'),
    path('change_value/', views.change_value, name='change_value'),
    path('change_value_l/', views.change_value_l, name='change_value_l'),
    path('insertNewBranchDetails/', views.insertNewBranchDetails, name='insert_branch_details_values'),
    path('maker_summary/', views.br_maker_summary, name='Br_MakerSummary'),
    path('GetpropertyType/', views.brGetPropertyType, name='Br_Get_Property_Type'),
    path('get_pr_details/', views.brGetPropertyDetails, name='Br_Get_Property_Details'),
    path('Br_PropertyApproval/', views.brPropertyApproval, name='Br_PropertyApproval')
    # path('Invoiceheader_set/', views.Invoiceheader_set, name='Invoiceheader_set'),

    #Br_Makersummary  -#Br_RentCreate

    # path('Expense_Process',view_branchexp.Expense_Process.as_view()),
    #  path('Expense_ProcessSet',view_branchexp.Expense_Process_Set.as_view())



]