from typing import Dict

from django.shortcuts import render

from Bigflow import settings
from Bigflow.Purchase.Model import mPurchase
from django.http import JsonResponse, HttpResponse
import json
import ast
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import Bigflow.Core.models as common
import requests
from Bigflow.Report.Model import mStock
from PyPDF2 import PdfFileWriter, PdfFileReader
from Bigflow.API import view_sales
import io
from reportlab.pdfgen import canvas
from rest_framework.response import Response
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.pagesizes import A4
ip = common.localip()
# token = common.token()
headers = {"content-type": "application/json", "Authorization": "" + common.token() + ""}
# ip = common.localip()
token = common.token()

#agentsummary
def agentsummary(request):
    return render(request, "Agent_summary.html")

def open_po(request):
    return render(request, "open_po.html")

def prheader_ccbs(request):
    return render(request, "pur_prheader_ccbs_popup.html")

def po_delievery_popup(request):
    return render(request, "po_delievery_popup.html")

def delmat(request):
    return render(request, "pur_delmatscreen.html")

def adddelmat(request):
    return render(request, "pur_Adddelmat.html")

def purchasesmry(request):
    return render(request, "pur_PurchaseSummary.html")

def expense_line_summary(request):
    return render(request, "expense_line_summary.html")

def expense_line_maker(request):
    return render(request, "expense_line_maker.html")

def purchasecrte(request):
    return render(request, "pur_PurchaseCreate.html")


def vendorselection(request):
    return render(request, "pur_vendorselection.html")
def purchase(request):
    return render(request, "purchasert.html")


def approvalsmry(request):
    return render(request, "pur_ApprovalSummary.html")

def codegenerationviews(request):
    #code generation
    code='CMD0001'

    return HttpResponse(code)


