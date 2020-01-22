import io

from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from Bigflow.AP.model import mAP
import pandas as pd
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.template import Context, Template, RequestContext
from django.views import View


def billentryIndex(request):
    return render(request, "AP_billentry.html")

def APsummary(request):
    return render(request, "AP_APSummary.html")

def bill(request):
    return render(request, "AP_BILL.html")

def POinvoice(request):
    return render(request, "AP_POinvoicemk.html")

def Stalesummary(request):
    return render(request, "AP_Stalesummary.html")

def getgrndetail(request):
    if request.method == 'POST':
        grn_dtl =  mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        grn_dtl.action = jsondata.get('params').get('action')
        grn_dtl.POnumber = jsondata.get('params').get('POnumber')
        grn_dtl.supplier_gid = jsondata.get('params').get('supplier_gid')
        grn_dtl.entity_gid = request.session['Entity_gid']
        dtl = grn_dtl.get_grn()
        jdata = dtl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def Invoicesummary(request):
    return render(request, "AP_invoicesummary.html")


def outputSplit(tubledtl,index):
    temp=tubledtl[0].split(',')
    if(len(temp)>1):
        if (index==0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return  temp[0]
    
def inwarddtl_get(request):
    if request.method == 'POST':
        inward_dtl = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        inward_dtl.action = jsondata.get('params').get('action')
        inward_dtl.type = jsondata.get('params').get('type')
        inward_dtl.FILTER_JSON = jsondata.get('params').get('FILTER_JSON')
        inward_dtl.entity_gid = request.session['Entity_gid']
        out = outputSplit(inward_dtl.get_inwarddtl(), 1)
        return JsonResponse(out, safe=False)

def Inward_entry(request):
    return render(request, "AP_Invoice-Inwardentry.html")

def Invoice_set(request):
    if request.method == 'POST':
        inward_dtl = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        inward_dtl.action = jsondata.get('params').get('action')
        inward_dtl.type = jsondata.get('params').get('type')
        inward_dtl.header_json = jsondata.get('params').get('header_json')
        inward_dtl.detail_json = jsondata.get('params').get('detail_json')
        inward_dtl.invoice_json = jsondata.get('params').get('invoice_json')
        inward_dtl.debit_json = jsondata.get('params').get('debit_json')
        inward_dtl.credit_json = jsondata.get('params').get('credit_json')
        inward_dtl.status_json = jsondata.get('params').get('status_json')
        inward_dtl.entity_gid = request.session['Entity_gid']
        inward_dtl.employee_gid = request.session['Emp_gid']
        out = outputSplit(inward_dtl.set_Invoice(), 1)
        return JsonResponse(out, safe=False)

def APInvoice_get(request):
    if request.method == 'POST':
        invoice_get = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        invoice_get.action = jsondata.get('params').get('action')
        invoice_get.ponumber = jsondata.get('params').get('ponumber')
        invoice_get.supplier_gid = jsondata.get('params').get('supplier_gid')
        invoice_get.inwarddetail_gid = jsondata.get('params').get('inwarddetail_gid')
        invoice_get.inwardheader_gid = jsondata.get('params').get('inwardheader_gid')
        invoice_get.status = jsondata.get('params').get('status')
        invoice_get.entity_gid = request.session['Entity_gid']
        invoice_get.state_gid = request.session['Entity_state_gid']
        invoice_get.limit = jsondata.get('params').get('limit')
        out = invoice_get.Invoice_get()
        jdata = out.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def Makersummary(request):
    return render(request,"AP_makersummary.html", {"my_data": {}})

def Credit_get(request):
    if request.method == 'POST':
        credit_get = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        credit_get.type = jsondata.get('params').get('type')
        credit_get.supplier_gid = jsondata.get('params').get('supplier_gid')
        credit_get.entity_gid = request.session['Entity_gid']
        out = credit_get.credit_get()
        jdata = out.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def Invoiceheader_set(request):
    if request.method == 'POST':
        inward_dtl = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        inward_dtl.action = jsondata.get('params').get('action')
        inward_dtl.type = jsondata.get('params').get('type')
        inward_dtl.header_json = jsondata.get('params').get('header_json')
        inward_dtl.debit_json = jsondata.get('params').get('debit_json')
        inward_dtl.detail_json = jsondata.get('params').get('detail_json')
        inward_dtl.status_json = jsondata.get('params').get('status_json')
        inward_dtl.entity_gid = request.session['Entity_gid']
        inward_dtl.employee_gid = request.session['Emp_gid']
        out = outputSplit(inward_dtl.set_Invoiceheader(), 1)
        return JsonResponse(out, safe=False)

def HSN_get(request):
    if request.method == 'POST':
        credit_get = mAP.ap_model()
        credit_get.type = "HSN"
        credit_get.group = "HSN"
        credit_get.filter = {}
        credit_get.entity_gid = request.session['Entity_gid']
        out = credit_get.hsn_get()
        jdata = out.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def Hsntax_get(request):
    if request.method == 'POST':
        tax = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        tax.hsndtl = jsondata.get('params').get('hsndtl')
        tax.entity_gid = request.session['Entity_gid']
        tax.group =jsondata.get('params').get('group')
        out = tax.hsn_taxget()
        data1 = pd.DataFrame(out,columns=['gst'])
        #data1 = {"detail":out}
        jdata = data1.to_json(orient='records')
        return JsonResponse(jdata, safe=False)

def HsntaxCredit_get(request):
    if request.method == 'POST':
        tax = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        tax.hsndtl = jsondata.get('params').get('hsndtl')
        tax.entity_gid = request.session['Entity_gid']
        tax.group =jsondata.get('params').get('group')
        out = tax.hsn_Credittaxget()
        jdata = out.to_json(orient='records')
        return JsonResponse(jdata, safe=False)

def tablevalue(request):
    if request.method == 'POST':
        dropdown = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        dropdown.type = "DEBIT"
        dropdown.tablevalue = jsondata.get('params').get('tablevalue')
        dropdown.entity_gid = request.session['Entity_gid']
        out = dropdown.tablevalue_get()
        jdata = out.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def Checkersummary(request):
    return render(request, "AP_CheckerSummary.html")

def APInvoiceChecker_get(request):
    if request.method == 'POST':
        invoice_get = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        invoice_get.action = jsondata.get('params').get('action')
        invoice_get.ponumber = jsondata.get('params').get('ponumber')
        invoice_get.supplier_gid = jsondata.get('params').get('supplier_gid')
        invoice_get.inwarddetail_gid = jsondata.get('params').get('inwarddetail_gid')
        invoice_get.inwardheader_gid = jsondata.get('params').get('inwardheader_gid')
        invoice_get.status = jsondata.get('params').get('status')
        invoice_get.entity_gid = request.session['Entity_gid']
        invoice_get.state_gid = request.session['Entity_state_gid']
        out = invoice_get.Invoice_get()
        out =  out.fillna(0)
        if  invoice_get.action == 'INVOICE_DETAILS_EDIT':
            df_invoice = (out[['invoicedetails_gid','invoicedetails_item', 'invoicedetails_desc',
                               'invoicedetails_hsncode','invoicedetails_unitprice','invoicedetails_qty','invoicedetails_sgst',
                               'invoicedetails_cgst','invoicedetails_igst','invoicedetails_amount','invoicedetails_discount','invoicedetails_totalamt','DEBIT_DETAILS']]).groupby(
                ['invoicedetails_gid','invoicedetails_item', 'invoicedetails_desc','invoicedetails_hsncode',
                 'invoicedetails_unitprice','invoicedetails_qty','invoicedetails_sgst',
                               'invoicedetails_cgst','invoicedetails_igst','invoicedetails_amount','invoicedetails_discount','invoicedetails_totalamt','DEBIT_DETAILS']).size().reset_index();
            df_debit = out.groupby(
                ['invoicedetails_gid','debit_gid', 'debit_categorygid', 'debit_subcategorygid',
                              'debit_glno','debit_amount','DEBIT_DETAILS']).size().reset_index()
            df_credit = (out[['credit_gid', 'credit_paymodegid', 'credit_refno','bankbranch_ifsccode',
                         'credit_glno','credit_amount','Paymode_name','bankdetails_beneficiaryname','credit_suppliertaxtrate','suppliertax_panno','credit_suppliertaxtype',
                              'ppxdetails_ppxheadergid','ppxdetails_gid','bankbranch_name']]).groupby(
                ['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                 'credit_glno','credit_amount','Paymode_name','bankdetails_beneficiaryname','credit_suppliertaxtrate','suppliertax_panno','credit_suppliertaxtype',
                 'ppxdetails_ppxheadergid','ppxdetails_gid','bankbranch_name']).size().reset_index();
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankbranch_ifsccode'] = ''
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankdetails_beneficiaryname'] = ''
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankbranch_name'] = ''
        else:
            df_invoice = (out[['invoicedetails_gid', 'invoicedetails_item', 'invoicedetails_desc',
                               'invoicedetails_hsncode', 'invoicedetails_unitprice', 'invoicedetails_qty',
                               'invoicedetails_sgst',
                               'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount','invoicedetails_discount',
                               'invoicedetails_totalamt','DEBIT_DETAILS']]).groupby(
                ['invoicedetails_gid', 'invoicedetails_item', 'invoicedetails_desc', 'invoicedetails_hsncode',
                 'invoicedetails_unitprice', 'invoicedetails_qty', 'invoicedetails_sgst',
                 'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount','invoicedetails_discount',
                 'invoicedetails_totalamt','DEBIT_DETAILS']).size().reset_index();
            df_debit = out.groupby(
                ['invoicedetails_gid', 'debit_gid', 'debit_categorygid', 'debit_subcategorygid',
                 'debit_glno', 'debit_amount']).size().reset_index();
            df_credit = (out[['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname','ppxdetails_ppxheadergid','ppxdetails_gid','bankbranch_name'
                              ]]).groupby(
                ['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                 'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname','ppxdetails_ppxheadergid','ppxdetails_gid','bankbranch_name'
                 ]).size().reset_index();
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankbranch_ifsccode'] = ''
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankdetails_beneficiaryname'] = ''
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankbranch_name'] = ''

        data = {}
        data['invoice'] = json.loads(df_invoice.to_json(orient='records'))
        data['debit'] = json.loads(df_debit.to_json(orient='records'))
        data['credit'] = json.loads(df_credit.to_json(orient='records'))
        jdata = data
        return JsonResponse(jdata, safe=False)

def Approvalsummary(request):
    return render(request, "AP_Approvalsummary.html")

def AP_History(request):
    return render(request, "AP_History.html")


def AP_History_get(request):
    if request.method == 'POST':
        history = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        history.group = jsondata.get('params').get('group')
        history.type = jsondata.get('params').get('type')
        history.entity_gid = request.session['Entity_gid']
        history.refvalue =jsondata.get('params').get('refvalue')
        out = history.History_get()
        jdata = out.to_json(orient='records')
        return JsonResponse(jdata, safe=False)

def PreparePayment(request):
    return render(request, "AP_Paymentsummary.html")

def PrepareFile(request):
    return render(request, "AP_Payment.html")

def paymentupdate(request):
    return render(request,"AP_PaymentUpdation.html")

def APpayment_set(request):
    if request.method == 'POST':
        inward_dtl   = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        inward_dtl.action = jsondata.get('params').get('action')
        inward_dtl.type = jsondata.get('params').get('type')
        inward_dtl.header_json = jsondata.get('params').get('header_json')
        inward_dtl.detail_json = jsondata.get('params').get('detail_json')
        inward_dtl.other_json = jsondata.get('params').get('other_json')
        inward_dtl.status_json = jsondata.get('params').get('status_json')
        inward_dtl.entity_gid = request.session['Entity_gid']
        inward_dtl.employee_gid = request.session['Emp_gid']
        out = outputSplit(inward_dtl.set_payment(), 1)
        return JsonResponse(out, safe=False)

def Rejectsummary(request):
    return render(request,"AP_Rejectsummary.html")

def claimrejection(request):
    return render(request, "AP_Claimrejection.html")

def Rejectdata(request):
    if request.method == 'POST':
        reject = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        reject.group = jsondata.get('params').get('group')
        reject.type = jsondata.get('params').get('type')
        reject.reject_json = jsondata.get('params').get('reject_json')
        reject.entity_gid = request.session['Entity_gid']
        out = reject.rejectdata_get()
        jdata = out.to_json(orient='records')
        return JsonResponse(jdata, safe=False)

def Getreason_data(request):
    if request.method == 'POST':
        reject = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        reject.type = jsondata.get('params').get('type')
        reject.reason_json = jsondata.get('params').get('reason_json')
        reject.entity_gid = request.session['Entity_gid']
        out = reject.getreasondata()
        jdata = out.to_json(orient='records')
        return JsonResponse(jdata, safe=False)

def APrejectinv_set(request):
    if request.method == 'POST':
        reject   = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        reject.action = jsondata.get('params').get('action')
        reject.type = jsondata.get('params').get('type')
        reject.reject_json = jsondata.get('params').get('reject_json')
        reject.entity_gid = request.session['Entity_gid']
        reject.employee_gid = request.session['Emp_gid']
        out = outputSplit(reject.set_Invoicereject(), 1)
        return JsonResponse(out, safe=False)

def Paymmentdtl_get(request):
    if request.method == 'POST':
        payment = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        payment.group = jsondata.get('params').get('group')
        payment.type = jsondata.get('params').get('type')
        payment.pay_json = jsondata.get('params').get('pay_json')
        payment.entity_gid = request.session['Entity_gid']
        out = payment.getpaymentdtl()
        jdata = out.to_json(orient='records')
        return JsonResponse(jdata, safe=False)

def billentryedit(request):
    return render(request,"AP_billentryEdit.html")

def Dropdown_detail_ap(request):
    if request.method == 'POST':
        dropdown = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        dropdown.tablename = jsondata.get('params').get('tablename')
        dropdown.gid = jsondata.get('params').get('gid')
        dropdown.name = jsondata.get('params').get('name')
        dropdown.entity_gid = request.session['Entity_gid']
        data = dropdown.get_dropdown_detail()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)

