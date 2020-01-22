from django.urls import path
from Bigflow.AP import views

urlpatterns = [
    path('billentry/', views.billentryIndex, name='billentry'),
    path('POinvoicemk/', views.POinvoice, name="POinvoice" ),
    path('getgrndetail/',views.getgrndetail, name='getgrndetail'),
    path('Invoicesummary/', views.Invoicesummary , name='Invoicesummary'),
    path('inwarddtl_get/', views.inwarddtl_get , name='inwarddtl_get'),
    path('Inward_entry/', views.Inward_entry , name='Inward_entry'),
    path('Invoice_set/', views.Invoice_set , name='Invoice_set'),
    path('APInvoice_get/',views.APInvoice_get, name='APInvoice_get'),
    path('makersummary/', views.Makersummary , name='makersummary'),
    path('Credit_get/', views.Credit_get , name='Credit_get'),
    path('Invoiceheader_set/' , views.Invoiceheader_set , name='Invoiceheader_set'),
    path('HSN_get/' , views.HSN_get , name='HSN_get'),
    path('Hsntax_get/', views.Hsntax_get , name='Hsntax_get'),
    path('tablevalue/', views.tablevalue, name = 'tablevalue'),
    path('Checkersummary/', views.Checkersummary, name = 'Checkersummary'),
    path('HsntaxCredit_get/', views.HsntaxCredit_get , name='HsntaxCredit_get'),
    path('APInvoiceChecker_get/', views.APInvoiceChecker_get , name='APInvoiceChecker_get'),
    path('Approvalsummary/', views.Approvalsummary, name='Approvalsummary'),
    path('AP_History/', views.AP_History, name='AP_History'),
    path('AP_History_get/', views.AP_History_get, name='AP_History_get'),
    path('PreparePayment/', views.PreparePayment , name='Paymentsummary'),
    path('PrepareFile/', views.PrepareFile , name='PrepareFile'),
    path('Paymentupdate/', views.paymentupdate, name = 'paymentstatus'),
    path('APpayment_set/', views.APpayment_set, name="Appaymentset"),
    path('Rejectsummary/', views.Rejectsummary , name='Rejectsummary'),
    path('claimrejection/', views.claimrejection, name='claimrejection'),
    path('Rejectdata/', views.Rejectdata , name = 'Rejectdata'),
    path('Getreason_data/', views.Getreason_data , name= 'Getreason_data'),
    path('APrejectinv_set/', views.APrejectinv_set ,name='APrejectinv_set'),
    path('Paymmentdtl_get/', views.Paymmentdtl_get , name='Paymmentdtl_get'),
    path('billentryedit/', views.billentryedit , name='billentryedit'),
    path('Dropdown_detail_ap/', views.Dropdown_detail_ap, name='Dropdown_details'),
    path('PPPXDeatails_get/', views.PPPXDeatails_get, name='PPPXDeatails_get'),
    path('PPPXDeatails_set/', views.PPPXDeatails_set, name='PPPXDeatails_set'),
    path('APsummary/', views.APsummary, name='APsummary'),
    path('getpayment_excel/', views.getpayment_excel, name='getpayment_excel'),
    path('Dispatch_Payment/', views.Dispatch_Set_Payment, name='getpayment_excel'),
    path('auditchklist_get/', views.auditchklist_get, name='auditchklist_get'),
    path('auditchklist_set/', views.auditchklist_set, name='auditchklist_get'),
    path('Get_address_ap/', views.Get_address_ap, name='Get_address_ap'),
    path('PaymentStatus/', views.AP_PaymentStatus, name='AP_PaymentStatus.html'),
    path('PODDispatch_Set_AP/', views.PODDispatch_Set_AP, name='PODDispatch_Set_AP'),
    path('upload_image_ap/', views.upload_image_ap, name='upload_image_ap'),
    path('APStale_set/', views.APStale_set, name='APStale_set'),
    path('APNeftExcel_downld/', views.APNeftExcel_downld, name='APNeftExcel_downld'),
    path('Stalesummary/', views.Stalesummary, name='Stalesummary'),
    path('stalesummary_get/', views.stalesummary_get, name='stalesummary_get'),
    path('classificationdata_get/', views.classificationdata_get, name='classificationdata_get'),
    path('supplierdata_get/', views.supplierdata_get, name='supplierdata_get'),
    path('EmployeeQuery/', views.Ap_EmployeeQuery, name='Ap_EmployeeQuery'),

    path('bill/', views.bill, name='billentry'),

    #ecf
    path('ECFinventry/', views.Ecf_Invoiceentry, name='ECFinventry'),
    path('ECFInvoiceheader_set/', views.ECFInvoiceheader_set, name='ECFInvoiceheader_set'),
    path('ECFInvoice_get/', views.ECFInvoice_get, name='ECFInvoice_get'),
    path('Ecf_billentry/', views.Ecf_billentry, name='Ecf_billentry'),
    path('ECFInvoice_set/', views.ECFInvoice_set, name='ECFInvoice_set'),
    path('ECFPOinvoicemk/', views.ECFPOinvoicemk, name="ECFPOinvoicemk"),
    path('ECFApproval/', views.ECFApproval, name="ECFApproval"),
    path('ECFInvoiceChecker_get/', views.ECFInvoiceChecker_get, name="ECFInvoiceChecker_get"),
    path('APECF_entry/', views.APECF_entry, name="APECF_entry"),
    path('ECFSummary/', views.ECFSummary, name="ECFSummary"),
    path('ECF_ApChecker_get/', views.ECF_ApChecker_get, name="ECF_ApChecker_get"),

]