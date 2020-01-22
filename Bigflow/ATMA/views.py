import io

import requests
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import Bigflow.Core.models as common
from datetime import datetime
from django.conf import settings
from django.core.files.base import ContentFile
from Bigflow.ATMA.model import mATMA
ip = common.localip()
token = common.token()
headers = {"content-type": "application/json", "Authorization": "" + token + ""}

def ATMA_PartnerSummary(request):
    return render(request,'ATMA_PartnerSummary.html')

def atma_activitydetails(request):
    return render(request, 'atma_activitydetails.html')

def atma_activitydetailsview(request):
    return render(request, 'atma_activitydetailsview.html')


def atma_activitydetailsedit(request):
    return render(request, 'atma_activitydetailsedit.html')


def atma_catalogcreation(request):
    return render(request, "atma_catalogcreation.html")

def AtmaPartnerMaker (request):
    return render(request, "atma_partnermaker.html")

def atmacatalogset(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Catalog Details':
           grp = jsondata.get('Group')
           action = jsondata.get('Action')
           typ = jsondata.get('Group')
           data = json.dumps(jsondata.get('data').get('Params'))
           dataw = json.dumps(jsondata.get('data').get('Classification'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atmaCatalog_Setapi", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

       if (jsondata.get('Group')) == 'Catalog_Details_Update':
           grp = jsondata.get('Group')
           action = jsondata.get('Action')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data').get('Params'))
           dataw = json.dumps(jsondata.get('data').get('Classification'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atmaCatalog_Setapi", params=params, data=datas, headers=headers,
                                verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

       if (jsondata.get('Group')) == 'CATALOG_ASSIGN':
           grp = jsondata.get('Group')
           action = jsondata.get('Action')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data').get('Params'))
           dataw = json.dumps(jsondata.get('data').get('Classification'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atmaCatalog_Setapi", params=params, data=datas, headers=headers,
                                verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def atmacatalog_get(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Catalog_Details':
           grp = jsondata.get('Group')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atmaCatalog_Getapi", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

       if (jsondata.get('Group')) == 'partner_product':
           grp = jsondata.get('Group')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atmaCatalog_Getapi", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def atma_getdata(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Params').get('Group')) == 'ATMASUMMARY':
           obj = mATMA.ATMA_model()
           grp = jsondata.get('Params').get('Group')
           action = jsondata.get('Params').get('Action')
           params = {'Group': "" + grp + "", 'Action': "" + action + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata)
           resp = requests.post("" + ip + "/GET_ATMA_Data", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)
       if (jsondata.get('Params').get('Group')) == 'QUERYSUMMARY':
           obj = mATMA.ATMA_model()
           grp = jsondata.get('Params').get('Group')
           action = jsondata.get('Params').get('Action')
           params = {'Group': "" + grp + "", 'Action': "" + action + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata)
           resp = requests.post("" + ip + "/GET_ATMA_Data", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)
       if (jsondata.get('Params').get('Group')) == 'ATMAPAYMENTSUMMARY':
           grp = jsondata.get('Params').get('Group')
           action = jsondata.get('Params').get('Action')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Action': "" + action + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata)
           resp = requests.post("" + ip + "/GET_ATMA_Data", params=params, data=datas, headers=headers, verify=False)
           return HttpResponse(resp)

def atma_ProductCatSubCat_get(request):
  if request.method == 'POST':
      jsondata = json.loads(request.body.decode('utf-8'))
      if (jsondata.get('Group')) == 'Activity_Group':
          grp = jsondata.get('Group')
          typ = jsondata.get('Type')
          data = json.dumps(jsondata.get('data'))
          params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
          headers = {"content-type": "application/json", "Authorization": "" + token + ""}
          datas = json.dumps(jsondata.get('data'))
          resp = requests.post("" + ip + "/atma_ProductCatSubCat_getAPI", params=params, data=datas, headers=headers, verify=False)
          response = resp.content.decode("utf-8")
          return HttpResponse(response)

def atma_changerequest_activationupdate(request):
    if request.method == 'POST':
        jsondata=json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'Activation_Request':
            obj=mATMA.ATMA_model()
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            params = {'Group': "" + grp + "", 'Action': "" + action + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/Update_changerequest_API", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def atma_getdirectordata(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Params').get('Group')) == 'ATMASUMMARY':
            obj = mATMA.ATMA_model()
            grp = jsondata.get('Params').get('Group')
            action = jsondata.get('Params').get('Action')
            params = {'Group': "" + grp + "", 'Action': "" + action + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/GET_ATMA_Directors_Data", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def atma_viewdata(request):
    return render(request,'ATMA_viewdata.html')

def atma_partneradd(request):
    return render(request,'ATMA_Partneradd.html')

def atma_activityaddIndex(request):
    return render(request, "ATMA_Activity.html")
def create_activity_details(request):
    return render(request, "create_activity_details.html")

def atma_ActivitydetailsIndex(request):
   return render(request, "atma_activitydetails.html")

def create_catalog_details(request):
   return render(request, "create_catalog_details.html")
def Partner_Address(request):
   return render(request, "Partner_Address.html")
def Partner_Contact(request):
   return render(request, "Partner_Contact.html")

def Query_Page(request):
   return render(request, "Query_Page.html")

def atma_activitydetailsset(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Activity_Details':
           grp = jsondata.get('Group')
           action=jsondata.get('Action')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data').get('Params'))
           dataw = json.dumps(jsondata.get('data').get('Classification'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atma_Activitydetails_Set", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

       if (jsondata.get('Group')) == 'Activity_Details_Update':
           grp = jsondata.get('Group')
           action=jsondata.get('Action')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data').get('Params'))
           dataw = json.dumps(jsondata.get('data').get('Classification'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atma_Activitydetails_Set", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def atma_activitydetailsget(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Activity_Details':
           grp = jsondata.get('Group')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atma_Activitydetails_Get", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def atmaPartnerPayment_Set(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Header Details':
           grp = jsondata.get('Group')
           action = jsondata.get('Action')
           typ = jsondata.get('Group')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atmaPartnerPayment_Setapi", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

       if (jsondata.get('Params').get('Group')) == 'PAYMODESUMMARY':
           grp = jsondata.get('Params').get('Group')
           action = jsondata.get('Params').get('Action')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Action': "" + action + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata)
           resp = requests.post("" + ip + "/atmaPartnerPayment_Setapi", params=params, data=datas, headers=headers, verify=False)
           return HttpResponse(resp)

       elif (jsondata.get('Params').get('Group')) == 'MoveToRM':
           group=jsondata.get('Params').get('Group')
           action=jsondata.get('Params').get('Action')
           data=json.dumps(jsondata.get('data'))
           params = {'Group':"" + group + "", 'Action':"" + action + ""}
           headers = {"content-type": "application/json", "Authorization":"" + token + ""}
           datas=json.dumps(jsondata)
           resp = requests.post("" + ip + "/atmaPartnerPayment_Setapi", params=params, data=datas, headers=headers, verify=False)
           return HttpResponse(resp)
       elif (jsondata.get('Params').get('Group')) == 'UPDATEPAYMODESUMMARY':
           grp = jsondata.get('Params').get('Group')
           action = jsondata.get('Params').get('Action')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Action': "" + action + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata)
           resp = requests.post("" + ip + "/atmaPartnerPayment_Setapi", params=params, data=datas, headers=headers, verify=False)
           return HttpResponse(resp)


def atma_addpayment(request):
    return render(request,"Atma_AddPayment.html")

def atma_paymentdetails(request):
    return render(request,'atma_paymentdetails.html')

def atma_attachmentdetails(request):
    return render(request,'atma_attachmentdetails.html')

def atma_branchdetailsdropdown(request):
    if request.method == 'POST':
        report_data = mATMA.ATMA_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        report_data.type = jsondata.get('Params').get('Type')
        report_data.gid = jsondata.get('Params').get('bank_gid')
        report_data.finaldata = json.dumps({'branch_gid': report_data.gid})
        report_data.emptyjson = json.dumps({})
        module_name = report_data.bankbranch_module()
        jdata = module_name.to_json(orient='records')
        return HttpResponse(jdata)



def atma_docgroupset(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Document_Group':
           grp = jsondata.get('Group')
           action=jsondata.get('Action')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atmaapi_Docgroup_Set", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def atma_doc_get(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Document_Group':
           grp = jsondata.get('Group')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atmaAttachment_apiurl", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def atma_attachmentupload(request):
   if request.method == 'POST' and request.FILES['file']:
        current_month = datetime.now().strftime('%m')
        current_day = datetime.now().strftime('%d')
        current_year_full = datetime.now().strftime('%Y')
        save_path = str(settings.MEDIA_ROOT) + '/Atma_Documents/' + str(current_year_full) + '/' + str(current_month) + '/' + str(current_day) + '/' + str(request.POST['name'])
        print(save_path)
        path = default_storage.save(str(save_path), request.FILES['file'])

        grp = request.POST['Group']
        action=request.POST['Action']
        typ = request.POST['Type']

        data = {"Documents_Partnergid": request.POST['Documents_Partnergid'],"Documents_Docgroupgid": request.POST['Documents_Docgroupgid'],
                "Documents_Period": request.POST['Documents_Period'],"Description": request.POST['Description'],"File_Name": request.POST['File_Name'],
                                      "File_Path": save_path, "Entity_Gid":request.POST['Entity_Gid'],"Create_By": request.POST['Create_By']
        }

        datas = json.dumps(data)

        params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}

        resp = requests.post("" + ip + "/atma_Docgroup_Setapi", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def atma_gettaxdetails(request):
    jsondata = json.loads(request.body.decode('utf-8'))
    if (jsondata.get('Params').get('Group')) == 'GETTAXTYPE':
        obj = mATMA.ATMA_model()
        grp = jsondata.get('Params').get('Group')
        action = jsondata.get('Params').get('Action')
        params = {'Group': "" + grp + "", 'Action': "" + action + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata)
        resp = requests.post("" + ip + "/Gettaxdetails", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
    elif (jsondata.get('Params').get('Group')) == 'TAXINSERTSUMMARY':
        obj = mATMA.ATMA_model()
        grp = jsondata.get('Params').get('Group')
        action = jsondata.get('Params').get('Action')
        params = {'Group': "" + grp + "", 'Action': "" + action + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata)
        resp = requests.post("" + ip + "/Gettaxdetails", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
    elif (jsondata.get('Params').get('Group')) == 'ATMATAXSUMMARY':
        obj = mATMA.ATMA_model()
        grp = jsondata.get('Params').get('Group')
        action = jsondata.get('Params').get('Action')
        params = {'Group': "" + grp + "", 'Action': "" + action + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata)
        resp = requests.post("" + ip + "/Gettaxdetails", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
        return HttpResponse
def atma_taxdetailsfileupload(request):
    if request.POST['Group'] == "TAXINSERTSUMMARYEXEMPTEDYES":
        if request.method == 'POST' and request.FILES['file']:
            current_month = datetime.now().strftime('%m')
            current_day = datetime.now().strftime('%d')
            current_year_full = datetime.now().strftime('%Y')
            save_path = str(settings.MEDIA_ROOT) + '/Atma_TDSDocuments/' + str(current_year_full) + '/' + str(
                current_month) + '/' + str(current_day) + '/' + str(request.POST['name'])
            print(save_path)
            path = default_storage.save(str(save_path), request.FILES['file'])
            grp = request.POST['Group']
            action = request.POST['Action']
            data = {"Tax_Gid": request.POST['Tax_Gid'],
                    "TaxDetails_Partner_Gid": request.POST['TaxDetails_Partner_Gid'],
                    "TaxDetails_Partnerbranchcode":request.POST['TaxDetails_Partnerbranchcode'],
                    "TaxDetails_Partner_Code": request.POST['TaxDetails_Partner_Code'],
                    "TaxDetails_Partner_Type": request.POST['TaxDetails_Partner_Type'],
                    "TaxDetails_TaxNo": request.POST['TaxDetails_TaxNo'],
                    "TaxSubDetails_TaxRate_Gid": request.POST['TaxSubDetails_TaxRate_Gid'],
                    "TaxSubDetails_ExcemthroSold": request.POST['TaxSubDetails_ExcemthroSold'],
                    "TaxSubDetails_TaxRate": request.POST['TaxSubDetails_TaxRate'],
                    "TaxSubDetails_IsExcempted": request.POST['TaxSubDetails_IsExcempted'],
                    "TaxSubDetails_ExcemTo": request.POST['TaxSubDetails_ExcemTo'],
                    "TaxSubDetails_ExcemFrom": request.POST['TaxSubDetails_ExcemFrom'],
                    "TaxSubDetails_ExcemRate": request.POST['TaxSubDetails_ExcemRate'],
                    "FileName": request.POST['FileName'], "FilePath": save_path,
                    "Create_By": request.POST['Create_By'],
                    "TaxDetails_Is_MSME": request.POST['TaxDetails_Is_MSME']
                    }, {"Entity_gid": request.session['Entity_gid']}
            datas = json.dumps(data)
            params = {'Group': "" + grp + "", 'Action': "" + action + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/Gettaxdetails", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
    if request.POST['Group'] == "TAXINSERTSUMMARYEXEMPTEDNO":
        grp = request.POST['Group']
        action = request.POST['Action']
        save_path = ""
        data = {"Tax_Gid": request.POST['Tax_Gid'],
                "TaxDetails_Partner_Gid":request.POST['TaxDetails_Partner_Gid'],
                "TaxDetails_Partnerbranchcode": request.POST['TaxDetails_Partnerbranchcode'],
                "TaxDetails_Partner_Code":request.POST['TaxDetails_Partner_Code'],
                "TaxDetails_Partner_Type":request.POST['TaxDetails_Partner_Type'],
                "TaxDetails_TaxNo": request.POST['TaxDetails_TaxNo'],
                "TaxSubDetails_TaxRate_Gid": request.POST['TaxSubDetails_TaxRate_Gid'],
                "TaxDetails_Is_MSME": request.POST['TaxDetails_Is_MSME'],
                "TaxSubDetails_ExcemthroSold": request.POST['TaxSubDetails_ExcemthroSold'],
                "TaxSubDetails_TaxRate": request.POST['TaxSubDetails_TaxRate'],
                "TaxSubDetails_IsExcempted": request.POST['TaxSubDetails_IsExcempted'],
                "TaxSubDetails_ExcemTo": request.POST['TaxSubDetails_ExcemTo'],
                "TaxSubDetails_ExcemFrom": request.POST['TaxSubDetails_ExcemFrom'],
                "TaxSubDetails_ExcemRate": request.POST['TaxSubDetails_ExcemRate'],
                "FileName": request.POST['FileName'], "FilePath": save_path,
                "Create_By": request.POST['Create_By']
                }, {"Entity_gid": request.session['Entity_gid']}
        datas = json.dumps(data)
        params = {'Group': "" + grp + "", 'Action': "" + action + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Gettaxdetails", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
    if request.POST['Group'] == "TAXINSERTSUMMARYEXEMPTEDUPDATENO":
        grp = request.POST['Group']
        action = request.POST['Action']
        data = {"Tax_Gid": request.POST['Tax_Gid'],
            "TaxDetails_Partner_Gid": request.POST['TaxDetails_Partner_Gid'],
            "TaxDetails_Partnerbranchcode": request.POST['TaxDetails_Partnerbranchcode'],
            "TaxDetails_Partner_Code": request.POST['TaxDetails_Partner_Code'],
            "TaxDetails_Partner_Type": request.POST['TaxDetails_Partner_Type'],
            "TaxDetails_Is_MSME": request.POST['TaxDetails_Is_MSME'],
            "TaxDetails_TaxNo": request.POST['TaxDetails_TaxNo'],
            "TaxDetails_Gid": request.POST['TaxDetails_Gid'],
            "TaxSubDetails_TaxRate_Gid": request.POST['TaxSubDetails_TaxRate_Gid'],
            "TaxSubDetails_TaxRate": request.POST['TaxSubDetails_TaxRate'],
            "TaxSubDetails_IsExcempted": request.POST['TaxSubDetails_IsExcempted'],
            }, {"Entity_gid": request.session['Entity_gid'], "Update_By": request.POST['Create_By']}
        datas = json.dumps(data)
        params = {'Group': "" + grp + "", 'Action': "" + action + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Gettaxdetails", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
    if request.POST['Group'] == "TAXINSERTSUMMARYEXEMPTEDUPDATEYES":
        if request.method == 'POST' and request.FILES['file']:
            current_month = datetime.now().strftime('%m')
            current_day = datetime.now().strftime('%d')
            current_year_full = datetime.now().strftime('%Y')
            save_path = str(settings.MEDIA_ROOT) + '/Atma_TDSDocuments/' + str(current_year_full) + '/' + str(
                current_month) + '/' + str(current_day) + '/' + str(request.POST['name'])
            print(save_path)
            path = default_storage.save(str(save_path), request.FILES['file'])
            grp = request.POST['Group']
            action = request.POST['Action']
            data = {"Tax_Gid": request.POST['Tax_Gid'],
                    "TaxDetails_Partner_Gid": request.POST['TaxDetails_Partner_Gid'],
                    "TaxDetails_Partnerbranchcode": request.POST['TaxDetails_Partnerbranchcode'],
                    "TaxDetails_Partner_Code": request.POST['TaxDetails_Partner_Code'],
                    "TaxDetails_Partner_Type": request.POST['TaxDetails_Partner_Type'],
                    "TaxDetails_TaxNo": request.POST['TaxDetails_TaxNo'],
                    "TaxDetails_Gid": request.POST['TaxDetails_Gid'],
                    "TaxDetails_Is_MSME": request.POST['TaxDetails_Is_MSME'],
                    "TaxSubDetails_TaxRate_Gid": request.POST['TaxSubDetails_TaxRate_Gid'],
                    "TaxSubDetails_ExcemthroSold": request.POST['TaxSubDetails_ExcemthroSold'],
                    "TaxSubDetails_TaxRate": request.POST['TaxSubDetails_TaxRate'],
                    "TaxSubDetails_IsExcempted": request.POST['TaxSubDetails_IsExcempted'],
                    "TaxSubDetails_ExcemTo": request.POST['TaxSubDetails_ExcemTo'],
                    "TaxSubDetails_ExcemFrom": request.POST['TaxSubDetails_ExcemFrom'],
                    "TaxSubDetails_ExcemRate": request.POST['TaxSubDetails_ExcemRate'],
                    "File_Name": request.POST['File_Name'], "FilePath": save_path
                    }, {"Entity_gid": request.session['Entity_gid'], "Update_By": request.POST['Create_By']}
            datas = json.dumps(data)
            params = {'Group': "" + grp + "", 'Action': "" + action + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/Gettaxdetails", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
    if request.POST['Group'] == "TAXINSERTSUMMARYEXEMPTEDUPDATEYESNOFILE":
        grp = request.POST['Group']
        action = request.POST['Action']
        data = {"Tax_Gid": request.POST['Tax_Gid'],
                "TaxDetails_Partner_Gid": request.POST['TaxDetails_Partner_Gid'],
                "TaxDetails_Partnerbranchcode": request.POST['TaxDetails_Partnerbranchcode'],
                "TaxDetails_Partner_Code": request.POST['TaxDetails_Partner_Code'],
                "TaxDetails_Partner_Type": request.POST['TaxDetails_Partner_Type'],
                "TaxDetails_TaxNo": request.POST['TaxDetails_TaxNo'],
                "TaxDetails_Gid": request.POST['TaxDetails_Gid'],
                "TaxDetails_Is_MSME": request.POST['TaxDetails_Is_MSME'],
                "TaxSubDetails_TaxRate_Gid": request.POST['TaxSubDetails_TaxRate_Gid'],
                "TaxSubDetails_ExcemthroSold": request.POST['TaxSubDetails_ExcemthroSold'],
                "TaxSubDetails_TaxRate": request.POST['TaxSubDetails_TaxRate'],
                "TaxSubDetails_IsExcempted": request.POST['TaxSubDetails_IsExcempted'],
                "TaxSubDetails_ExcemTo": request.POST['TaxSubDetails_ExcemTo'],
                "TaxSubDetails_ExcemFrom": request.POST['TaxSubDetails_ExcemFrom'],
                "TaxSubDetails_ExcemRate": request.POST['TaxSubDetails_ExcemRate'],
                "FilePath": request.POST['FilePath'],
                "File_Name": request.POST['File_Name'],
                }, {"Entity_gid": request.session['Entity_gid'], "Update_By": request.POST['Create_By']}
        datas = json.dumps(data)
        params = {'Group': "" + grp + "", 'Action': "" + action + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        resp = requests.post("" + ip + "/Gettaxdetails", params=params, data=datas, headers=headers,
                         verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)
        return HttpResponse
def atma_updateattacment_details(request):
   if request.POST['Group'] == "Document_Update":
       if request.method == 'POST' and request.FILES['file']:
           current_month = datetime.now().strftime('%m')
           current_day = datetime.now().strftime('%d')
           current_year_full = datetime.now().strftime('%Y')
           save_path = str(settings.MEDIA_ROOT) + '/Atma_Documents/' + str(current_year_full) + '/' + str(
               current_month) + '/' + str(current_day) + '/' + str(request.POST['name'])
           print(save_path)
           path = default_storage.save(str(save_path), request.FILES['file'])
           grp = request.POST['Group']
           action = request.POST['Action']
           typ = request.POST['Type']
           data = {"Documents_Gid": request.POST['Documents_Gid'],
                   "Documents_Docgroupgid": request.POST['Documents_Docgroupgid'],
                  "Description": request.POST['Description'],
                   "File_Name": request.POST['File_Name'],
                   "File_Path":save_path,
                   "Update_By": request.session['Emp_gid'],
                   }
           datas = json.dumps(data)
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           resp = requests.post("" + ip + "/atma_Updateattachment", params=params, data=datas, headers=headers,
                                verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)
   if request.POST['Group'] == "Document_Updatenofile":
       if request.method == 'POST':
           current_month = datetime.now().strftime('%m')
           current_day = datetime.now().strftime('%d')
           current_year_full = datetime.now().strftime('%Y')
           save_path = str(settings.MEDIA_ROOT) + '/Atma_Documents/' + str(current_year_full) + '/' + str(
               current_month) + '/' + str(current_day) + '/' + str(request.POST['name'])
           print(save_path)
           grp = request.POST['Group']
           action = request.POST['Action']
           typ = request.POST['Type']
           data = {"Documents_Gid": request.POST['Documents_Gid'],
                   "Documents_Docgroupgid": request.POST['Documents_Docgroupgid'],
                  "Description": request.POST['Description'],
                   "File_Name": request.POST['File_Name'],
                   "File_Path": save_path,
                   "Update_By": request.session['Emp_gid'],
                   }
           datas = json.dumps(data)
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           resp = requests.post("" + ip + "/atma_Updateattachment", params=params, data=datas, headers=headers,
                                verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)
   return render()

def atma_taxviewpage(request):
    return render(request,'atma_taxviewpage.html')

def atma_tax_details(request):
    return render(request,'atma_tax_details.html')

def atma_ProductCatSubCat_get(request):
  if request.method == 'POST':
      jsondata = json.loads(request.body.decode('utf-8'))
      if (jsondata.get('Group')) == 'Activity_Group':
          grp = jsondata.get('Group')
          typ = jsondata.get('Type')
          data = json.dumps(jsondata.get('data'))
          params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
          headers = {"content-type": "application/json", "Authorization": "" + token + ""}
          datas = json.dumps(jsondata.get('data'))
          resp = requests.post("" + ip + "/atma_ProductCatSubCat_getAPI", params=params, data=datas, headers=headers, verify=False)
          response = resp.content.decode("utf-8")
          return HttpResponse(response)


def atma_activity_get(request):
  if request.method == 'POST':
      jsondata = json.loads(request.body.decode('utf-8'))
      if (jsondata.get('Group')) == 'Activity_Group':
          grp = jsondata.get('Group')
          typ = jsondata.get('Type')
          data = json.dumps(jsondata.get('data'))
          params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
          headers = {"content-type": "application/json", "Authorization": "" + token + ""}
          datas = json.dumps(jsondata.get('data'))
          resp = requests.post("" + ip + "/atma_Activityget", params=params, data=datas, headers=headers, verify=False)
          response = resp.content.decode("utf-8")
          return HttpResponse(response)

def atma_activityaddedit(request):
  if request.method == 'POST':
      jsondata = json.loads(request.body.decode('utf-8'))
      if (jsondata.get('Group')) == 'Activity_ADD':
          grp = jsondata.get('Group')
          action=jsondata.get('Action')
          typ = jsondata.get('Type')
          data = json.dumps(jsondata.get('data').get('Params'))
          dataw = json.dumps(jsondata.get('data').get('Classification'))
          params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ ""}
          headers = {"content-type": "application/json", "Authorization": "" + token + ""}
          datas = json.dumps(jsondata.get('data'))
          resp = requests.post("" + ip + "/atma_ActivitySet_APIurl", params=params, data=datas, headers=headers, verify=False)
          response = resp.content.decode("utf-8")
          return HttpResponse(response)
      if (jsondata.get('Group')) == 'Activity_UPDATE':
          grp = jsondata.get('Group')
          action = jsondata.get('Action')
          typ = jsondata.get('Type')
          data = json.dumps(jsondata.get('data').get('Params'))
          dataw = json.dumps(jsondata.get('data').get('Classification'))
          params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
          headers = {"content-type": "application/json", "Authorization": "" + token + ""}
          datas = json.dumps(jsondata.get('data'))
          resp = requests.post("" + ip + "/atma_ActivitySet_APIurl", params=params, data=datas, headers=headers, verify=False)
          response = resp.content.decode("utf-8")
          return HttpResponse(response)

# Start Profile page...
def atma_profilepage(request):
    return render(request,'atma_profilepage.html')
def atma_Productdetails(request):
    return render(request,'atma_Productdetails.html')

def atma_Branchdetails(request):
    return render(request,'atma_Branchdetails.html')

def atma_Clientdetails(request):
    return render(request,'atma_Clientdetails.html')

def atma_Contractdetails(request):
    return render(request,'atma_Contractdetails.html')

def atma_SetClientdetails(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'ClientDetails_ADD':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_clientdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        if (jsondata.get('Group')) == 'ClientDetails_GET':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_clientdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        if (jsondata.get('Group')) == 'ClientDetails_Update':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_clientdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def atma_SetContractdetails(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'ContractDetails_SET':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_contractdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        if (jsondata.get('Group')) == 'ContractDetails_GET':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_contractdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        if (jsondata.get('Group')) == 'ContractDetails_Update':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_contractdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def atma_SetBranchdetails(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'BranchDetails_Set':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_branchdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        if (jsondata.get('Group')) == 'BranchDetails_GET':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_branchdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        if (jsondata.get('Group')) == 'BranchDetails_Update':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_branchdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def atma_BasicProfilDetails(request):
    return render(request,'atma_BasicProfilDetails.html')

def atma_Setbasicprofildedetails(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'BasicProfile_Set':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_basicprofiledetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        if (jsondata.get('Group')) == 'Partnerprofile_Get':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_basicprofiledetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def atma_PartnerCheckerPage(request):
    return render(request,'atma_PartnerCheckerPage.html')

def atma_PartnerCheckerApprovalPage(request):
    return render(request,'atma_PartnerCheckerApprovalPage.html')

def atma_CheckerDetails(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'Checker_Get':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_getcheckerdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        if (jsondata.get('Group')) == 'Checker_Status':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Type')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/atma_getcheckerdetails_api", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def prmakerset(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'PRMAKER Details':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Group')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/Prmaker_Setapi", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def prmaker_get(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'PRMAKER Details':
           grp = jsondata.get('Group')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/PRMAKERapi", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def AtmaPartnerDeactivationRequest(request):
    return render(request, "atma_partnerdeactivation_request.html")

def AtmaPartnerActivationRequest(request):
   return render(request, "atma_partneractivation_request.html")

def AtmaPartnerTerminationRequest(request):
   return render(request, "atma_partnertermination_request.html")

def partdisapproval_get(request):
  if request.method == 'POST':
      jsondata = json.loads(request.body.decode('utf-8'))
      if (jsondata.get('Group')) == 'Partner Inactivate':
          grp = jsondata.get('Group')
          typ = jsondata.get('Type')
          data = json.dumps(jsondata.get('data'))
          params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
          headers = {"content-type": "application/json", "Authorization": "" + token + ""}
          datas = json.dumps(jsondata.get('data'))
          resp = requests.post("" + ip + "/Partnerdisapproval", params=params, data=datas, headers=headers, verify=False)
          response = resp.content.decode("utf-8")
          return HttpResponse(response)

def atma_profileproduct_get(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Partner Product':
           grp = jsondata.get('Group')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data'))
           params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atma_profileproduct_getapi", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def atma_profileproduct_set(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Partner Product':
           grp = jsondata.get('Group')
           action=jsondata.get('Action')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data').get('Params'))
           dataw = json.dumps(jsondata.get('data').get('Classification'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/atma_profileproduct_setapi", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def partnerdeactivate_set(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       if (jsondata.get('Group')) == 'Partner Inactive':
           grp = jsondata.get('Group')
           action=jsondata.get('Action')
           typ = jsondata.get('Type')
           data = json.dumps(jsondata.get('data').get('Params'))
           dataw = json.dumps(jsondata.get('data').get('Classification'))
           params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ+ ""}
           headers = {"content-type": "application/json", "Authorization": "" + token + ""}
           datas = json.dumps(jsondata.get('data'))
           resp = requests.post("" + ip + "/PartnerdeactivateSet_api", params=params, data=datas, headers=headers, verify=False)
           response = resp.content.decode("utf-8")
           return HttpResponse(response)

def partapproval_get(request):
  if request.method == 'POST':
      jsondata = json.loads(request.body.decode('utf-8'))
      if (jsondata.get('Group')) == 'Partner Activate':
          grp = jsondata.get('Group')
          typ = jsondata.get('Type')
          data = json.dumps(jsondata.get('data'))
          params = {'Group': "" + grp + "", 'Type': "" + typ + ""}
          headers = {"content-type": "application/json", "Authorization": "" + token + ""}
          datas = json.dumps(jsondata.get('data'))
          resp = requests.post("" + ip + "/Partnerapproval", params=params, data=datas, headers=headers, verify=False)
          response = resp.content.decode("utf-8")
          return HttpResponse(response)

def atma_Approval_Summary_Page(request):
    return render(request,'atma_Approval_Summary_Page.html')

def atma_Approval_ViewDetails_Page(request):
    return render(request,'atma_Approval_ViewDetails_Page.html')

def atma_Approval_Taxdetails_Page(request):
    return render(request,'atma_Approval_Taxdetails_Page.html')
def atma_Approval_Paymentdetails_Page(request):
    return render(request,'atma_Approval_Paymentdetails_Page.html')

def atma_Approval_Attachmentdetails_Page(request):
    return render(request,'atma_Approval_Attachmentdetails_Page.html')

def atma_Approval_ProfileBasic_Page(request):
    return render(request,'atma_Approval_ProfileBasic_Page.html')

def atma_Approval_ProfileBranch_Page(request):
    return render(request,'atma_Approval_ProfileBranch_Page.html')

def atma_Approval_ProfileClient_Page(request):
    return render(request,'atma_Approval_ProfileClient_Page.html')

def atma_Approval_ProfileContract_Page(request):
    return render(request,'atma_Approval_ProfileContract_Page.html')

def atma_Approval_ActivityDetails_Page(request):
    return render(request,'atma_Approval_Activity.html')

def atma_Approval_ActivityDetails_Summary(request):
    return render(request,'atma_Approval_ActivityDetails_Summary.html')

def atma_Approval_Catalogcreation(request):
    return render(request,'atma_Approval_Catalogcreation.html')

def atma_Approval_ProfileProduct(request):
    return render(request,'atma_Approval_ProfileProduct.html')

def atma_Approval_Stages(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'RM_To_VMU_Update':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Group')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/approval_stagesapi", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        if (jsondata.get('Group')) == 'APPROVED_GROUP':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Group')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/approval_stagesapi", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def atma_Approval_Request_Change(request):
    return render(request,'atma_ApprovedRequest_Change.html')

def atma_ApprovedPartner_Get(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'Partner_Approval_Get':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Group')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/approval_paartnergetapi", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        if (jsondata.get('Group')) == 'Partner_ChangeRequest':
            grp = jsondata.get('Group')
            action = jsondata.get('Action')
            typ = jsondata.get('Group')
            data = json.dumps(jsondata.get('data').get('Params'))
            dataw = json.dumps(jsondata.get('data').get('Classification'))
            params = {'Group': "" + grp + "", 'Action': "" + action + "", 'Type': "" + typ + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/approval_paartnergetapi", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

        elif (jsondata.get('Params').get('Group')) == 'APPROVER_TO_REQUEST':
            group = jsondata.get('Params').get('Group')
            action = jsondata.get('Params').get('Action')
            data = json.dumps(jsondata.get('data'))
            params = {'Group': "" + group + "", 'Action': "" + action + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/approval_paartnergetapi", params=params, data=datas, headers=headers,
                                 verify=False)
            return HttpResponse(resp)

        elif (jsondata.get('Params').get('Group')) == 'VIEW_TO_CANCEL':
            group = jsondata.get('Params').get('Group')
            action = jsondata.get('Params').get('Action')
            data = json.dumps(jsondata.get('data'))
            params = {'Group': "" + group + "", 'Action': "" + action + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/approval_paartnergetapi", params=params, data=datas, headers=headers,
                                 verify=False)
            return HttpResponse(resp)

def atma_changerequest_summarypage(request):
    return render(request,'atma_changerequest_summarypage.html')

def Query_Page(request):
   return render(request, "Query_Page.html")