def PPPXDeatails_get(request):
    if request.method == 'POST':
        details = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        details.group = jsondata.get('params').get('group')
        details.type =  jsondata.get('params').get('type')
        details.filter = jsondata.get('params').get('Filterdata')
        details.entity_gid = request.session['Entity_gid']
        data = details.get_ppxdetails()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def PPPXDeatails_set(request):
    if request.method == 'POST':
        details = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        details.action = jsondata.get('params').get('action')
        details.type =  ''
        details.header_json = jsondata.get('params').get('header_json')
        details.detail_json = jsondata.get('params').get('detail_json')
        details.entity_gid = request.session['Entity_gid']
        details.employee_gid = request.session['Emp_gid']
        data =outputSplit( details.set_ppxdetails(), 1)
        return JsonResponse(data, safe=False)

def getpayment_excel(request):
    df = pd.read_excel(open(str(settings.MEDIA_ROOT)+"/"+"bankdetails.xlsx", 'rb'), sheetname='Sheet1')
    XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = HttpResponse(content_type=XLSX_MIME)
    response['Content-Disposition'] = 'attachment; filename="PythonExport.xlsx"'
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    df.loc[0,'Bank Name'] = "ICICI"
    df.to_excel(writer, 'Sheet1', index=False)
    email = EmailMessage('Subject', "", to=['vsolvstab@gmail.com'])
    attachment = export_excel(df)
    email.attach('invoice.xlsx', attachment, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()
    writer.save()
    return response

def export_excel(df):
  with io.BytesIO() as buffer:
    writer = pd.ExcelWriter(buffer)
    df.to_excel(writer,index=False)
    writer.save()
    return buffer.getvalue()

def Dispatch_Set_Payment(request):
    if request.method == 'POST':
        details = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        lst = jsondata.get('dispatch_data')
        for x in lst:
            details.action = x.get('action')
            details.type = x.get('type')
            details.in_out =  x.get('in_out')
            details.courier_gid = x.get('courier_gid')
            details.Dispatch_date = x.get('Dispatch_date')
            details.send_by = request.session['Emp_gid']
            details.awbno = x.get('awbno')
            details.dispatch_mode = x.get('dispatch_mode')
            details.dispatch_type = x.get('dispatch_type')
            details.packets = x.get('packets')
            details.weight = x.get('weight')
            details.dispatch_to = x.get('dispatch_to')
            details.address = x.get('address')
            details.city = x.get('city')
            details.state = x.get('state')
            details.pincode = x.get('pincode')
            details.remark = x.get('remark')
            details.returned = x.get('returned')
            details.returned_on = x.get('returned_on')
            details.returned_remark = x.get('returned_remark')
            details.pod = x.get('pod')
            details.pod_image = x.get('pod_image')
            details.isactive = x.get('isactive')
            details.isremoved = x.get('isremoved')
            details.dispatch_gid = x.get('dispatch_gid')
            details.status = x.get('status')
        details.PAYMENT_JSON = jsondata.get('payment_dtl')
        details.entity_gid = request.session['Entity_gid']
        details.employee_gid = request.session['Emp_gid']
        Service_out = outputSplit(details.set_Dispatchpayment(), 0)
        return JsonResponse(Service_out, safe=False)


def auditchklist_get(request):
    if request.method == 'POST':
        details = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        details.type =  jsondata.get('params').get('type')
        details.header_gid =  jsondata.get('params').get('header_gid')
        details.chk_type =  jsondata.get('params').get('chk_type')
        details.entity_gid = request.session['Entity_gid']
        data = details.get_auditchklist()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)