def approvalview(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        objdata = mPurchase.Purchase_model()

        objdata.commodity_gid= json.dumps(jsondata.get('params'))
        objdata.action= jsondata.get('action')
        objdata.type= jsondata.get('type')
        objdata.limitamut= 0
        value = request.session['Entity_gid']
        objdata.entity_gid  = json.dumps({"Entity_Gid": value})
        delmatlimit = objdata.delmatlimit()
        # jdata = delmatlimit.to_json(orient='records')

        if jsondata.get('commodity_name') != None:
            deal= jsondata.get('commodity_name')
            df1=pd.DataFrame(delmatlimit)

            df2 = df1[df1['commodity_name'].astype(str).str[:].str.contains(deal, na=False, case=False)]
            df3 = pd.concat([df2, df1])
            df3 = df3.drop_duplicates(keep=False)
            df4 = pd.concat([df2, df3])
            df4.drop_duplicates(keep=False)
            df4= df4.drop_duplicates(subset=['employee_code'], keep='first')
            df4.loc[df4.commodity_name !=deal,'delmat_limit']=''

            jdata = df4.to_json(orient='records')

        return JsonResponse(jdata, safe=False)


    else:
        return render(request, "pur_ApprovalView.html")

def tranapproval(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        objdata = mPurchase.Purchase_model()
        objdata.data = json.dumps(jsondata)
        objdata.action = 'INSERT_PR'
        objdata.ref_gid =jsondata.get('li_ref_gid')
        objdata.totype = jsondata.get('lc_totype')
        objdata.reftable = jsondata.get('li_reftable_gid')
        objdata.status = jsondata.get('ls_status')
        objdata.to = jsondata.get('li_tto')
        objdata.remark = jsondata.get('ls_remarks')
        objdata.Employee_gid = request.session['Emp_gid']
        objdata.entity_gid = request.session['Entity_gid']
        tran = objdata.set_trans()
        return JsonResponse(tran[0], safe=False)
        # jdata = tran.to_json(orient='records')
        # return JsonResponse(jdata, safe=False)

# def basedonlogin(request):
#     if request.method == 'POST':
#         jsondata = json.loads(request.body.decode('utf-8'))
#         objdata = mPurchase.Purchase_model()


def po_ammentsummry(request):
    return render(request, "pur_poadmentsummary.html")

def po_headerget_view(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        objdata = mPurchase.Purchase_model()
        objdata.type=jsondata.get('Type')
        objdata.filter_json = json.dumps(jsondata.get('data').get('Params').get('FILTER'))
        objdata.classification_json = json.dumps(jsondata.get('data').get('Params').get('CLASSIFICATION'))
        objdata.create_by = request.session['Emp_gid']
        obj_cancel_data = objdata.getPoheader_details()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def prfinalapproval(request):
    return render(request, "pur_Finalapproval.html")


def po_ammentcreate(request):
    return render(request, "pur_poadmentcreate.html")


def po_ammentapprovalcreate(request):
    return render(request, "pur_poadmentapprovalcreate.html")


def po_ammentapprovalsummry(request):
    return render(request, "pur_poadmentapprovalsummary.html")

def getfinalapproval(request):
    if request.method == 'GET':
        objdata = mPurchase.Purchase_model()
        obj_cancel_data = objdata.getfinalapprovalget()
        obj_cancel_data['ccbs_details'] = obj_cancel_data['ccbs_details'].apply(json.loads)
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)



#insert pr ccbs data
def saveccbs(request):
    if request.method == 'POST':
        objdata = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        objdata.action =jsondata.get('Action')
        objdata.type =jsondata.get('Type')
        objdata.prdetailsgid =jsondata.get('prdetailsgid')
        objdata.prheaderddl =json.dumps(jsondata.get('PR_Header'))
        prproductddl =jsondata.get('PR_Products')
        objdata.productsddl=json.dumps(prproductddl)
        objdata1 = request.session['Entity_gid']
        objdata.emp = request.session['Emp_gid']
        objdata.draft=json.dumps({"Entity_Gid":[objdata1]})
        objdata.classification_json=json.dumps({"Entity_Gid":[objdata1]})
        obj_data = objdata.insertprccbs()
        return HttpResponse(obj_data)
        # return JsonResponse(jdata, safe=False)

def po_querystring(request):
    return render(request, "pur_querystring.html")
#Delmat Save
def delmatsavedatas(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        array=jsondata.get('array')
        crtby = jsondata.get('CLASSIFICATION').get('Create_By')
        value = jsondata.get('CLASSIFICATION').get('Entity_Gid')
        enty=json.dumps({"entity_gid":value})
        action='insert'
        type='pr_multi'
        params = {'Action': "" + action + "", 'Type': "" + type + "",
                  'Entity_Gid': "" + enty + "",'Employee_Gid':""+ str(crtby) +"" }
        # headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(array)
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Delmat_set", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
#delmatapproval
def delmatapproval(request):
    return render(request, "pur_delmatapproval.html")
#delmatapprovalsmry
def delmatapprovalsmry(request):
    return render(request, "pur_delmatapprovalsmry.html")


#Delmat Get
def delmatget(request):
      if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        e = request.session['Entity_gid']
        enty=json.dumps({"entity_gid":e})
        #action='get'
        params = {'Action': "" + jsondata.get('Action') + "",
                  'Entity_Gid': "" + enty + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Delmat_set", params=params,headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
#Delmat Update
def delmatupdate(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        crtby = request.session['Emp_gid']
        value = request.session['Entity_gid']
        enty=json.dumps({"entity_gid":value})
        action='update'
        type='pr_update'
        params = {'Action': "" + action + "", 'Type': "" + type + "",
                  'Entity_Gid': "" + enty + "",'Employee_Gid':""+ str(crtby) +"" }
        # headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata )
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Delmat_set", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

# get delmat type
def delmattype(request):
       if request.method == 'GET':
           objdata = mPurchase.Purchase_model()
           objdata.entity_gid=request.session['Entity_gid']
           objdata.data='{"Table_name": "gal_mst_tmetadata","Column_1": "metadata_gid,metadata_tablename,metadata_columnname,metadata_value","Column_2": "","Where_Common": "metadata","Where_Primary": "columnname","Primary_Value": "delmat_tran","Order_by": "gid"}'
           obj_cancel_data = objdata.getdelmattype()
           jdata = obj_cancel_data.to_json(orient='records')
           return JsonResponse(jdata, safe=False)



#All table value for ccbs
def alltable(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        # value = request.session['Entity_gid']
        obj = mPurchase.Purchase_model()
        obj.actn = ''
        obj.entity_gid = json.dumps(request.session['Entity_gid'])
        params = {'Action': "" + obj.actn + "", 'Entity_Gid': "" + obj.entity_gid + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata)
        resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        # object_query.action = ''
        # object_query.enty =value
        # enty=json.dumps({"entity_gid":value})
        # action=''
        # params = {'Action': "" + action + "",
        #           'Entity_Gid':value }
        # datas = json.dumps(jsondata)
        # headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        # resp = requests.post("" + ip + "/Alltable_ccbs", params=params, data=datas, headers=headers, verify=False)
        # response = resp.content.decode("utf-8")

        # jdata = ld_out_message.to_json(orient='records')
        return JsonResponse(response, safe=False)





def trandatadetails1(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        action = jsondata.get('Action')
        type = jsondata.get('Type')
        classification = jsondata.get('classification')
        main = json.dumps(jsondata.get('Main_data'))
        params = {'Action': "" + action + "",
                  'Type': "" +type + "",'classification': "" +classification + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}

        resp = requests.post("" + ip + "/Agaentsmry", params=params, data=main, headers=headers)
        response = resp.content.decode("utf-8")
        return JsonResponse(response, safe=False)


#branchresult
def branchresult(request):
    if request.method == 'POST':
        objdata = mPurchase.Purchase_model()
        objdata.entity_gid = request.session['Entity_gid']
        objdata.data ='{"Table_name": "gal_mst_tbranch","Column_1": "branch_gid,branch_code,branch_name","Column_2": "","Where_Common": "branch","Where_Primary": "","Primary_Value": "","Order_by": "gid"}'
        obj_cancel_data = objdata.getdelmattype()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)
def reftable(request):
    if request.method == 'POST':
        objdata = mPurchase.Purchase_model()
        objdata.entity_gid = request.session['Entity_gid']
        obj_cancel_data = objdata.Reftable_Get()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)

def pending_posummary(request):
     if request.method == 'POST':
         objdata = mPurchase.Purchase_model()
         jsondata = json.loads(request.body.decode('utf-8'))
         objdata.Type = jsondata.get('Type')
         objdata.SubType = jsondata.get('SubType')
         objdata.darta = jsondata.get('darta')
         objdata.entity_gid = request.session['Entity_gid']
         obj_cancel_data = objdata.pending_posummary()
         jdata = obj_cancel_data.to_json(orient='records')
         return JsonResponse(jdata, safe=False)


def New_delmat_Get(request):
    if request.method == 'POST':
        objdata = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        objdata.Type = jsondata.get('Type')
        objdata.filter_json = json.dumps(jsondata.get('data').get('Params').get('FILTER'))
        objdata.json_classification = json.dumps(jsondata.get('data').get('Params').get('CLASSIFICATION'))
        #objdata.entity_gid = request.session['Entity_gid']
        objdata.create_by = request.session['Emp_gid']
        obj_cancel_data = objdata.New_delmatget()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def Prdraftdata(request):
    if request.method == 'POST':
        objdata = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        # objdata.Type = jsondata.get('Type')
        objdata.filter_json = json.dumps(jsondata.get('params'))
        # objdata.json_classification = json.dumps(jsondata.get('data').get('Params').get('CLASSIFICATION'))
        # objdata.entity_gid = request.session['Entity_gid']
        objdata.create_by = request.session['Emp_gid']
        obj_data = objdata.getdraftddl()
        jdata = obj_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

# Export openpo excel
def openpo_getexcel(request):
    if request.method == 'GET':
        obj_master =  mPurchase.Purchase_model()
        obj_master.Type ='SUMMARY'
        obj_master.SubType = 'OPENPO'
        obj_master.darta ={

            'Supplier_Gid':'',
            'Po_No': '',
            'Product_Gid': '',
            'From_Date': '',
            'To_Date':''
        }
        obj_master.entity_gid = request.session['Entity_gid']
        obj_master.jsonData = json.dumps({"entity_gid": [request.session['Entity_gid']]})
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        response['Content-Disposition'] = 'attachment; filename="Openpo.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view = obj_master.pending_posummary()
        final_df = df_view[['poheader_no', 'poheader_date', 'supplier_name', 'product_name', 'total_qty',  'allreceive_qty','rem_qty']]
        final_df.columns= ['PO Number', 'PO Date', 'Supplier Name', 'Product Name', 'Ordered Quantity','Received Quantity','Remaining Quantity']
        #convert proper df type
        final_df[['Received Quantity','Remaining Quantity']]=  final_df[['Received Quantity','Remaining Quantity']].apply(pd.to_numeric)
        final_df=final_df.sort_values(by=['PO Number'])
        final_df.to_excel(writer, index=False)
        writer.save()
        return response


def purchasesmryget(request):
    if request.method == 'GET':
        obj_purchase_get = mPurchase.Purchase_model()
        obj_purchase_get.serail_no = ''
        obj_purchase_get.status = ''
        obj_purchase_get.action = 'get'

        obj_purchase_get.Employee_gid = request.session['Emp_gid']
        obj_purchase_get.entity = request.session['Entity_gid']
        entity = request.session['Entity_gid']
        obj_purchase_get.egid = json.dumps({'entity_gid': entity})
        obj_purchase_get.data = json.dumps({'prheader_employee_gid': obj_purchase_get.Employee_gid})

        df_preschedule = obj_purchase_get.get_prheader()
        jdata = df_preschedule.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def purcappsryget(request):
    if request.method == 'GET':
        obj_purchase_get = mPurchase.Purchase_model()
        obj_purchase_get.serail_no = ''
        obj_purchase_get.status = ''
        obj_purchase_get.Employee_gid = request.session['Emp_gid']
        df_preschedule = obj_purchase_get.get_prheader()
        jdata = df_preschedule.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def pur_poclosesummary(request):
    if request.method == 'GET':
        obj_purchase_get = mPurchase.Purchase_model()
        obj_purchase_get.serail_no = ''
        obj_purchase_get.supplier_name = ''
        obj_purchase_get.amount = '0.00'
        obj_purchase_get.status = ''
        df_poclosesummary = obj_purchase_get.get_pocolse()
        jdata = df_poclosesummary.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def pur_pocloseappsummary(request):
    if request.method == 'GET':
        obj_purchase_get = mPurchase.Purchase_model()
        obj_purchase_get.serail_no = ''
        obj_purchase_get.amount = '0.00'
        obj_purchase_get.status = ''
        obj_purchase_get.Employee_gid = '0';
        df_pocloseapp = obj_purchase_get.get_pocloseapproval()
        jdata = df_pocloseapp.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def pur_poreopensummary(request):
    if request.method == 'GET':
        obj_purchase_get = mPurchase.Purchase_model()
        obj_purchase_get.serail_no = ''
        obj_purchase_get.amount = '0.00'
        obj_purchase_get.status = ''
        obj_purchase_get.Employee_gid = 0
        df_pocloseapp = obj_purchase_get.get_poreopen()
        jdata = df_pocloseapp.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def poclosesmry(request):
    return render(request, "pur_PoCloseSummary.html")


def poclosecrte(request):
    return render(request, "pur_PoCloseCreate.html")


def pocancelsmry(request):
    if request.method == 'POST':
        obj_cancel_data = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_cancel_data.Employee_gid = request.session['Emp_gid']
        obj_cancel_data.poheader_gid = jsondata.get('params').get('poheader_gid')
        obj_cancel_data.supplier_name = jsondata.get('params').get('supplier_name')
        obj_cancel_data.amount = jsondata.get('params').get('amount')
        obj_cancel_data.status = jsondata.get('params').get('status')
        obj_cancel_data.Employee_gid = 0
        data = obj_cancel_data.get_pocancel()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)
    else:
        return render(request, "pur_PoCancelSummary.html")


def pocancelcrte(request):
    return render(request, "pur_PoCancelCreate.html")


def poreopensmry(request):
    return render(request, "pur_PoReopenSummary.html")


def poreopencrte(request):
    return render(request, "pur_PoReopenCreate.html")


def poapprvlclssmry(request):
    return render(request, "pur_PoApprovalCloseSummary.html")


def poapprvlclscrt(request):
    return render(request, "pur_PoApprovalCloseCreate.html")


def poapprvlcnclsmry(request):
    if request.method == 'POST':
        obj_cancel_data = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_cancel_data.serail_no = jsondata.get('params').get('serail_no')
        obj_cancel_data.amount = jsondata.get('params').get('amount')
        obj_cancel_data.status = jsondata.get('params').get('status')
        obj_cancel_data.Employee_gid = 0
        data = obj_cancel_data.get_pocancelapproval()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)
    else:
        return render(request, "pur_PoApprovalCancelSummary.html")


def poapprvlcnclcrt(request):
    return render(request, "pur_PoApprovalCancelCreate.html")



#open po edit
def openpo_edit(request):
    return render(request, "pur_openpo_edit.html")

#pdfviewer2
def pdfviewer2(request):
    return render(request, "demo.html")

#pdfviewer
def pdfviewer(request):
    return render(request, "Pdfviewer.html")

#pdfeditor
def pdfedit(request):
    jsondata=json.loads(request.body.decode('utf-8'))
    # jsondata=request.GET['Main']
    top = jsondata.get('top')
    left=jsondata.get('left')
    txt=jsondata.get('value')


    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(top, left, txt)
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(str(settings.MEDIA_ROOT) + '/destination4.pdf', "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(str(settings.MEDIA_ROOT) + '/pod/pl454.pdf', "wb")
    output.write(outputStream)
    outputStream.close()
    return JsonResponse(outputStream, safe=False)

def grnsmry(request):
    return render(request, "pur_GrnSummary.html")


def grncreate(request):
    return render(request, "pur_GrnCreate.html")


def grnaprvlsmry(request):
    return render(request, "pur_GrnApprovalSummary.html")


def grnaprvlcreate(request):
    return render(request, "pur_GrnApprovalCreate.html")


def posummary(request):
    return render(request, "pur_POsummary.html")


def createpoindex(request):
    return render(request, "pur_Createpo_index.html")


def Poheader_detail(request):
    if request.method == 'POST':
        obj_header_dtl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_header_dtl.serail_no = jsondata.get('params').get('poheader_sno')
        obj_header_dtl.supplier_name = jsondata.get('params').get('poheader_suppliername')
        obj_header_dtl.amount = jsondata.get('params').get('po_amount')
        obj_header_dtl.status = jsondata.get('params').get('po_status')
        obj_header_dtl.Employee_gid = 0
        data = obj_header_dtl.get_poheader()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def Getpostatus(request):
    if request.method == 'GET':
        obj_status_get = mPurchase.Purchase_model()
        data = obj_status_get.get_postatus()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def POApproval_create(request):
    return render(request, "pur_POapproval_Create.html")


def POApproval_Index(request):
    return render(request, "pur_POapproval_Index.html")


def POApproval_detail(request):
    if request.method == 'POST':
        obj_header_dtl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_header_dtl.serail_no = jsondata.get('params').get('poheader_sno')
        obj_header_dtl.supplier_name = jsondata.get('params').get('poheader_suppliername')
        obj_header_dtl.amount = jsondata.get('params').get('po_amount')
        obj_header_dtl.status = jsondata.get('params').get('po_status')
        obj_header_dtl.Employee_gid = 0
        data = obj_header_dtl.get_poheader()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def Approval_PODetail(request):
    if request.method == 'POST':
        obj_podetail = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_podetail.podetails_gid = jsondata.get('params').get('podetails_gid')
        obj_podetail.product_name = jsondata.get('params').get('product_name')
        obj_podetail.Employee_gid = 0
        data = obj_podetail.get_podetails()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def PODelivery_detail(request):
    if request.method == 'POST':
        obj_delivery = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_delivery.podetails_gid = jsondata.get('params').get('podetails_gid')
        data = obj_delivery.get_delivery()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def Approval_View_Update(request):
    if request.method == 'POST':
        obj_maker = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_maker.action = jsondata.get('params').get('action')
        obj_maker.actionsys = jsondata.get('params').get('actionsys')
        obj_maker.poheader_gid = jsondata.get('params').get('poheader_gid')
        obj_maker.remark = jsondata.get('params').get('remark')
        obj_maker.Employee_gid = request.session['Emp_gid']
        obj_maker.entity_gid = request.session['Entity_gid']
        data = obj_maker.set_poapprovalviewupdate()
        return JsonResponse(json.dumps(data), safe=False)


def Approval_Update(request):
    if request.method == 'POST':
        obj_maker = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_maker.action = jsondata.get('params').get('action')
        obj_maker.poheader_gid = jsondata.get('params').get('poheader_gid')
        obj_maker.remark = ' ' if jsondata.get('params').get('remark') == None else jsondata.get('params').get('remark')
        obj_maker.entity_gid = request.session['Entity_gid']
        obj_maker.Employee_gid = request.session['Emp_gid']
        data = obj_maker.set_poapprovalupdate()[0].split(',')
        return JsonResponse(json.dumps(data[1]), safe=False)

def Prapproval_get(request):
   if request.method == 'POST':
       obj_prapproval = mPurchase.Purchase_model()
       jdata = json.loads(request.body.decode('utf-8'))
       obj_prapproval.empcode = jdata.get('empcode')
       obj_prapproval.action = jdata.get('Action')
       obj_prapproval.enty = request.session['Entity_gid']
       df_prapproval = obj_prapproval.get_prapproval()
       jdata = df_prapproval.to_json(orient='records')
       return JsonResponse(json.loads(jdata), safe=False)


def pr_po_delete(request):
    if request.method == 'POST':
        obj_prapproval = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_prapproval.action = jsondata.get('action')
        obj_prapproval.data = json.dumps(jsondata.get('data'))
        value = request.session['Entity_gid']
        obj_prapproval.enty = json.dumps({"entity_gid": value})
        obj_prapproval.Employee_gid = json.dumps(request.session['Emp_gid'])
        tran = obj_prapproval.pr_po_delete()
        # jdata = tran.to_json(orient='records')
        return JsonResponse(json.dumps(tran), safe=False)



def Prdetail_get(request):
    if request.method == 'POST':
        obj_prapproval = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_prapproval.prheader_gid = jsondata.get('params').get('prheader_gid')
        obj_prapproval.product_name = jsondata.get('params').get('product_name')
        obj_prapproval.action = jsondata.get('params').get('action')
        obj_prapproval.Employee_gid = request.session['Emp_gid']
        obj_prapproval.entity_gid = request.session['Entity_gid']
        df_prdetails = obj_prapproval.get_prdetails()
        jdata = df_prdetails.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def Dropdown_details(request):
    if request.method == 'POST':
        dropdown = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        dropdown.tablename = jsondata.get('params').get('tablename')
        dropdown.gid = jsondata.get('params').get('gid')
        dropdown.name = jsondata.get('params').get('name')
        dropdown.entity_gid = request.session['Entity_gid'];
        data = dropdown.get_dropdown_details()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def product_name(request):
    if request.method == 'POST':
        productname = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        productname.action = 'Date_wise'
        productname.date = common.convertdbDate(request.session['date'])
        productname.supplier_gid = jsondata.get('params').get('supplier_gid')
        productname.product_gid = jsondata.get('params').get('product_gid')
        productname.char_active = jsondata.get('params').get('char_active')
        data = productname.get_productnames()
        data['stategid'] = request.session['Entity_state_gid']
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def POQtyList(request):
    if request.method == 'POST':
        polist = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        polist.action = jsondata.get('params').get('action')
        polist.supplier_gid = jsondata.get('params').get('supplier_gid')
        polist.product_gid = jsondata.get('params').get('product_gid')
        polist.product_name = jsondata.get('params').get('product_name')
        polist.serail_no = jsondata.get('params').get('serial_no')
        data = polist.get_poqty()
        data = data[data['req_qty'] > 0]
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def supplier_details(request):
    if request.method == 'POST':
        suplierdetails = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        suplierdetails.action = jsondata.get('params').get('action')
        suplierdetails.type = jsondata.get('params').get('type')
        suplierdetails.vendor = jsondata.get('params').get('product_gid')
        data = suplierdetails.get_supplier()
        data['stategid'] = request.session['Entity_state_gid']
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def poreject(request):
    if request.method == 'POST':
        obj_maker = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_maker.Type = jsondata.get('Type')
        obj_maker.actionsys = jsondata.get('Sub_Type')
        obj_maker.lj_filters = json.dumps(jsondata.get('data').get('Params').get('FILTER'))
        obj_maker.lj_classification = json.dumps(jsondata.get('data').get('Params').get('CLASSIFICATION'))
        data = obj_maker.set_poreject()
        return JsonResponse(json.dumps(data), safe=False)


def Poapproval_get(request):
   if request.method == 'GET':
       obj_prapproval = mPurchase.Purchase_model()
       obj_prapproval.serial_no = ''
       obj_prapproval.status = ''
       obj_prapproval.login_gid = request.session['Emp_gid']
       df_prapproval = obj_prapproval.gett_poapproval()
       jdata = df_prapproval.to_json(orient='records')
       return JsonResponse(json.loads(jdata), safe=False)

#PONEWAPPROVAL_SET
def ponewapproval_set(request):
    if request.method == 'POST':
        suplierdetails = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        suplierdetails.action = jsondata.get('Action')
        suplierdetails.header_gid = jsondata.get('data').get('Params').get('FILTER').get('li_POHeader_gid')
        suplierdetails.remarks = jsondata.get('data').get('Params').get('FILTER').get('ls_remarks')
        suplierdetails.employee_name = jsondata.get('data').get('Params').get('FILTER').get('emp_name')
        suplierdetails.li_ref_gid = jsondata.get('data').get('Params').get('FILTER').get('li_ref_gid')
        suplierdetails.ls_status = jsondata.get('data').get('Params').get('FILTER').get('ls_status')
        suplierdetails.lc_totype = jsondata.get('data').get('Params').get('FILTER').get('lc_totype')
        suplierdetails.li_tto = jsondata.get('data').get('Params').get('FILTER').get('li_tto')
        suplierdetails.entity_gid = jsondata.get('data').get('Params').get('CLASSIFICATION').get('li_entity_gid')
        suplierdetails.create_by = jsondata.get('data').get('Params').get('CLASSIFICATION').get('ls_update_by')
        jdata = suplierdetails.set_ponewapproval()
        #print(jdata)
        if jdata[0] == 'Success':
            temp='Poheader is Updated Successfully'
        else:
            temp='Poheader Update is Failed'
            return JsonResponse(temp, safe=False)
        if temp == 'Poheader is Updated Successfully':
            suplierdetails.type='INSERT'
            suplierdetails.subtype='pr_trans'
            suplierdetails.filter_json={"li_ref_gid":suplierdetails.li_ref_gid,
                                        "li_reftable_gid":suplierdetails.header_gid,
                                        "ls_status":suplierdetails.ls_status,
                                        "lc_totype":suplierdetails.lc_totype,
                                        "li_tto":suplierdetails.li_tto,
                                        "ls_remarks":""
                                        }
            suplierdetails.classification_json={
                                        "Entity_Gid":request.session['Entity_gid'],
                                        "Create_by":request.session['Emp_gid']
                                        }

            tran = suplierdetails.tranapp1()
            if tran[0] == 'Partially Completed' or tran[0] == 'Action Completed' or tran[0] == 'FAIL':
               return JsonResponse(tran, safe=False)
            else:
                return JsonResponse("Error on"+tran, safe=False)
        #data[0]
        #jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def deliverydetail(request):
    if request.method == 'POST':
        delivery = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        delivery.serail_no = jsondata.get('params').get('serail_no')
        data = delivery.get_podelivery()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def Prapproval_set(request):
    if request.method == 'POST':
        obj_prapproval = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_prapproval.action = jsondata.get('params').get('status_pr')
        obj_prapproval.prheader_gid = jsondata.get('params').get('prheader')
        obj_prapproval.empname = jsondata.get('params').get('empname')

        if jsondata.get('params').get('lsremaks') == None :
            obj_prapproval.remark = ' '
        else:
            obj_prapproval.remark = jsondata.get('params').get( 'lsremaks')
        obj_prapproval.Employee_gid = request.session['Emp_gid']
        obj_prapproval.entity_gid = request.session['Entity_gid']
        data = obj_prapproval.set_prapproval()
        return JsonResponse(json.dumps(data), safe=False)

def Poapproval_set(request):
    if request.method == 'POST':
        obj_prapproval = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_prapproval.action = jsondata.get('params').get('status_pr')
        obj_prapproval.poheader_gid = jsondata.get('params').get('poheader')
        obj_prapproval.empname = jsondata.get('params').get('empname')
        obj_prapproval.lsremaks = jsondata.get('params').get('lsremaks')
        obj_prapproval.Employee_gid = request.session['Emp_gid']
        obj_prapproval.entity_gid = request.session['Entity_gid']
        data = obj_prapproval.set_poapproval()
        return JsonResponse(json.dumps(data), safe=False)


def Prheader_Set(request):
    if request.method == 'POST':
        obj_prdata = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        prdetails = jsondata.get('params').get('prdetails')
        prheader_gid = prdetails[0].get('prheader_gid')
        prdetail_details = jsondata.get('params').get('prdelete')

        if prdetail_details != None:
            for x in prdetail_details:
                obj_prdata.prdetail_gid = x
                obj_prdata.Employee_gid = request.session['Emp_gid']
                data = obj_prdata.set_prdelete()

        if prheader_gid == None:
            obj_prdata.action = jsondata.get('params').get('action')
            obj_prdata.date = datetime.datetime.now().date()
            obj_prdata.Employee_gid = request.session['Emp_gid']
            obj_prdata.status = jsondata.get('params').get('status')
            obj_prdata.entity_gid = request.session['Entity_gid']
            obj_prdata.create_by = request.session['Emp_gid']

            obj_prdata.commodity_gid = jsondata.get('params').get('details').get('commodity_gid')
            obj_prdata.totalamt = jsondata.get('params').get('details').get('totalamt')
            obj_prdata.mepnumber = jsondata.get('params').get('details').get('mepnumber')
            obj_prdata.branchcode = jsondata.get('params').get('details').get('branchcode')
            # for x in prdetails:
            #      obj_prdata.mepnumber =x.get('mep_no')
            #      obj_prdata.branchcode =x.get('branch_gid')

            data = obj_prdata.set_prheader()[0].split(',')

            if data != "Error":
                for x in prdetails:
                    obj_prdata.prheader_gid = data[0]
                    obj_prdata.product_gid = x.get('product_gid')
                    obj_prdata.product_qty = x.get('prdetails_qty')
                    obj_prdata.supplier_gid = x.get('supplier_gid')
                    obj_prdata.Employee_gid = request.session['Emp_gid']
                    obj_prdata.entity_gid = request.session['Entity_gid']
                    data1 = obj_prdata.set_prdetails()[0].split(',')
                # return JsonResponse(json.dumps(data1[1]), safe=False)


            if obj_prdata.status =='Pending For Approval':
                obj_prdata.action = 'INSERT_PR'
                obj_prdata.ref_gid = 'pr'
                obj_prdata.reftable = int(data[0])
                obj_prdata.status = 'Pending For Approval'
                obj_prdata.totype = 'I'
                obj_prdata.to = jsondata.get('params').get('details').get('empgid')
                obj_prdata.remark = ''
                obj_prdata.Employee_gid = request.session['Emp_gid']
                obj_prdata.entity_gid = request.session['Entity_gid']
                tran = obj_prdata.set_trans()
                #self.action, self.prheader_gid, self.remark,self.empname,self.entity_gid, self.Employee_gid, ''
                obj_prdata.action='Approve'
                obj_prdata. prheader_gid=int(data[0])
                obj_prdata. remark=''
                obj_prdata.empname=jsondata.get('params').get('details').get('empname')
                head = obj_prdata.set_prapproval()
                return JsonResponse(json.dumps(data1[1]), safe=False)
            else :
                return JsonResponse(json.dumps(data1[1]), safe=False)

                # return JsonResponse(json.dumps(data1[1]), safe=False)
            #self.action, self.ref_gid, self.reftable, self.status, self.totype,
            # self.to, self.remark, self.entity_gid, self.Employee_gid
            # if data[0]!=None:
            #     obj_prdata.reftable = data[0]
            #     obj_prdata.action = 'INSERT_PR'
            #     obj_prdata.ref_gid = 'pr'
            #     obj_prdata.status = 'Pending for approval'
            #     obj_prdata.totype = 'I'
            #     obj_prdata.to = jsondata.get('params').get('details').get('empgid')
            #     obj_prdata.entity_gid = request.session['Emp_gid']
            #     obj_prdata.remark = ''
            #     obj_prdata.Employee_gid = request.session['Emp_gid']




                # if obj_prdata.status == "Pending For Approval":
                #     if data1[1] == "SUCCESS":
                #         obj_prdata.action = 'Insert'
                #         obj_prdata.ref_gid = 'PR'
                #         obj_prdata.reftable = obj_prdata.prheader_gid
                #         obj_prdata.status = 'Pending for Approval'
                #         obj_prdata.totype = 'I'
                #         obj_prdata.to = 'MAKER'
                #         obj_prdata.remark = ''
                #         tran = obj_prdata.set_trans()[0].split(',')


        # else:
        #     obj_prdata.action = jsondata.get('params').get('action')
        #     obj_prdata.prheader_gid = prheader_gid
        #     obj_prdata.entity_gid = request.session['Entity_gid']
        #     obj_prdata.create_by = request.session['Emp_gid']
        #     data = obj_prdata.set_prheaderupdate()[0].split(',')
        #     if data != "Error":
        #         for x in prdetails:
        #             if x.get('prdetails_gid') == None:
        #                 obj_prdata.prheader_gid = prheader_gid
        #                 obj_prdata.product_gid = x.get('product_gid')
        #                 obj_prdata.product_qty = x.get('prdetails_qty')
        #                 obj_prdata.supplier_gid = x.get('supplier_gid')
        #                 obj_prdata.Employee_gid = request.session['Emp_gid']
        #                 obj_prdata.entity_gid = request.session['Entity_gid']
        #                 data1 = obj_prdata.set_prdetails()[0].split(',')
        #             else:
        #                 obj_prdata.prdetail_gid = x.get('prdetails_gid')
        #                 obj_prdata.product_gid = x.get('product_gid')
        #                 obj_prdata.product_qty = x.get('prdetails_qty')
        #                 data1 = obj_prdata.set_prdetailupdate()[0].split(',')
        #
        #         if obj_prdata.status == "Pending for Approval":
        #             if data1[1] == "SUCCESS":
        #                 obj_prdata.action = 'INSERT_PR'
        #                 obj_prdata.ref_gid = 'pr'
        #                 obj_prdata.reftable = obj_prdata.prheader_gid
        #                 obj_prdata.status = 'Pending for Approval'
        #                 obj_prdata.totype = 'I'
        #                 obj_prdata.to = jsondata.get('params').get('details').get('empgid')
        #                 obj_prdata.remark = ''
        #                 obj_prdata.Employee_gid = request.session['Emp_gid']
        #                 obj_prdata.entity_gid = request.session['Entity_gid']
        #                 #obj_prdata.reftable = data[0]
        #                 #     obj_prdata.action = 'INSERT_PR'
        #                 #     obj_prdata.ref_gid = 'pr'
        #                 #     obj_prdata.status = 'Pending for approval'
        #                 #     obj_prdata.totype = 'I'
        #                 #     obj_prdata.to = jsondata.get('params').get('details').get('empgid')
        #                 #     obj_prdata.entity_gid = request.session['Emp_gid']
        #                 #     obj_prdata.remark = ''
        #                 #     obj_prdata.Employee_gid = request.session['Emp_gid']
        #
        #                 tran = obj_prdata.set_trans()[0].split(',')
        #
        #         return JsonResponse(json.dumps(data1[1]), safe=False)
        #
        #     else:
        #         return JsonResponse(json.dumps(data), safe=False)


def Prdelete_Set(request):
    if request.method == 'POST':
        obj_prdata = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_prdata.prdetail_gid = jsondata.get('params').get('prdetail_gid')
        obj_prdata.Employee_gid = request.session['Emp_gid']
        data = obj_prdata.set_prdelete()
        return JsonResponse(json.dumps(data), safe=False)


# #PR_to_POheader_Set
# def PR_to_POheader_Set(request):
#     if request.method == 'POST':
#         obj_prdata = mPurchase.Purchase_model()
#         jsondata = json.loads(request.body.decode('utf-8'))
#         podetails = jsondata.get('params').get('podetails')
#         if podetails == []:
#             poheader_gid = '0'
#         else:
#             poheader_gid = podetails[0].get('poheader_gid')
#         if poheader_gid !=0:
#             obj_prdata.action = jsondata.get('params').get('action')
#             obj_prdata.date = datetime.datetime.now().date()
#             obj_prdata.supplier_gid = podetails[0].get('supplier_gid')
#             obj_prdata.teamandcont_gid = podetails[0].get('teamandcont_gid')
#             obj_prdata.amount = jsondata.get('params').get('total_amount')
#             obj_prdata.amement_gid = podetails[0].get('amement_gid')
#             obj_prdata.commodity_gid = podetails[0].get('prheader_commodity_gid')
#             obj_prdata.branchgid = podetails[0].get('branch_gid')
#             obj_prdata.mepno = podetails[0].get('prheader_mepno')
#             obj_prdata.vesion_gid = podetails[0].get('vesion_gid')
#             obj_prdata.from_date = datetime.datetime.strptime(jsondata.get('params').get('from_date'),
#                                                               "%d/%m/%Y").strftime("%Y-%m-%d")
#             obj_prdata.to_date = datetime.datetime.strptime(jsondata.get('params').get('to_date'), "%d/%m/%Y").strftime(
#                 "%Y-%m-%d")
#             obj_prdata.Employee_gid = request.session['Emp_gid']
#             obj_prdata.status = jsondata.get('params').get('status')
#             obj_prdata.entity_gid = request.session['Entity_gid']
#             data = obj_prdata.set_poheader()[0].split(',')
#             for x in podetails:
#                 obj_prdata.poheader_gid = data[0]
#                 obj_prdata.product_gid = x.get('product_gid')
#                 obj_prdata.product_qty = x.get('podetails_qty')
#                 obj_prdata.umo_gid = x.get('podetails_uom')
#                 obj_prdata.per_unitamt = x.get('podetails_unitprice')
#                 obj_prdata.amount = x.get('podetails_amount')
#                 obj_prdata.taxamt = x.get('podetails_taxamount')
#                 obj_prdata.netamount = x.get('podetails_totalamount')
#                 obj_prdata.entity_gid = request.session['Entity_gid']
#                 obj_prdata.Employee_gid = request.session['Emp_gid']
#                 data1 = obj_prdata.set_podetails()[0].split(',')
#                 dataout1 = data1[1].split(',')
#             for x in podetails:
#                 if x.get('prpopty') != None:
#                     prdtlgid = x.get("prdetail_gid")
#                     if prdtlgid == 0 or prdtlgid == None:
#                         prdtlgid = x.get("podetails_gid")
#                         prptgid = x.get("podetails_qty")
#                     if prptgid == 0 or prptgid == None:
#                         prptgid = x.get("podetails_qty1")
#                     # prptgid = int(z.get("prdetails_qty1"))
#                     prdtlgid = x.get("podetail_gid")
#                     obj_prdata.action = 'Insert'
#                     obj_prdata.poheader_gid = data[0]
#                     obj_prdata.podetails_gid = data1[0]
#                     obj_prdata.prdetail_gid = prdtlgid
#                     obj_prdata.product_qty = prptgid
#                     obj_prdata.entity_gid = request.session['Entity_gid']
#                     obj_prdata.Employee_gid = request.session['Emp_gid']
#                     obj_prdata.prpo_gid = x.get("prpo_gid")
#                     data3 = obj_prdata.set_prpoqty()[0].split(',')
#
#                 if obj_prdata.status == 'Approved':
#                     obj_prdata.action = 'INSERT_PR'
#                     obj_prdata.ref_gid = 'POMAKER'
#                     obj_prdata.reftable = int(data[0])
#                     obj_prdata.status = jsondata.get('params').get('status')
#                     obj_prdata.totype = 'C'
#                     obj_prdata.to = ''
#                     obj_prdata.remark = ''
#                     tran = obj_prdata.set_trans()[0]
#                     for x in podetails:
#                         obj_prdata.action = 'Branch'
#                         obj_prdata.poheader_gid = data[0]
#                         obj_prdata.podetails_gid = data1[0]
#                         obj_prdata.product_gid = x.get('product_gid')
#                         obj_prdata.product_qty = x.get('podetails_qty')
#                         obj_prdata.godown_gid = 1
#                         obj_prdata.entity_gid = request.session['Entity_gid']
#                         obj_prdata.Employee_gid = request.session['Emp_gid']
#                         obj_prdata.delivery_gid = x.get('podetails_qty')
#                         data2 = obj_prdata.set_podelivery()[0].split(',')
#
#             if jsondata.get('params').get('action') == 'draft':
#                 sum = 0;
#                 for i in podetails:
#                     for key, values in i.items():
#                         if key == 'podetails_qty':
#                             sum = sum + values
#                 qty=sum
#                 unit_price= podetails[0].get('podetails_unitprice')
#                 amount=sum*unit_price
#                 tax_amount=(amount*podetails[0].get('podetails_taxamount'))/100
#                 net_amount=tax_amount+amount
#                 obj_prdata.poheader_gid = data[0]
#                 obj_prdata.product_gid = podetails[0].get('product_gid')
#                 obj_prdata.product_qty = sum
#                 obj_prdata.umo_gid = podetails[0].get('podetails_uom')
#                 obj_prdata.per_unitamt = podetails[0].get('podetails_unitprice')
#                 obj_prdata.amount = amount
#                 obj_prdata.taxamt = podetails[0].get('podetails_taxamount')
#                 obj_prdata.netamount =net_amount
#                 obj_prdata.entity_gid = request.session['Entity_gid']
#                 obj_prdata.Employee_gid = request.session['Emp_gid']
#                 data1 = obj_prdata.set_podetails()[0].split(',')
#                 dataout1 = data1[1].split(',')
#
#
#
#
#
#
#                     # if x.get('prpopty') != None:
#                     #     prdtlgid = x.get("prdetail_gid")
#                     #     if prdtlgid == 0 or prdtlgid == None:
#                     #         prdtlgid = x.get("podetails_gid")
#                     #         prptgid = x.get("podetails_qty")
#                     #     if prptgid == 0 or prptgid == None:
#                     #         prptgid = x.get("podetails_qty1")
#                     #     # prptgid = int(z.get("prdetails_qty1"))
#                     #     prdtlgid = x.get("podetail_gid")
#                     #     obj_prdata.action = 'Insert'
#                     #     obj_prdata.poheader_gid = data[0]
#                     #     obj_prdata.podetails_gid = data1[0]
#                     #     obj_prdata.prdetail_gid = prdtlgid
#                     #     obj_prdata.product_qty = prptgid
#                     #     obj_prdata.entity_gid = request.session['Entity_gid']
#                     #     obj_prdata.Employee_gid = request.session['Emp_gid']
#                     #     obj_prdata.prpo_gid = x.get("prpo_gid")
#                     #     data3 = obj_prdata.set_prpoqty()[0].split(',')
#                     #
#                     #
#                     # if  obj_prdata.status =='Approved':
#                     #     obj_prdata.action = 'INSERT_PR'
#                     #     obj_prdata.ref_gid = 'POMAKER'
#                     #     obj_prdata.reftable = int(data[0])
#                     #     obj_prdata.status =jsondata.get('params').get('status')
#                     #     obj_prdata.totype = 'C'
#                     #     obj_prdata.to = ''
#                     #     obj_prdata.remark = ''
#                     #     tran = obj_prdata.set_trans()[0]
#
#         return JsonResponse(json.dumps(data[1]), safe=False)

#PR_to_POheader_Set
def PR_to_POheader_Set(request):
    if request.method == 'POST':
        obj_prdata = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        podetails = jsondata.get('podetails')
        obj_prdata.action = jsondata.get('action')
        obj_prdata.date = datetime.datetime.now().date()
        obj_prdata.supplier_gid = jsondata.get('supplier_gid')
        obj_prdata.teamandcont_gid = jsondata.get('teamandcont_gid')
        obj_prdata.amount = jsondata.get('total_amount')
        obj_prdata.amement_gid = jsondata.get('amement_gid')
        obj_prdata.commodity_gid = jsondata.get('commodity_gid')
        obj_prdata.branchgid = jsondata.get('branch_gid')
        obj_prdata.mepno = jsondata.get('prheader_mepno')
        obj_prdata.vesion_gid = jsondata.get('vesion_gid')
        obj_prdata.from_date = jsondata.get('from_date')
        obj_prdata.to_date = jsondata.get('to_date')
        obj_prdata.Employee_gid = request.session['Emp_gid']
        obj_prdata.status =jsondata.get('status_poheader')
        obj_prdata.entity_gid = request.session['Entity_gid']
        data = obj_prdata.set_poheader()[0].split(',')
        if data[1] == 'SUCCESS':
            for x in podetails:
                obj_prdata.poheader_gid = data[0]
                obj_prdata.product_gid = x.get('product_gid')
                obj_prdata.product_qty = x.get('total_quatity')
                obj_prdata.umo_gid = x.get('podetails_uom')
                obj_prdata.per_unitamt = x.get('supplier_unit_price')
                obj_prdata.amount = x.get('po_amount')
                obj_prdata.taxamt = (x.get('total_quatity') * x.get('supplier_unit_price'))*18/100
                obj_prdata.netamount = x.get('po_amount')+(x.get('total_quatity') * x.get('supplier_unit_price'))*18/100
                obj_prdata.entity_gid = request.session['Entity_gid']
                obj_prdata.Employee_gid = request.session['Emp_gid']
                data1 = obj_prdata.set_podetails()[0].split(',')
                dataout1 = data1[1].split(',')
                if dataout1[0] == 'SUCCESS':
                    for y in x.get('delivery_details'):
                        obj_prdata.poheader_gid = data[0]
                        obj_prdata.podetails_gid = data1[0]
                        obj_prdata.prdetail_gid = y.get('prdetails_gid')
                        for zz in y.get('pr_ccbs'):
                            if zz.get('ccbs_qty') !=0 :
                                obj_prdata.action = 'Insert'
                                obj_prdata.prpoqty_prccbs_gid = zz.get('prccbs_gid')
                                obj_prdata.product_qty = zz.get('ccbs_qty')
                                obj_prdata.entity_gid = request.session['Entity_gid']
                                obj_prdata.Employee_gid = request.session['Emp_gid']
                                obj_prdata.prpo_gid=0
                                data3 = obj_prdata.set_prpoqty()[0].split(',')
                                obj_prdata.action = 'Branch'
                                obj_prdata.poheader_gid = data[0]
                                obj_prdata.podetails_gid = data1[0]
                                obj_prdata.product_gid = y.get('product_gid')
                                obj_prdata.podelivery_prpoqty_gid=data3[0]
                                obj_prdata.podelivery_ccbs=zz.get('prccbs_gid')
                                obj_prdata.product_qty = zz.get('ccbs_qty')
                                obj_prdata.reftable = zz.get('prccbs_reftablegid')
                                obj_prdata.godown_gid = 1
                                obj_prdata.entity_gid = request.session['Entity_gid']
                                obj_prdata.Employee_gid = request.session['Emp_gid']
                                obj_prdata.delivery_gid = y.get('qty')
                                data2 = obj_prdata.set_podelivery()[0].split(',')
                else:
                    return JsonResponse(json.dumps(data[1]), safe=False)
        else:
            return JsonResponse(json.dumps(data[1]), safe=False)

        obj_prdata.action = 'INSERT_PR'
        obj_prdata.ref_gid = 'POMAKER'
        obj_prdata.reftable = int(data[0])
        obj_prdata.status = jsondata.get('status')
        obj_prdata.totype = 'G'
        obj_prdata.to = jsondata.get('tran_to')
        obj_prdata.remark = ''
        tran = obj_prdata.set_trans()[0]
        return JsonResponse(data[1], safe=False)



def POheader_Set(request):
    if request.method == 'POST':
        obj_prdata = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        podetails = jsondata.get('params').get('podetails')
        if podetails == []:
            poheader_gid = '0'
        else:
            poheader_gid = podetails[0].get('poheader_gid')
        if poheader_gid == '':
            obj_prdata.action = jsondata.get('params').get('action')
            obj_prdata.date = datetime.datetime.now().date()
            obj_prdata.supplier_gid = podetails[0].get('supplier_gid')
            obj_prdata.teamandcont_gid = podetails[0].get('teamandcont_gid')
            obj_prdata.amount = jsondata.get('params').get('total_amount')
            obj_prdata.amement_gid = podetails[0].get('amement_gid')
            obj_prdata.vesion_gid = podetails[0].get('vesion_gid')
            obj_prdata.from_date = datetime.datetime.strptime(jsondata.get('params').get('from_date'),
                                                              "%d/%m/%Y").strftime("%Y-%m-%d")
            obj_prdata.to_date = datetime.datetime.strptime(jsondata.get('params').get('to_date'), "%d/%m/%Y").strftime(
                "%Y-%m-%d")
            obj_prdata.Employee_gid = request.session['Emp_gid']
            obj_prdata.status = jsondata.get('params').get('status')
            obj_prdata.entity_gid = request.session['Entity_gid']
            data = obj_prdata.set_poheader()[0].split(',')
            if data != "Error":
                for x in podetails:
                    obj_prdata.poheader_gid = data[0]
                    obj_prdata.product_gid = x.get('product_gid')
                    obj_prdata.product_qty = x.get('podetails_qty')
                    obj_prdata.umo_gid = x.get('podetails_uom')
                    obj_prdata.per_unitamt = x.get('podetails_unitprice')
                    obj_prdata.amount = x.get('podetails_amount')
                    obj_prdata.taxamt = x.get('podetails_taxamount')
                    obj_prdata.netamount = x.get('podetails_totalamount')
                    obj_prdata.entity_gid = request.session['Entity_gid']
                    obj_prdata.Employee_gid = request.session['Emp_gid']
                    data1 = obj_prdata.set_podetails()[0].split(',')
                    dataout1 = data1[1].split(',')
                    prdtlgid = 0
                    prptgid = 0
                    if data1 != "Error":
                        if x.get('godown') != None:
                            for y in x.get('godown'):
                                if y.get('godown_incharge') != "":
                                    obj_prdata.action = 'Insert'
                                    obj_prdata.poheader_gid = data[0]
                                    obj_prdata.podetails_gid = data1[0]
                                    obj_prdata.product_gid = x.get('product_gid')
                                    obj_prdata.product_qty = y.get('godown_qty')
                                    obj_prdata.godown_gid = y.get('godown_gid')
                                    obj_prdata.entity_gid = request.session['Entity_gid']
                                    obj_prdata.Employee_gid = request.session['Emp_gid']
                                    obj_prdata.delivery_gid = 0
                                    data2 = obj_prdata.set_podelivery()[0].split(',')
                        if x.get('prpopty') != None:
                            for z in x.get('prpopty'):

                                prdtlgid = z.get("prdetail_gid")
                                if prdtlgid == 0 or prdtlgid == None:
                                    prdtlgid = z.get("prdetails_gid")
                                    prptgid = z.get("pr_qty")
                                if prptgid == 0 or prptgid == None:
                                    prptgid = z.get("qty")
                                obj_prdata.action = 'Insert'
                                obj_prdata.poheader_gid = data[0]
                                obj_prdata.podetails_gid = data1[0]
                                obj_prdata.prdetail_gid = prdtlgid
                                obj_prdata.product_qty = prptgid
                                obj_prdata.entity_gid = request.session['Entity_gid']
                                obj_prdata.Employee_gid = request.session['Emp_gid']
                                obj_prdata.prpo_gid = z.get("prpo_gid")
                                data3 = obj_prdata.set_prpoqty()[0].split(',')

                # if obj_prdata.status == "Pending for Approval":
                #     if dataout1 == "SUCCESS":
                #         obj_prdata.action = 'Insert'
                #         obj_prdata.ref_gid = 1
                #         obj_prdata.reftable = obj_prdata.prheader_gid
                #         obj_prdata.status = 'Pending for Approval'
                #         obj_prdata.totype = 'I'
                #         obj_prdata.to = 2
                #         obj_prdata.remark = ''
                #         tran = obj_prdata.set_trans()[0].split(',')
                return JsonResponse(json.dumps(dataout1), safe=False)
            else:
                return JsonResponse(json.dumps(data), safe=False)
        else:
            if poheader_gid != '0':
                obj_prdata.action = jsondata.get('params').get('action')
                obj_prdata.poheader_gid = poheader_gid
                obj_prdata.amount = jsondata.get('params').get('total_amount')
                podelete = jsondata.get('params').get('podelete')
                obj_prdata.from_date = datetime.datetime.strptime(jsondata.get('params').get('from_date'),
                                                                  "%d/%m/%Y").strftime("%Y-%m-%d")
                obj_prdata.to_date = datetime.datetime.strptime(jsondata.get('params').get('to_date'),
                                                                "%d/%m/%Y").strftime(
                    "%Y-%m-%d")

                obj_prdata.teamandcont_gid = podetails[0].get('teamandcont_gid')
                obj_prdata.entity_gid = request.session['Entity_gid']
                obj_prdata.create_by = request.session['Emp_gid']
                data = obj_prdata.set_poheaderupdate()[0].split(',')
                if data != "Error":
                    for x in podetails:
                        prdtlgid = 0
                        if x.get('podetail_gid') == "":
                            obj_prdata.poheader_gid = data[0]
                            obj_prdata.product_gid = x.get('product_gid')
                            obj_prdata.product_qty = x.get('podetails_qty')
                            obj_prdata.umo_gid = x.get('podetails_uom')
                            obj_prdata.per_unitamt = x.get('podetails_unitprice')
                            obj_prdata.amount = x.get('podetails_amount')
                            obj_prdata.taxamt = x.get('podetails_taxamount')
                            obj_prdata.netamount = x.get('podetails_totalamount')
                            obj_prdata.entity_gid = request.session['Entity_gid']
                            obj_prdata.Employee_gid = request.session['Emp_gid']
                            data1 = obj_prdata.set_podetails()

                            prptgid = 0
                            if data1 != "Error":
                                for y in x.get('godown'):
                                    if y.get('godown_deivery_gid') == 0:
                                        obj_prdata.action = 'Insert'
                                        obj_prdata.poheader_gid = data[0]
                                        obj_prdata.podetails_gid = data1[0]
                                        obj_prdata.product_gid = x.get('product_gid')
                                        obj_prdata.product_qty = y.get('godown_qty')
                                        obj_prdata.godown_gid = y.get('godown_gid')
                                        obj_prdata.entity_gid = request.session['Entity_gid']
                                        obj_prdata.Employee_gid = request.session['Emp_gid']
                                        obj_prdata.delivery_gid = y.get('godown_deivery_gid')
                                        data2 = obj_prdata.set_podelivery()[0].split(',')
                                    else:
                                        obj_prdata.action = 'Update'
                                        obj_prdata.poheader_gid = data[0]
                                        obj_prdata.podetails_gid = data1[0]
                                        obj_prdata.product_gid = x.get('product_gid')
                                        obj_prdata.product_qty = y.get('godown_qty')
                                        obj_prdata.godown_gid = y.get('godown_Gid')
                                        obj_prdata.entity_gid = request.session['Entity_gid']
                                        obj_prdata.Employee_gid = request.session['Emp_gid']
                                        obj_prdata.delivery_gid = y.get('godown_deivery_gid')
                                        data3 = obj_prdata.set_podelivery()[0].split(',')
                                for z in x.get('prpopty'):
                                    prdtlgid = z.get("prdetail_gid")
                                    if prdtlgid == 0 or prdtlgid == None:
                                        prdtlgid = z.get("prdetails_gid")
                                        prptgid = z.get("pr_qty")
                                    if prptgid == 0 or prptgid == None:
                                        prptgid = z.get("qty")

                                        obj_prdata.action = 'Insert'
                                        obj_prdata.poheader_gid = data[0]
                                        obj_prdata.podetails_gid = data1[0]
                                        obj_prdata.prdetail_gid = z.get('prdetail_gid')
                                        obj_prdata.product_qty = prptgid
                                        obj_prdata.entity_gid = request.session['Entity_gid']
                                        obj_prdata.Employee_gid = request.session['Emp_gid']
                                        obj_prdata.prpo_gid = z.get('prpo_gid')
                                        data4 = obj_prdata.set_prpoqty()[0].split(',')
                                    else:
                                        obj_prdata.action = 'Update'
                                        obj_prdata.poheader_gid = data[0]
                                        obj_prdata.podetails_gid = data1[0]
                                        obj_prdata.prdetail_gid = z.get('prdetail_gid')
                                        obj_prdata.product_qty = z.get('pr_qty')
                                        obj_prdata.entity_gid = request.session['Entity_gid']
                                        obj_prdata.Employee_gid = request.session['Emp_gid']
                                        obj_prdata.prpo_gid = z.get('prpo_gid')
                                        data5 = obj_prdata.set_prpoqty()[0].split(',')
                        else:
                            prdtlgid = 0
                            prdtlgid = x.get('podetails_gid')
                            if prdtlgid == 0 or prdtlgid == None:
                                prdtlgid = x.get("podetail_gid")
                            obj_prdata.podetails_gid = prdtlgid
                            obj_prdata.product_gid = x.get('product_gid')
                            obj_prdata.product_qty = x.get('podetails_qty')
                            obj_prdata.per_unitamt = x.get('podetails_unitprice')
                            obj_prdata.amount = x.get('podetails_amount')
                            obj_prdata.taxamt = x.get('podetails_taxamount')
                            obj_prdata.netamount = x.get('podetails_totalamount')
                            obj_prdata.Employee_gid = request.session['Emp_gid']
                            data1 = outputSplit(obj_prdata.set_podetailupdate(), 1)

                            prptgid = 0
                            if data1 != "Error":
                                if x.get('godown') != None:
                                    for y in x.get('godown'):
                                        if y.get('godown_deivery_gid') == 0:
                                            obj_prdata.action = 'Insert'
                                            obj_prdata.poheader_gid = obj_prdata.poheader_gid
                                            obj_prdata.podetails_gid = prdtlgid
                                            obj_prdata.product_gid = x.get('product_gid')
                                            obj_prdata.product_qty = y.get('godown_qty')
                                            obj_prdata.godown_gid = y.get('godown_gid')
                                            obj_prdata.entity_gid = request.session['Entity_gid']
                                            obj_prdata.Employee_gid = request.session['Emp_gid']
                                            obj_prdata.delivery_gid = y.get('godown_deivery_gid')
                                            data2 = obj_prdata.set_podelivery()[0].split(',')
                                        else:
                                            obj_prdata.action = 'Update'
                                            obj_prdata.poheader_gid = obj_prdata.poheader_gid
                                            obj_prdata.podetails_gid = obj_prdata.podetails_gid
                                            obj_prdata.product_gid = x.get('product_gid')
                                            obj_prdata.product_qty = y.get('godown_qty')
                                            obj_prdata.godown_gid = y.get('godown_gid')
                                            obj_prdata.entity_gid = request.session['Entity_gid']
                                            obj_prdata.Employee_gid = request.session['Emp_gid']
                                            obj_prdata.delivery_gid = y.get('godown_deivery_gid')
                                            data3 = obj_prdata.set_podelivery()[0].split(',')

                                if x.get('prpopty') != None:
                                    for z in x.get('prpopty'):
                                        if prdtlgid == 0 or prdtlgid == None:
                                            prdtlgid = z.get("prdetails_gid")
                                            prptgid = z.get("pr_qty")
                                        if prptgid == 0 or prptgid == None:
                                            prptgid = z.get("qty")

                                            obj_prdata.action = 'Insert'
                                            obj_prdata.poheader_gid = obj_prdata.poheader_gid
                                            obj_prdata.podetails_gid = obj_prdata.podetails_gid
                                            obj_prdata.prdetail_gid = z.get('prdetail_gid')
                                            obj_prdata.product_qty = prptgid
                                            obj_prdata.entity_gid = request.session['Entity_gid']
                                            obj_prdata.Employee_gid = request.session['Emp_gid']
                                            obj_prdata.prpo_gid = z.get('prpo_gid')
                                            data4 = obj_prdata.set_prpoqty()[0].split(',')
                                        else:
                                            obj_prdata.action = 'Update'
                                            obj_prdata.poheader_gid = obj_prdata.poheader_gid
                                            obj_prdata.podetails_gid = obj_prdata.podetails_gid
                                            obj_prdata.prdetail_gid = z.get('prdetail_gid')
                                            obj_prdata.product_qty = z.get('pr_qty')
                                            obj_prdata.entity_gid = request.session['Entity_gid']
                                            obj_prdata.Employee_gid = request.session['Emp_gid']
                                            obj_prdata.prpo_gid = z.get('prpo_gid')
                                            data5 = obj_prdata.set_prpoqty()[0].split(',')
                    if data1 == "SUCCESS":
                        for podel in podelete:
                            obj_prdata.podetails_gid = podel
                            obj_prdata.Employee_gid = request.session['Emp_gid']
                            obj_prdata.entity_gid = request.session['Entity_gid']
                            datapodel = obj_prdata.set_podetele()[0].split(',')

                        podeliverydelete = jsondata.get('params').get('podeliverydelete')

                        if podeliverydelete != None:
                            for podeliverydel in podeliverydelete:
                                obj_prdata.action = 'Delete'
                                obj_prdata.poheader_gid = 0
                                obj_prdata.podetails_gid = 0
                                obj_prdata.product_gid = 0
                                obj_prdata.product_qty = 0
                                obj_prdata.godown_gid = 0
                                obj_prdata.entity_gid = request.session['Entity_gid']
                                obj_prdata.Employee_gid = request.session['Emp_gid']
                                obj_prdata.delivery_gid = podeliverydel
                                data3 = obj_prdata.set_podelivery()[0].split(',')

                    if obj_prdata.status == "Pending for Approval":
                        if data1 == "SUCCESS":
                            obj_prdata.action = 'Insert'
                            obj_prdata.ref_gid = 1
                            obj_prdata.reftable = obj_prdata.prheader_gid
                            obj_prdata.status = 'Pending for Approval'
                            obj_prdata.totype = 'I'
                            obj_prdata.to = 2
                            obj_prdata.remark = ''
                            tran = obj_prdata.set_trans()[0].split(',')

                    return JsonResponse(data1, safe=False)
                else:
                    return JsonResponse(data, safe=False)
            else:
                podelete = jsondata.get('params').get('podelete')
                for podel in podelete:
                    obj_prdata.podetails_gid = podel
                    obj_prdata.Employee_gid = request.session['Emp_gid']
                    obj_prdata.entity_gid = request.session['Entity_gid']
                    datapodel = obj_prdata.set_podetele()[0].split(',')

                podeliverydelete = jsondata.get('params').get('podeliverydelete')

                if podeliverydelete != None:
                    for podeliverydel in podeliverydelete:
                        obj_prdata.action = 'Delete'
                        obj_prdata.poheader_gid = 0
                        obj_prdata.podetails_gid = 0
                        obj_prdata.product_gid = 0
                        obj_prdata.product_qty = 0
                        obj_prdata.godown_gid = 0
                        obj_prdata.entity_gid = request.session['Entity_gid']
                        obj_prdata.Employee_gid = request.session['Emp_gid']
                        obj_prdata.delivery_gid = podeliverydel
                        data3 = obj_prdata.set_podelivery()[0].split(',')


                return JsonResponse(datapodel, safe=False)


def outputSplit(tubledtl, index):
    temp = tubledtl[0].split(',')
    if (len(temp) > 1):
        if (index == 0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return temp[0]


def Getprstatus(request):
    if request.method == 'GET':
        obj_status_get = mPurchase.Purchase_model()
        data = obj_status_get.get_prstatus()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def getpoadmentment(request):
    if request.method == 'GET':
        obj_adment = mPurchase.Purchase_model()
        data = obj_adment.get_poadment()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def getpoadmentmentapp(request):
    if request.method == 'GET':
        obj_adment = mPurchase.Purchase_model()
        data = obj_adment.get_poadmentapproval()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def get_grnheadersumry(request):
    if request.method == 'GET':
        obj_grnheader = mPurchase.Purchase_model()
        obj_grnheader.serail_no = ""
        obj_grnheader.grnheader_gid = ""
        obj_grnheader.supplier_name = ""
        data = obj_grnheader.get_grnheader()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def get_grndetails(request):
    if request.method == 'POST':
        obj_grnheader = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_grnheader.grnheader_gid = jsondata.get('params').get('grnheader_gid')
        obj_grnheader.supplier_gid = jsondata.get('params').get('grnheader_supplier_gid')
        data = obj_grnheader.get_grndetails()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def set_grnheader(request):
    if request.method == 'POST':
        obj_grnheader = mPurchase.Purchase_model()
        obj_grnheader.grnheader_gid = ""
        obj_grnheader.supplier_gid = ""
        data = obj_grnheader.get_grndetails()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def set_grndetails(request):
    if request.method == 'POST':
        obj_grnheader = mPurchase.Purchase_model()
        obj_grnheader.grnheader_gid = ""
        obj_grnheader.supplier_gid = ""
        data = obj_grnheader.set_grndetails()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def set_grnapproval(request):
    if request.method == 'POST':
        obj_maker = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_maker.action = jsondata.get('params').get('action')
        obj_maker.grnheader_gid = jsondata.get('params').get('grnheader_gid')

        obj_maker.remark = ' ' if jsondata.get('params').get('remarks') == None else jsondata.get('params').get(
            'remarks')

        obj_maker.Employee_gid = request.session['Emp_gid']
        obj_maker.entity_gid = request.session['Entity_gid']
        data = obj_maker.set_grnapproval()
        return JsonResponse(json.dumps(data), safe=False)


def get_grnapprovalget(request):
    if request.method == 'GET':
        obj_grnheader = mPurchase.Purchase_model()
        obj_grnheader.grnheader_gid = 0
        obj_grnheader.supplier_gid = 0
        data = obj_grnheader.get_grnapprovalset()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def get_querystring(request):
    if request.method == 'GET':
        obj_grnheader = mPurchase.Purchase_model()
        obj_grnheader.poheader_gid = 0
        obj_grnheader.podetail_gid = 0
        obj_grnheader.entity_gid = request.session['Entity_gid']
        data = obj_grnheader.get_querystring()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def get_grnpoheaderdetails(request):
    if request.method == "POST":
        obj_grnpo = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_grnpo.grnheader_gid = jsondata.get('params').get('grnheader_gid')
        obj_grnpo.supplier_gid = jsondata.get('params').get('supplier_gid')
        data = obj_grnpo.get_pogrndetails()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)
 #commodity
def commodity(request):
    return render(request, "pur_commodity.html")
#Commodity Add
def commodityadd(request):
    return render(request, "pur_AddCommodity.html")

#commo_product_name
def commo_product_name(request):
    if request.method == 'POST':
        obj_dropdown = mPurchase.Purchase_model()
        obj_dropdown.action = 'Product'
        obj_dropdown.json_data='{"Table_name":"gal_mst_tproduct","Column_1":"product_gid,product_name","Column_2":"","Where_Common":"product","Where_Primary":"","Primary_Value":"","Order_by":"name"}'
        obj_dropdown.entity_gid = request.session['Entity_gid']
        df_dropexec = obj_dropdown.get_alltablevalue()
        jdata = df_dropexec.to_json(orient='records')
        return JsonResponse(jdata, safe=False)



#commo_product
def commo_product(request):
    if request.method == 'POST':
        obj_producategory_ddl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_producategory_ddl.value = jsondata.get('Action')
        obj_producategory_ddl.value1 = json.dumps(jsondata.get('data').get('Params').get('FILTER'))
        obj_producategory_ddl.value2 = json.dumps(jsondata.get('data').get('Params').get('CLASSIFICATION'))
        df_customer_ddl = obj_producategory_ddl.commo_productmap()
        return JsonResponse(json.dumps(df_customer_ddl), safe=False)


 #commodity
def commoditydropdown(request):
    if request.method == 'POST':
        objdata = mPurchase.Purchase_model()
        objdata.entity_gid = request.session['Entity_gid']
        objdata.data = '{"Table_name": "ap_mst_tcommodity","Column_1": "commodity_gid,commodity_code,commodity_name,commodity_status","Column_2": "","Where_Common": "commodity","Where_Primary": "","Primary_Value": "","Order_by": "gid"}'
        obj_cancel_data = objdata.getdelmattype()
        jdata = obj_cancel_data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)

# supplier dropdown
def supplier_dropdown(request):
    if request.method == 'POST':
        obj_producategory_ddl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_producategory_ddl.action = jsondata.get('Action')
        obj_producategory_ddl.json_data = json.dumps(jsondata.get('data').get('Params').get('FILTER'))
        obj_producategory_ddl.entity_gid =request.session['Entity_gid']
        df_customer_ddl = obj_producategory_ddl.supplier_drop()
        jdata = df_customer_ddl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

# prbased ccbs
def prdetails_ccbs(request):
    if request.method == 'POST':
        obj_producategory_ddl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_producategory_ddl.Type = jsondata.get('Type')
        obj_producategory_ddl.Sub_type = jsondata.get('Sub_type')
        obj_producategory_ddl.json_data = json.dumps(jsondata.get('data').get('Params').get('FILTER'))
        obj_producategory_ddl.json_classification = json.dumps(jsondata.get('data').get('Params').get('CLASSIFICATION'))
        obj_producategory_ddl.create_by =request.session['Emp_gid']
        df_customer_ddl = obj_producategory_ddl.prccbs_details()
        jdata = df_customer_ddl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


#dimdim
def commosave(request):
    if request.method == 'POST':
        obj_producategory_ddl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_producategory_ddl.value = jsondata.get('Action')
        obj_producategory_ddl.value1 = json.dumps(jsondata.get('data').get('Params').get('FILTER'))
        obj_producategory_ddl.value2 = json.dumps(jsondata.get('data').get('Params').get('CLASSIFICATION'))
        df_customer_ddl = obj_producategory_ddl.dimdimmod()
        return JsonResponse(json.dumps(df_customer_ddl), safe=False)

#PR
def pr_productcategory(request):
    if request.method == 'GET':
        obj_producategory_ddl = mPurchase.Purchase_model()
        obj_producategory_ddl.productcat_gid = 1
        df_customer_ddl = obj_producategory_ddl.get_pr_productcategory()
        jdata = df_customer_ddl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)
#PR type
def pr_category_type(request):
    if request.method == 'POST':
        obj_producategory_ddl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_producategory_ddl.prodcat_gid = str(jsondata)
        df_customer_ddl = obj_producategory_ddl.get_pr_product_types()
        jdata = df_customer_ddl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

#PR product
def pr_product(request):
    if request.method == 'POST':
        obj_producategory_ddl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_producategory_ddl.producttype_gid = str(jsondata)
        df_customer_ddl = obj_producategory_ddl.get_pr_productname()
        jdata = df_customer_ddl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

#PR Commodity data get
def commodity_pdata(request):
    if request.method == 'POST':
        obj_producategory_ddl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_producategory_ddl.action = jsondata.get('Action')
        obj_producategory_ddl.pgid = json.dumps(jsondata.get('data'))
        obj_producategory_ddl.engid = json.dumps(jsondata.get('endata'))

        df_customer_ddl = obj_producategory_ddl.Commodity_product_data()
        jdata = df_customer_ddl.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

#commodity_generate_code
def commodity_code_gen(request):
    if request.method == 'POST':
        obj_producategory_ddl = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_producategory_ddl.type = jsondata.get('Type')
        obj_producategory_ddl.sub_type = jsondata.get('Sub_Type')
        obj_producategory_ddl.filter_json = json.dumps(jsondata.get('data').get('Params').get('FILTER'))
        obj_producategory_ddl.classification_json = json.dumps(jsondata.get('data').get('Params').get('CLASSIFICATION'))
        df_customer_ddl = obj_producategory_ddl.codegen_commodity()
        return JsonResponse(df_customer_ddl, safe=False)


def get_grnheader(request):
    if request.method == 'POST':
        obj_prdata = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        grndetails = jsondata.get('params').get('grndetlist')
        grnheader = jsondata.get('params').get('objgrnheader')
        grnheader_gid = grnheader.get('grnheader_gid')
        if grnheader_gid == None:
            obj_prdata.action = grnheader.get('type')
            obj_prdata.date = datetime.datetime.strptime(grnheader.get('grnheader_received'), "%d/%m/%Y").strftime(
                "%Y-%m-%d")
            obj_prdata.dcno = grnheader.get('grnheader_dcno')
            obj_prdata.invoice_no = grnheader.get('grnheader_invno')
            obj_prdata.remark = grnheader.get('grnheader_remarks')
            obj_prdata.Employee_gid = request.session['Emp_gid']
            obj_prdata.entity_gid = request.session['Entity_gid']
            data = obj_prdata.set_grnheader()[0].split(',')
            if data != "Error":
                for x in grndetails:
                    if x.get('is_check') == True:
                        obj_prdata.action = 'insert'
                        obj_prdata.grnheader_gid = data[0]
                        obj_prdata.poheader_gid = x.get('poheader_gid')
                        obj_prdata.podetails_gid = x.get('podetails_gid')
                        obj_prdata.product_qty = x.get('current_qty')
                        obj_prdata.godown_gid = x.get('podelivery_godown_gid')
                        obj_prdata.Employee_gid = request.session['Emp_gid']
                        obj_prdata.entity_gid = request.session['Entity_gid']
                        data1 = obj_prdata.set_grndetails()[0].split(',')
                        dataout1 = data1[1]
                return JsonResponse(json.dumps(dataout1), safe=False)
            else:
                return JsonResponse(json.dumps(data), safe=False)
        else:
            obj_prdata.action = grnheader.get('type')
            obj_prdata.date = datetime.datetime.strptime(grnheader.get('grnheader_received'), "%d/%m/%Y").strftime(
                "%Y-%m-%d")
            obj_prdata.dcno = grnheader.get('grnheader_dcno')
            obj_prdata.grnheader_gid = grnheader_gid
            obj_prdata.invoice_no = grnheader.get('grnheader_invno')
            obj_prdata.remark = grnheader.get('grnheader_remarks')
            obj_prdata.Employee_gid = request.session['Emp_gid']
            obj_prdata.entity_gid = request.session['Entity_gid']
            data = obj_prdata.set_grnheaderupdate()[0].split(',')
            # data = obj_prdata.set_grnheaderupdate()[0].split(',')
            if data != "Error":
                for x in grndetails:
                    if x.get('is_check') == True:
                        if x.get('grninwarddetails_gid') == None:
                            obj_prdata.action = 'insert'
                            obj_prdata.grnheader_gid = grnheader_gid
                            obj_prdata.poheader_gid = x.get('poheader_gid')
                            obj_prdata.podetails_gid = x.get('podetails_gid')
                            obj_prdata.product_qty = x.get('current_qty')
                            obj_prdata.godown_gid = x.get('podelivery_godown_gid')
                            obj_prdata.Employee_gid = request.session['Emp_gid']
                            obj_prdata.entity_gid = request.session['Entity_gid']
                            data1 = obj_prdata.set_grndetails()[0].split(',')
                            dataout1 = data1[1]
                        else:
                            obj_prdata.action = 'update'
                            obj_prdata.grnheader_gid = data[0]
                            obj_prdata.grndetail_gid = x.get('grninwarddetails_gid')
                            obj_prdata.poheader_gid = x.get('poheader_gid')
                            obj_prdata.podetails_gid = x.get('podetails_gid')
                            obj_prdata.product_qty = x.get('current_qty')
                            obj_prdata.godown_gid = x.get('podelivery_godown_gid')
                            obj_prdata.Employee_gid = request.session['Emp_gid']
                            obj_prdata.entity_gid = request.session['Entity_gid']
                            data1 = obj_prdata.set_grndetails()[0].split(',')
                            dataout1 = data1[1]
                return JsonResponse(json.dumps(dataout1), safe=False)
            else:
                return JsonResponse(json.dumps(data), safe=False)


def PurchasePlanningIndex(request):
    return render(request, "PurchasePlanning.html")


def pr_supplierIndex(request):
    return render(request, "pr_supplier_allocation.html")


def purchasedata(request):
    if request.method == 'GET':
        fdate = common.convertDateTime(request.GET['fromdate'])
        data_perc = 1
        supplier_capcity = 5000
        capacity = {'sup_count': 1, 'sup_capacity': supplier_capcity}
        obj_salesplanning = mPurchase.Purchase_model()

        f_date = fdate
        t_date = f_date + relativedelta(months=+5)

        obj_salesplanning.prod_type_gid = 1
        df_product = obj_salesplanning.get_producttype()

        obj_salesplanning.from_year = f_date.year
        obj_salesplanning.to_year = t_date.year
        obj_salesplanning.from_month = f_date.month
        obj_salesplanning.to_month = t_date.month

        df_salesplan = obj_salesplanning.get_salesplanningl()
        df_podetails = obj_salesplanning.get_purchplanningl()
        productdtl = []
        obj_stock = mStock.StockModel()
        obj_stock.type = 'MonthWise_Stock'
        obj_stock.sub_type = ''
        obj_stock.from_date = ''
        obj_stock.to_date = ''
        obj_stock.product_gid = 1
        obj_stock.supplier_gid = 1
        obj_stock.entity_gid = request.session['Entity_gid']
        obj_stock.jsonData = json.dumps({"date": str(f_date + relativedelta(months=-1))})
        openstock = obj_stock.get_stock()
        df_stock = openstock['DATA']
        for x, item in df_product.iterrows():
            productgid = item['product_gid']
            productname = item['product_displayname']
            suppplieruntiprice = item['supplierproduct_unitprice']

            pdtl = {'product_gid': productgid, 'product_name': productname, 'unit_price': suppplieruntiprice,
                    }
            months = []
            temp_date = f_date
            for y in range(0, 4):
                months.append(temp_date.strftime('%m-%Y'))
                pdtl['targetperc' + str(y + 1)] = data_perc

                # closing stock
                nxt_mnt = temp_date + relativedelta(months=+1)
                pdtl['nxtSalePlanQty' + str(y + 1)] = int(
                    df_salesplan[(df_salesplan['salesplandetails_year'] == nxt_mnt.year) & (
                            df_salesplan['product_gid'] == productgid) & (df_salesplan[
                                                                              'salesplandetails_month'] == nxt_mnt.month)][
                        'salqty'].sum())

                # opening stock
                if (y == 0):
                    #pdtl['openStk' + str(y + 1)] = 200
                    for x, item in df_stock.iterrows():
                        productgid1 = item['product_gid']
                        if productgid == productgid1:
                            pdtl['openStk' + str(y + 1)] = item['stockbalance_cb']
                            break

                # sales as on month (Sales planning)
                pdtl['salePlanQty' + str(y + 1)] = int(
                    df_salesplan[(df_salesplan['salesplandetails_year'] == temp_date.year) & (
                            df_salesplan['product_gid'] == productgid) & (
                                         df_salesplan[
                                             'salesplandetails_month'] == temp_date.month)][
                        'salqty'].sum())
                pdtl['ActualSales' + str(y + 1)] = (df_salesplan[(df_salesplan['product_gid'] == productgid)]['actual_qty'].sum())
                # yearmnth['purPlanQty'] = float(df_podetails[(df_podetails['po_year'] == temp_date.year) & (
                #         df_podetails['product_gid'] == productgid) & (df_podetails['po_month'] == temp_date.month)][
                #                                    'po_quantity'].sum())

                # pending po
                pdtl['pendingPO' + str(y + 1)] = float(df_podetails[(df_podetails['po_year'] == temp_date.year) & (
                        df_podetails['product_gid'] == productgid) & (df_podetails['po_month'] == temp_date.month)][
                                                           'pending_qty'].sum())
                temp_date = temp_date + relativedelta(months=+1)
            productdtl.append(pdtl)
        data = {'productdtl': productdtl, 'months': months, 'capacity': capacity}
        return JsonResponse(data, safe=False)


def get_supCapacity(request):
    if request.method == 'GET':
        prsuplierdetails = mPurchase.Purchase_model()
        prsuplierdetails.action = request.GET['action']
        prsuplierdetails.supplier_gid = request.GET['supplier_gid']
        prsuplierdetails.product_gid = request.GET['product_gid']
        prsuplierdetails.product_name = request.GET['product_name']
        prsuplierdetails.serail_no = request.GET['serial_no']
        df_pro = prsuplierdetails.get_poqty()
        # df_pro = json.loads(jdata.to_json(orient='records'))

        prsuplierdetails.action = 'suppliercapacity'
        prsuplierdetails.type = ''
        prsuplierdetails.vendor = '{}'
        sup_details = prsuplierdetails.get_supplier()
        df_supplier = (sup_details[['supplier_gid', 'supplier_name', 'creditlimit_days', 'sup_capacity']]).groupby(
            ['supplier_gid', 'supplier_name', 'creditlimit_days', 'sup_capacity']).size().reset_index();
        df_sup_pro = (sup_details[['product_gid']]).groupby(
            ['product_gid']).size().reset_index(name='counts');
        result = pd.merge(df_pro, df_sup_pro, how='left', on='product_gid').sort_values(by=['counts']).reset_index(
            drop=True)
        supplierlist = json.loads(df_supplier.to_json(orient='records'))
        sup_cap = {}
        for i, item in df_supplier.iterrows():
            sup_cap[item['supplier_gid']] = item['sup_capacity']

        productList = []

        for x, pro in result.iterrows():
            product = {'product_gid': pro['product_gid'], 'product_name': pro['product_name'],
                       'pr_qty': pro['prdetails_qty']}
            supplier = sup_details[sup_details['product_gid'] == pro['product_gid']].sort_values(by=
                                                                                                 ['unitprice',
                                                                                                  'creditlimit_days'],
                                                                                                 ascending=[1,
                                                                                                            0]).reset_index(
                drop=True)
            prqty = pro['prdetails_qty']
            ttl_sup = supplier['supplier_gid'].count()
            remain = prqty
            total = 0
            pro_fill = False
            for y, sup in supplier.iterrows():
                if not pro_fill:
                    capacity = sup_cap[sup['supplier_gid']]
                    remain = capacity - abs(remain)
                    if remain >= 0:
                        product[sup['supplier_gid']] = capacity - remain
                        sup_cap[sup['supplier_gid']] = remain
                        total = total + capacity - remain
                        pro_fill = True;
                    else:
                        product[sup['supplier_gid']] = capacity
                        sup_cap[sup['supplier_gid']] = 0
                        total = total + capacity
                else:
                    product[sup['supplier_gid']] = 0
                if y + 1 == ttl_sup:
                    product['total'] = total
            productList.append(product)
        data = {'product': productList, 'supplier': supplierlist}
        return JsonResponse(data, safe=False)


def get_allqueue_status(request):
    if request.method == "POST":
        obj_allqueuestatus = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_allqueuestatus.tablename = jsondata.get('params').get('table_name')
        obj_allqueuestatus.ref_gid = jsondata.get('params').get('gid')
        obj_allqueuestatus.status = jsondata.get('params').get('status')
        obj_allqueuestatus.entity_gid = request.session['Entity_gid']
        out_message = outputReturn(obj_allqueuestatus.get_questatus(), 0)
        return JsonResponse(out_message, safe=False)


def outputReturn(tubledtl, index):
    temp = tubledtl[0].split(',')
    if (len(temp) > 1):
        if (index == 0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return temp[0]


def set_PRDetails(request):
    if request.method == "POST":
        jsondata = json.loads(request.body.decode('utf-8'))
        action = jsondata.get('action')
        status = jsondata.get('status')
		#type = jsondata.get('type')
        #header = jsondata.get('prheader')
        prdetails = jsondata.get('prdetails')
        #classification = jsondata.get('classificaton')
        pr_amt=jsondata.get('pr_amt')
        prdelete = jsondata.get('prdelete')
        params = {'Action': "" + action + "", 'Employee_Gid': request.session['Emp_gid'] ,
                  'entity_gid':  request.session['Entity_gid'] }
        datas = {"params": {"status": status, "prdetails": prdetails, "prdelete": prdelete,"pr_amt": pr_amt}}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/PurchaseRequest_Set", params=params, data=json.dumps(datas), headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def get_SalesCount(request):
    if request.method == "POST":
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_sales = mPurchase.Purchase_model()
        obj_sales.type = jsondata.get('type')
        obj_sales.sub_type = jsondata.get('sub_type')
        obj_sales.fliter = jsondata.get('fliter')
        obj_sales.classification = jsondata.get('classification')
        obj_sales.create_by = jsondata.get('create_by')
        data = obj_sales.get_salescount()
        ldict = data.to_json(orient='records')
        return JsonResponse(json.loads(ldict), safe=False)


def set_grn(request):
    if request.method == 'POST':
        obj_ = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_.type =  jsondata.get('params').get('type')
        obj_.action = ''
        obj_.jsonData = json.dumps(jsondata.get('params').get('FILTER'))
        #obj_.json_classification = jsondata.get('params').get('CLASSIFICATION')
        obj_.json_classification = '{"Entity_Gid":[1]}'
        #obj_.json_classification["Entity_Gid"][0] = request.session['Entity_gid']
        obj_.employee_gid = request.session['Emp_gid']
        ld_out_message = obj_.set_grn_data()
        out_message = outputReturn(ld_out_message, 0)
        return JsonResponse(out_message, safe=False)

def get_grnprocess_details(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if ((jsondata.get('params').get('type') == 'GRN') ):
            type = jsondata.get('params').get('type')
            sub_type = jsondata.get('params').get('subtype')
            filter_json = json.dumps(jsondata.get('params').get('filter'))
            entity_gid = request.session['Entity_gid']
            params = {'type': type,'sub_type':sub_type, 'entity_gid': entity_gid}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Get_Grn_Details", params=params, headers=headers, data=filter_json,verify=False)
            results = result.content.decode("utf-8")
            return JsonResponse(json.loads(results), safe=False)

def grndetailsview(request):
    return render(request, "pur_GrnDetailsView.html")

def get_grnprocessdetails(request):
    if request.method == "POST":
        obj_grnpo = mPurchase.Purchase_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_grnpo.filter_json = jsondata.get('params').get('filter')
        obj_grnpo.type = jsondata.get('params').get('type')
        obj_grnpo.sub_type = jsondata.get('params').get('subtype')
        data = obj_grnpo.grndetails_get()
        jdata = data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def get_Saleshstry(request):
    if request.method == 'GET':
        cur_date = datetime.datetime.now()
        #jsondata = json.loads(request.body.decode('utf-8'))
        cust_gid = request.GET['cust_gid']
        product_gid = request.GET['product_gid']
        searchtype = request.GET['searchtype']
        cur_year = int(cur_date.strftime("%Y"))
        toyear = cur_year
        fromyear = cur_year - 3
        entity_gid = request.session['Entity_gid']
        emp_gid =  request.session['Emp_gid']
        params = {'cust_gid': cust_gid, 'fromyear': fromyear, 'entity_gid': entity_gid,'toyear':toyear,'product_gid':product_gid,'searchtype':searchtype,'Emp_Gid':emp_gid }
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        result = requests.get("" + ip + "/Salesplan_Report", params=params, headers=headers,
                                   verify=False)
        data = result.content.decode("utf-8")
        data=json.loads(data)
        data=data.get('DATA')
        df_saleshstry = pd.DataFrame(data)
        df_saleshstry["year_month"] = df_saleshstry["order_year"].apply(str) + "-" + df_saleshstry["order_month"].apply(str)
        year_month0 = datetime.datetime.today() + relativedelta(years=0,months=0)
        year0 = year_month0.strftime("%Y")
        month0 = year_month0.strftime("%B")
        year_month0 = year_month0.strftime("%Y-%m")
        year_month1 = datetime.datetime.today() + relativedelta(years=0, months=1)
        year1 = year_month1.strftime("%Y")
        month1 = year_month1.strftime("%B")
        year_month1 = year_month1.strftime("%Y-%m")
        year_month2 = datetime.datetime.today() + relativedelta(years=0, months=2)
        year2 = year_month2.strftime("%Y")
        month2 = year_month2.strftime("%B")
        year_month2 = year_month2.strftime("%Y-%m")
        year_month3 = datetime.datetime.today() + relativedelta(years=0, months=3)
        year3 = year_month3.strftime("%Y")
        month3 = year_month3.strftime("%B")
        year_month3 = year_month3.strftime("%Y-%m")
        year_month4 = datetime.datetime.today() + relativedelta(years=-1, months=0)
        year4 = year_month4.strftime("%Y")
        year_month4 = year_month4.strftime("%Y-%m")
        year_month5 = datetime.datetime.today() + relativedelta(years=-1, months=1)
        year5 = year_month5.strftime("%Y")
        year_month5 = year_month5.strftime("%Y-%m")
        year_month6 = datetime.datetime.today() + relativedelta(years=-1, months=2)
        year6 = year_month6.strftime("%Y")
        year_month6 = year_month6.strftime("%Y-%m")
        year_month7 = datetime.datetime.today() + relativedelta(years=-1, months=3)
        year7 = year_month7.strftime("%Y")
        year_month7 = year_month7.strftime("%Y-%m")
        year_month8 = datetime.datetime.today() + relativedelta(years=-2, months=0)
        year8 = year_month8.strftime("%Y")
        year_month8 = year_month8.strftime("%Y-%m")
        year_month9 = datetime.datetime.today() + relativedelta(years=-2, months=1)
        year9 = year_month9.strftime("%Y")
        year_month9 = year_month9.strftime("%Y-%m")
        year_month10 = datetime.datetime.today() + relativedelta(years=-2, months=2)
        year10 = year_month10.strftime("%Y")
        year_month10 = year_month10.strftime("%Y-%m")
        year_month11 = datetime.datetime.today() + relativedelta(years=-2, months=3)
        year11 = year_month11.strftime("%Y")
        year_month11 = year_month11.strftime("%Y-%m")
        year_month12 = datetime.datetime.today() + relativedelta(years=-3, months=0)
        year12 = year_month12.strftime("%Y")
        year_month12 = year_month12.strftime("%Y-%m")
        year_month13 = datetime.datetime.today() + relativedelta(years=-3, months=1)
        year13 = year_month13.strftime("%Y")
        year_month13 = year_month13.strftime("%Y-%m")
        year_month14 = datetime.datetime.today() + relativedelta(years=-3, months=2)
        year14 = year_month14.strftime("%Y")
        year_month14 = year_month14.strftime("%Y-%m")
        year_month15 = datetime.datetime.today() + relativedelta(years=-3, months=3)
        year15 = year_month15.strftime("%Y")
        year_month15 = year_month15.strftime("%Y-%m")
        sales_data = []
        data2=0;data3=0;data4=0;data5=0;data6=0
        data7 = 0;data8=0;data9=0;data10=0;data11=0
        data12 = 0;data13=0;data14=0;data1=0
        b = df_saleshstry.isin([year_month0]).any().any()
        if b != False:
            ym1 = int(df_saleshstry[(df_saleshstry['year_month'] == year_month0)]['order_qty'].sum())
            data1 =  {str(year0):{"qty": int(ym1)},"month":month0}
            sales_data.append(data1)
        else:
            data1 = {str(year0): {"qty": "0"},"month":month0}
            sales_data.append(data1)

        b1 = df_saleshstry.isin([year_month1]).any().any()
        if b1 != False:
            ym2 = int(df_saleshstry[(df_saleshstry['year_month'] == year_month1)]['order_qty'].sum())
            data2 = {str(year1) : {"qty": int(ym2)},"month":month1}
            sales_data.append(data2)
        else:
            data2 =  {str(year1): {"qty": "0"},"month":month1}
            sales_data.append(data2)

        b2 = df_saleshstry.isin([year_month2]).any().any()
        if b2 != False:
            ym3 = int(df_saleshstry[(df_saleshstry['year_month'] == year_month2)]['order_qty'].sum())
            data3 =  {str(year2):{"qty": int(ym3)},"month":month2}
            sales_data.append(data3)
        else:
            data3 = {str(year2): {"qty": "0"},"month":month2}
            sales_data.append(data3)

        b3 = df_saleshstry.isin([year_month3]).any().any()
        if b3 != False:
            ym4 = int(df_saleshstry[(df_saleshstry['year_month'] == year_month3)]['order_qty'].sum())
            data4 = {str(year3): {"qty": int(ym4)},"month":month3}
            sales_data.append(data4)
        else:
            data4 = {str(year3): {"qty": "0"},"month":month3}
            sales_data.append(data4)

        b4 = df_saleshstry.isin([year_month4]).any().any()
        if b4 != False:
            ym5 = int(df_saleshstry[(df_saleshstry['year_month'] == year_month4)]['order_qty'].sum())
            data5 = {str(year4): {"qty": int(ym5)}}
            data1.update(data5)
        else:
            data5 = {str(year4): {"qty": "0"}}
            data1.update(data5)

        b5 = df_saleshstry.isin([year_month5]).any().any()
        if b5 != False:
            ym6 = int(df_saleshstry[(df_saleshstry['year_month'] == year_month5)]['order_qty'].sum())
            data6 = {str(year5): {"qty": int(ym6)}}
            data2.update(data6)
        else:
            data6 = {str(year5): {"qty": "0"}}
            data2.update(data6)

        b6 = df_saleshstry.isin([year_month6]).any().any()
        if b6 != False:
            ym7 = int(df_saleshstry[(df_saleshstry['year_month'] == year_month6)]['order_qty'].sum())
            data7 = {str(year6): {"qty": int(ym7)}}
            data3.update(data7)
        else:
            data7 = {str(year6): {"qty":"0"}}
            data3.update(data7)

        b7 = df_saleshstry.isin([year_month7]).any().any()
        if b7 != False:
            ym8 = int(df_saleshstry[(df_saleshstry['year_month'] == year_month7)]['order_qty'].sum())
            data8 = {str(year7): {"qty": int(ym8)}}
            data4.update(data8)
        else:
            data8 = {str(year7): {"qty": "0"}}
            data4.update(data8)

        b8 = df_saleshstry.isin([year_month8]).any().any()
        if b8 != False:
            ym9 = int(df_saleshstry[(df_saleshstry['year_month'] == year_month8)]['order_qty'].sum())
            data9 = {str(year8): {"qty": int(ym9)}}
            data1.update(data9)
        else:
            data9 = {str(year8): {"qty": "0"}}
            data1.update(data9)

        b9 = df_saleshstry.isin([year_month9]).any().any()
        if b9 != False:
            ym10 = int(df_saleshstry[(df_saleshstry['year_month'] == year_month9)]['order_qty'].sum())
            data10 = {str(year9): {"qty": int(ym10)}}
            data2.update(data10)
        else:
            data10 = {str(year9): {"qty": "0"}}
            data2.update(data10)

        b10 = df_saleshstry.isin([year_month10]).any().any()
        if b10 != False:
            ym11 = int(df_saleshstry[(df_saleshstry['year_month'] == year_month10)]['order_qty'].sum())
            data11 = {str(year10): {"qty": int(ym11)}}
            data3.update(data11)
        else:
            data11 = {str(year10): {"qty": "0"}}
            data3.update(data11)

        b11 = df_saleshstry.isin([year_month11]).any().any()
        if b11 != False:
            ym12 = int(df_saleshstry[(df_saleshstry['year_month'] == year_month11)]['order_qty'].sum())
            data12 = {str(year11): {"qty": int(ym12)}}
            data4.update(data12)
        else:
            data12 = {str(year11): {"qty": "0"}}
            data4.update(data12)

        b12 = df_saleshstry.isin([year_month12]).any().any()
        if b12 != False:
            ym13 = int(df_saleshstry[(df_saleshstry['year_month'] == year_month12)]['order_qty'].sum())
            data13 = {str(year12): {"qty": int(ym13)}}
            data1.update(data13)
        else:
            data13 = {str(year12): {"qty": "0"}}
            data1.update(data13)

        b13 = df_saleshstry.isin([year_month13]).any().any()
        if b13 != False:
            ym14 = int(df_saleshstry[(df_saleshstry['year_month'] == year_month13)]['order_qty'].sum())
            data14 = {str(year13): {"qty": int(ym14)}}
            data2.update(data14)
        else:
            data14 = {str(year13): {"qty": "0"}}
            data2.update(data14)

        b14 = df_saleshstry.isin([year_month14]).any().any()
        if b14 != False:
            ym15 = int(df_saleshstry[(df_saleshstry['year_month'] == year_month14)]['order_qty'].sum())
            data15 = {str(year14): {"qty": int(ym15)}}
            data3.update(data15)
        else:
            data15 = {str(year14): {"qty": "0"}}
            data3.update(data15)

        b15 = df_saleshstry.isin([year_month15]).any().any()
        if b15 != False:
            ym16 = int(df_saleshstry[(df_saleshstry['year_month'] == year_month15)]['order_qty'].sum())
            data16 = {str(year15): {"qty": int(ym16)}}
            data4.update(data16)
        else:
            data16 = {str(year15): {"qty": "0"}}
            data4.update(data16)

        years = [year0,year1,year2,year3,year4,year5,
                 year6,year7,year8,year9,year10,year11,
                 year12,year13,year14,year15]
        years = list(dict.fromkeys(years))
        months = [month0,month1,month2,month3]
        data = {'sales_data':sales_data,'years':years,'months':months}
    return JsonResponse(data,safe=False)


def set_expense_line(request):
    if request.method == "POST":
        jsondata = json.loads(request.body.decode('utf-8'))
        action = jsondata.get('params').get('action')
        type = jsondata.get('params').get('type')
        entity_gid = request.session['Entity_gid']
        create_by = request.session['Emp_gid']
        jsondata["params"]["classification"] = {"Entity_Gid": entity_gid}
        datas = json.dumps(jsondata)
        params = {'action':action,'type': type,'create_by':create_by}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        result = requests.post("" + ip + "/Expense_Line_API", params=params, headers=headers, data=datas,verify=False)
        results = result.content.decode("utf-8")
        return JsonResponse(json.loads(results), safe=False)