def auditchklist_set(request):
    if request.method == 'POST':
        details = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        details.action = jsondata.get('params').get('action')
        details.type = jsondata.get('params').get('type')
        details.chklist_json = jsondata.get('params').get('chklist_json')
        details.entity_gid = request.session['Entity_gid']
        details.employee_gid = request.session['Emp_gid']
        out = outputSplit(details.auditchklist(), 1)
        return JsonResponse(out, safe=False)

def Get_address_ap(request):
    if request.method == 'POST':
        obj_customer_ddl =  mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_customer_ddl.location_gid =jsondata.get('params').get('Address_gid')
        obj_customer_ddl.entity_gid = request.session['Entity_gid']
        df_customer_ddl = obj_customer_ddl.Address_Get()
        jdata = df_customer_ddl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def AP_PaymentStatus(request):
    return render(request, "AP_PaymentStatus.html")

def PODDispatch_Set_AP(request):
    if request.method == 'POST':
        dispatch_dtl = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        lst = jsondata.get('dispatch_data')
        for x in lst:
            dispatch_dtl.action = x.get('action')
            dispatch_dtl.type = x.get('type')
            dispatch_dtl.courier_gid = x.get('courier_gid')
            dispatch_dtl.Dispatch_date = x.get('Dispatch_date')
            dispatch_dtl.send_by = x.get('send_by')
            dispatch_dtl.awbno = x.get('awbno')
            dispatch_dtl.dispatch_mode = x.get('dispatch_mode')
            dispatch_dtl.dispatch_type = x.get('dispatch_type')
            dispatch_dtl.packets = x.get('packets')
            dispatch_dtl.weight = x.get('weight')
            dispatch_dtl.dispatch_to = x.get('dispatch_to')
            dispatch_dtl.address = x.get('address')
            dispatch_dtl.city = x.get('city')
            dispatch_dtl.state = x.get('state')
            dispatch_dtl.pincode = x.get('pincode')
            dispatch_dtl.remark = x.get('remark')
            dispatch_dtl.returned = x.get('returned')
            dispatch_dtl.returned_on = x.get('returned_on')
            dispatch_dtl.returned_remark = x.get('returned_remark')
            dispatch_dtl.pod = x.get('pod')
            dispatch_dtl.pod_image = x.get('pod_image')
            dispatch_dtl.isactive = x.get('isactive')
            dispatch_dtl.isremoved = x.get('isremoved')
            dispatch_dtl.dispatch_gid = x.get('dispatch_gid')
            dispatch_dtl.entity_gid = request.session['Entity_gid']
        dispatch_dtl.employee_gid = request.session['Emp_gid']
        Service_out = dispatch_dtl.set_PODDispatch_ap()
        return JsonResponse(Service_out, safe=False)

from django.conf import settings
from datetime import datetime
def upload_image_ap(request):
    if request.method == 'POST' and request.FILES['file']:
        try:
            current_month = datetime.now().strftime('%m')
            current_day = datetime.now().strftime('%d')
            current_year_full = datetime.now().strftime('%Y')
            save_path = str(settings.MEDIA_ROOT) + '/AP_POD/' + str(current_year_full) + '/' + str(
                current_month) + '/' + str(current_day) + '/' + str(request.POST['filename'])
            path = default_storage.save(str(save_path), request.FILES['file'])
            db_path = 'media/AP_POD/' + str(current_year_full) + '/' + str(
                current_month) + '/' + str(current_day) + '/' + str(request.POST['filename'])
            #path = default_storage.save(str(save_path), request.FILES['file'])
            return JsonResponse({"MESSAGE": "SUCCESS", "IMAGE_URL": db_path})
        except Exception as ex:
            return JsonResponse({"DATA": str(ex)})

def APStale_set(request):
    if request.method == 'POST':
        details = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        details.action = jsondata.get('params').get('action')
        details.type =  ''
        details.header_json = jsondata.get('params').get('header_json')
        details.entity_gid = request.session['Entity_gid']
        details.employee_gid = request.session['Emp_gid']
        data =outputSplit( details.set_APstale(), 1)
        return JsonResponse(data, safe=False)

def APNeftExcel_downld(request):
    if request.method == 'POST':
         try:
            jsondata = json.loads(request.body.decode('utf-8'))
            Amount = jsondata.get('params').get('Amount')
            ACCno = jsondata.get('params').get('ACCno')
            IFSC_code = jsondata.get('params').get('IFSC_code')
            BENIFICIARY_NAME = jsondata.get('params').get('BENIFICIARY_NAME')
            df = pd.read_excel(open(str(settings.MEDIA_ROOT)+"/"+"bankdetails.xlsx", 'rb'), sheetname='Sheet1')
            XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            response = HttpResponse(content_type=XLSX_MIME)
            response['Content-Disposition'] = 'attachment; filename="PythonExport.xlsx"'
            writer = pd.ExcelWriter(response, engine='xlsxwriter')
            df.loc[0,'Bank Name'] = ""
            df.loc[0,'Amount'] = Amount
            df.loc[0,'Bank beneficiary'] = BENIFICIARY_NAME
            df.loc[0,'Bank IFSC'] = IFSC_code
            df.loc[0,'Acc'] = ACCno
            df.to_excel(writer, 'Sheet1', index=False)
            email = EmailMessage('Subject', "", to=['vsolvstab@gmail.com'])
            attachment = export_excel(df)
            email.attach('invoice.xlsx', attachment, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            email.send()
            writer.save()
            return JsonResponse({"MESSAGE": "SUCCESS"})
         except Exception as ex:
              return JsonResponse({"DATA": str(ex)})

def stalesummary_get(request):
    if request.method == 'POST':
        details = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        details.type =  jsondata.get('params').get('type')
        details.sub_type =  jsondata.get('params').get('sub_type')
        details.filter_json ='{"Payment_Header_Gid":""}'
        details.entity_gid = request.session['Entity_gid']
        details.employee_gid = request.session['Emp_gid']
        data = details.get_stale()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)

def classificationdata_get(request):
    if request.method == 'POST':
        classify = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        classify.type =  jsondata.get('params').get('type')
        classify.sub_type =  jsondata.get('params').get('Sub_Type')
        classify.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
        classify.json_classification = jsondata.get('params').get('CLASSIFICATION')
        classify.json_classification["Entity_Gid"][0] = request.session['Entity_gid']
        ld_out_message = classify.get_classification_summary()
        ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND'}
        return  JsonResponse(ld_dict, safe=False)

def supplierdata_get(request):
    if request.method == 'POST':
        classify = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        classify.type =  jsondata.get('params').get('type')
        classify.sub_type =  jsondata.get('params').get('Sub_Type')
        classify.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
        classify.json_classification = jsondata.get('params').get('CLASSIFICATION')
        classify.json_classification["Entity_Gid"][0] = request.session['Entity_gid']
        ld_out_message = classify.get_supplier_data()
        ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')), "MESSAGE": 'FOUND'}
        return  JsonResponse(ld_dict, safe=False)

#ECF

def Ecf_Invoiceentry(request):
    return render(request, "ECF_invoiceentry.html")

def ECFInvoiceheader_set(request):
    if request.method == 'POST':
        inward_dtl = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        inward_dtl.action = jsondata.get('params').get('action')
        inward_dtl.type = jsondata.get('params').get('type')
        inward_dtl.header_json = jsondata.get('params').get('header_json')
        inward_dtl.debit_json = jsondata.get('params').get('debit_json')
        inward_dtl.detail_json = jsondata.get('params').get('detail_json')
        inward_dtl.status_json = jsondata.get('params').get('status_json')
        inward_dtl.entity_gid = request.session['Entity_gid']
        inward_dtl.employee_gid = request.session['Emp_gid']
        out = outputSplit(inward_dtl.set_ECFInvoiceheader(), 1)
        return JsonResponse(out, safe=False)

def ECFInvoice_get(request):
    if request.method == 'POST':
        invoice_get = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        invoice_get.action = jsondata.get('params').get('action')
        invoice_get.ecfnumber = jsondata.get('params').get('ecfnumber')
        invoice_get.supplier_gid = jsondata.get('params').get('supplier_gid')
        invoice_get.inwarddetail_gid = jsondata.get('params').get('inwarddetail_gid')
        invoice_get.inwardheader_gid = jsondata.get('params').get('inwardheader_gid')
        invoice_get.status = jsondata.get('params').get('status')
        invoice_get.entity_gid = request.session['Entity_gid']
        invoice_get.state_gid = request.session['Entity_state_gid']
        out = invoice_get.ECFInvoice_get()
        jdata = out.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def Ecf_billentry(request):
    return render(request, "ECF_billentry.html")

def ECFInvoice_set(request):
    if request.method == 'POST':
        inward_dtl = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        inward_dtl.action = jsondata.get('params').get('action')
        inward_dtl.type = jsondata.get('params').get('type')
        inward_dtl.header_json = jsondata.get('params').get('header_json')
        inward_dtl.detail_json = jsondata.get('params').get('detail_json')
        inward_dtl.invoice_json = jsondata.get('params').get('invoice_json')
        inward_dtl.debit_json = jsondata.get('params').get('debit_json')
        inward_dtl.credit_json = jsondata.get('params').get('credit_json')
        inward_dtl.status_json = jsondata.get('params').get('status_json')
        inward_dtl.entity_gid = request.session['Entity_gid']
        inward_dtl.employee_gid = request.session['Emp_gid']
        out = outputSplit(inward_dtl.ECFset_Invoice(), 1)
        return JsonResponse(out, safe=False)

def ECFPOinvoicemk(request):
    return render(request, "ECF_POinvoicemk.html")

def ECFApproval(request):
    return render(request, "ECF_ApprovalSummary.html")

def ECFInvoiceChecker_get(request):
    if request.method == 'POST':
        invoice_get = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        invoice_get.action = jsondata.get('params').get('action')
        invoice_get.ecfnumber = jsondata.get('params').get('ecfnumber')
        invoice_get.supplier_gid = jsondata.get('params').get('supplier_gid')
        invoice_get.inwarddetail_gid = jsondata.get('params').get('inwarddetail_gid')
        invoice_get.inwardheader_gid = jsondata.get('params').get('inwardheader_gid')
        invoice_get.status = jsondata.get('params').get('status')
        invoice_get.entity_gid = request.session['Entity_gid']
        invoice_get.state_gid = request.session['Entity_state_gid']
        out = invoice_get.ECFInvoice_get()
        out =  out.fillna(0)
        if  invoice_get.action == 'INVOICE_DETAILS_EDIT':
            df_invoice = (out[['invoicedetails_gid','invoicedetails_item', 'invoicedetails_desc',
                               'invoicedetails_hsncode','invoicedetails_unitprice','invoicedetails_qty','invoicedetails_sgst',
                               'invoicedetails_cgst','invoicedetails_igst','invoicedetails_amount','invoicedetails_totalamt']]).groupby(
                ['invoicedetails_gid','invoicedetails_item', 'invoicedetails_desc','invoicedetails_hsncode',
                 'invoicedetails_unitprice','invoicedetails_qty','invoicedetails_sgst',
                               'invoicedetails_cgst','invoicedetails_igst','invoicedetails_amount','invoicedetails_totalamt']).size().reset_index();
            df_debit = out.groupby(
                ['invoicedetails_gid','debit_gid', 'debit_categorygid', 'debit_subcategorygid',
                              'debit_glno','debit_amount','ccbsjsondata']).size().reset_index()
            df_credit = (out[['credit_gid', 'credit_paymodegid', 'credit_refno','bankbranch_ifsccode',
                         'credit_glno','credit_amount','Paymode_name','bankdetails_beneficiaryname','credit_suppliertaxtrate','suppliertax_panno','credit_suppliertaxtype',
                              'ppxdetails_ppxheadergid','ppxdetails_gid','bankbranch_name']]).groupby(
                ['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                 'credit_glno','credit_amount','Paymode_name','bankdetails_beneficiaryname','credit_suppliertaxtrate','suppliertax_panno','credit_suppliertaxtype',
                 'ppxdetails_ppxheadergid','ppxdetails_gid','bankbranch_name']).size().reset_index();
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankbranch_ifsccode'] = ''
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankdetails_beneficiaryname'] = ''
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankbranch_name'] = ''
        else:
            df_invoice = (out[['invoicedetails_gid', 'invoicedetails_item', 'invoicedetails_desc',
                               'invoicedetails_hsncode', 'invoicedetails_unitprice', 'invoicedetails_qty',
                               'invoicedetails_sgst',
                               'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount',
                               'invoicedetails_totalamt']]).groupby(
                ['invoicedetails_gid', 'invoicedetails_item', 'invoicedetails_desc', 'invoicedetails_hsncode',
                 'invoicedetails_unitprice', 'invoicedetails_qty', 'invoicedetails_sgst',
                 'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount',
                 'invoicedetails_totalamt']).size().reset_index();
            df_debit = out.groupby(
                ['invoicedetails_gid', 'debit_gid', 'debit_categorygid', 'debit_subcategorygid',
                 'debit_glno', 'debit_amount','ccbsjsondata']).size().reset_index();
            df_credit = (out[['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname','ppxdetails_ppxheadergid','ppxdetails_gid','bankbranch_name'
                              ]]).groupby(
                ['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                 'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname','ppxdetails_ppxheadergid','ppxdetails_gid','bankbranch_name'
                 ]).size().reset_index();
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankbranch_ifsccode'] = ''
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankdetails_beneficiaryname'] = ''
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankbranch_name'] = ''

        data = {}
        data['invoice'] = json.loads(df_invoice.to_json(orient='records'))
        data['debit'] = json.loads(df_debit.to_json(orient='records'))
        data['credit'] = json.loads(df_credit.to_json(orient='records'))
        jdata = data
        return JsonResponse(jdata, safe=False)

def APECF_entry(request):
    return render(request, "AP_ECFbillentry.html")

def ECFSummary(request):
    return render(request,"ECF_Summary.html")

def ECF_ApChecker_get(request):
    if request.method == 'POST':
        invoice_get = mAP.ap_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        invoice_get.action = jsondata.get('params').get('action')
        invoice_get.ecfnumber = jsondata.get('params').get('ecfnumber')
        invoice_get.supplier_gid = jsondata.get('params').get('supplier_gid')
        invoice_get.inwarddetail_gid = jsondata.get('params').get('inwarddetail_gid')
        invoice_get.inwardheader_gid = jsondata.get('params').get('inwardheader_gid')
        invoice_get.status = jsondata.get('params').get('status')
        invoice_get.entity_gid = request.session['Entity_gid']
        invoice_get.state_gid = request.session['Entity_state_gid']
        out = invoice_get.ECFInvoice_get()
        out =  out.fillna(0)
        if  invoice_get.action == 'ECF_DETAILS_EDIT':
            df_invoice = (out[['invoicedetails_gid','invoicedetails_item', 'invoicedetails_desc',
                               'invoicedetails_hsncode','invoicedetails_unitprice','invoicedetails_qty','invoicedetails_sgst',
                               'invoicedetails_cgst','invoicedetails_igst','invoicedetails_amount','invoicedetails_totalamt','DEBIT_DETAILS','ppxx',
                               'ecfinvoicepo_poheadergid','ecfinvoicepo_podetailsgid','ecfinvoicepo_grninwardheadergid','ecfinvoicepo_grninwarddetailsgid','ecfinvoicepo_qty']]).groupby(
                ['invoicedetails_gid','invoicedetails_item', 'invoicedetails_desc','invoicedetails_hsncode',
                 'invoicedetails_unitprice','invoicedetails_qty','invoicedetails_sgst',
                               'invoicedetails_cgst','invoicedetails_igst','invoicedetails_amount','invoicedetails_totalamt','DEBIT_DETAILS','ppxx',
                 'ecfinvoicepo_poheadergid','ecfinvoicepo_podetailsgid','ecfinvoicepo_grninwardheadergid','ecfinvoicepo_grninwarddetailsgid','ecfinvoicepo_qty']).size().reset_index();
            # df_debit = out.groupby(
            #     ['invoicedetails_gid','debit_gid', 'debit_categorygid', 'debit_subcategorygid',
            #                   'debit_glno','debit_amount','ccbsjsondata']).size().reset_index()
            df_credit = (out[['credit_gid', 'credit_paymodegid', 'credit_refno','bankbranch_ifsccode',
                         'credit_glno','credit_amount','Paymode_name','bankdetails_beneficiaryname','credit_suppliertaxtrate','suppliertax_panno','credit_suppliertaxtype',
                              'ppxdetails_ppxheadergid','ppxdetails_gid','bankbranch_name','ppxheadergid','ppxheader_crno']]).groupby(
                ['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                 'credit_glno','credit_amount','Paymode_name','bankdetails_beneficiaryname','credit_suppliertaxtrate','suppliertax_panno','credit_suppliertaxtype',
                 'ppxdetails_ppxheadergid','ppxdetails_gid','bankbranch_name','ppxheadergid','ppxheader_crno']).size().reset_index();
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankbranch_ifsccode'] = ''
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankdetails_beneficiaryname'] = ''
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankbranch_name'] = ''
        else:
            df_invoice = (out[['invoicedetails_gid', 'invoicedetails_item', 'invoicedetails_desc',
                               'invoicedetails_hsncode', 'invoicedetails_unitprice', 'invoicedetails_qty',
                               'invoicedetails_sgst',
                               'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount','invoicedetails_totalamt','DEBIT_DETAILS',
                               'ecfinvoicepo_poheadergid','ecfinvoicepo_podetailsgid','ecfinvoicepo_grninwardheadergid','ecfinvoicepo_grninwarddetailsgid','ecfinvoicepo_qty']]).groupby(
                ['invoicedetails_gid', 'invoicedetails_item', 'invoicedetails_desc', 'invoicedetails_hsncode',
                 'invoicedetails_unitprice', 'invoicedetails_qty', 'invoicedetails_sgst',
                 'invoicedetails_cgst', 'invoicedetails_igst', 'invoicedetails_amount','invoicedetails_totalamt','DEBIT_DETAILS',
                               'ecfinvoicepo_poheadergid','ecfinvoicepo_podetailsgid','ecfinvoicepo_grninwardheadergid','ecfinvoicepo_grninwarddetailsgid','ecfinvoicepo_qty']).size().reset_index();
            # df_debit = out.groupby(
            #     ['invoicedetails_gid', 'debit_gid', 'debit_categorygid', 'debit_subcategorygid',
            #      'debit_glno', 'debit_amount','ccbsjsondata']).size().reset_index();
            df_credit = (out[['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname','ppxdetails_ppxheadergid','ppxdetails_gid','bankbranch_name'
                              ,'ppxheadergid','ppxheader_crno']]).groupby(
                ['credit_gid', 'credit_paymodegid', 'credit_refno', 'bankbranch_ifsccode',
                 'credit_glno', 'credit_amount', 'Paymode_name', 'bankdetails_beneficiaryname','ppxdetails_ppxheadergid','ppxdetails_gid','bankbranch_name'
                 ,'ppxheadergid','ppxheader_crno']).size().reset_index();
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankbranch_ifsccode'] = ''
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankdetails_beneficiaryname'] = ''
            df_credit.loc[df_credit['Paymode_name'] != 'NEFT' ,  'bankbranch_name'] = ''

        data = {}

        data['invoice'] = json.loads(df_invoice.to_json(orient='records'))
       # data['debit'] = json.loads(df_debit.to_json(orient='records'))
        data['credit'] = json.loads(df_credit.to_json(orient='records'))
        jdata = data
        #jdata = json.dumps(jdata)
        #print(type(jdata))
        #jdata = jdata.replace("\\", '')
        #jdata = json.loads(jdata)
        return JsonResponse(jdata, safe=False)


def Ap_EmployeeQuery(request):
    return render(request, "Ap_EmployeeQuery.html")