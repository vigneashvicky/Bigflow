from __future__ import unicode_literals
import base64

#import utl as utl
from django.contrib.sites import requests
import json
from django.http import JsonResponse, HttpResponse
from reportlab.lib import yaml
from Bigflow.API import view_fa, view_sales, view_master
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import Bigflow.Core.models as common
import requests
#import base64image

ip = common.localip()
token = common.token()

# Asset Make
def fa_summary(request):
    return render(request, 'fa_summary.html')
def fa_assetadd(request):
    return render(request, 'fa_assetadd.html')
def fa_assetchecker(request):
    return render(request, 'fa_assetchecker.html')

# capitalise date
def fa_capdate_change(request):
    return render(request, 'fa_capdate_change.html')
def fa_capdate_changeplus(request):
    return render(request, 'fa_capdate_changeplus.html')
def fa_capdate_checker(request):
    return render(request, 'fa_capdate_checker.html')

# ParentChild
def fa_asset_parentchild(request):
    return render(request, 'fa_asset_parentchild.html')
def fa_asset_parentchildcheck(request):
    return render(request, 'fa_asset_parentchildcheck.html')

# writeoff checker
def fa_writeoff(request):
    return render(request, 'fa_writeoff.html')
def fa_writeoffplus(request):
    # utl.check_authorization(request)(request)
    return render(request, 'fa_writeoffplus.html')
def fa_writeoff_check(request):
    return render(request, 'fa_writeoff_check.html')
# impairment
def fa_impairment(request):
    return render(request, 'fa_impairment.html')
def fa_impairmentplus(request):
    return render(request, 'fa_impairmentplus.html')
def fa_impairment_check(request):
    return render(request, 'fa_impairment_check.html')
# Merge
def fa_asset_merge(request):
    return render(request, 'fa_asset_merge.html')
def fa_asset_merge_plus(request):
    return render(request, 'fa_asset_merge_plus.html')
def fa_asset_merge_checker(request):
    return render(request, 'fa_asset_merge_checker.html')
# Split
def fa_asset_split(request):
    return render(request, 'fa_asset_split.html')
def fa_asset_split_plus(request):
    return render(request, 'fa_asset_split_plus.html')
def fa_asset_split_checker(request):
    return render(request, 'fa_asset_split_checker.html')
# catgry
def fa_asset_catgry(request):
    return render(request, 'fa_asset_catgry.html')
def fa_asset_catgry_plus(request):
    return render(request, 'fa_asset_catgry_plus.html')
def fa_asset_catgrychecker(request):
    return render(request, 'fa_asset_catgrychecker.html')
#catgry_master
def fa_asset_catgry_master_plus(request):
    return render(request, 'fa_asset_catgry_master_plus.html')
def fa_asset_catgry_summary(request):
    return render(request, 'fa_asset_catgry_master.html')

#fa_asset_salevaluemaker_details
def fa_asset_sale(request):
    return render(request, 'fa_asset_sale.html')
def fa_asset_saleplus(request):
    return render(request, 'fa_asset_saleplus.html')
def fa_asset_sale_checker(request):
    return render(request, 'fa_asset_sale_checker.html')
# reduction
def fa_value_reduction(request):
    return render(request, 'fa_value_reduction.html')
def fa_value_reduction_plus(request):
    return render(request, 'fa_value_reduction_plus.html')
def fa_reduction_checker(request):
    return render(request, 'fa_value_reduction_checker.html')
# transfer
def fa_transfer_maker(request):
    return render(request, 'fa_transfer_maker.html')
def fa_transferplus(request):
    return render(request, 'fa_transferplus.html')
def fa_transfer_checker(request):
    return render(request, 'fa_transfer_checker.html')
#deprisation_calc
def fa_depreciation_calc(request):
    return render(request, 'fa_depreciation_calc.html')

#fa_financial_year
def fa_financial_year(request):
    return render(request, 'fa_financial_year.html')
def fa_financial_year_plus(request):
    return render(request, 'fa_financial_year_plus.html')
def fa_financial_year_checker(request):
    return render(request, 'fa_financial_year_checker.html')

# physical Verification
def fa_physic_verify(request):
    return render(request, 'fa_physic_verify.html')
def fa_physic_verify_plus(request):
    return render(request, 'fa_physic_verify_plus.html')
def fa_physic_verify_check(request):
    return render(request, 'fa_physic_verify_check.html')

def asset_details(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FAApi()
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        params = {"Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_Summary", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def drop_data(request):
    if request.method == 'POST':
        drop_l ={
                "Table_name":"fa_mst_tassetcat",
                "Column_1":"assetcat_gid,assetcat_subcatname",
                "Column_2":"",
                "Where_Common":"assetcat",
                "Where_Primary":"",
                "Primary_Value":"",
                "Order_by":"subcatname"
               }
        drop_table ={"data":drop_l}
        obj = view_sales.SalesOrder_Register()
        obj.actn ='FACAT'
        obj.entity_gid =1
        params = {'Action':obj.actn, 'Entity_Gid': obj.entity_gid}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(drop_table.get('data'))
        resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def get_branch(request):
    if request.method == 'POST':
        drop_m = {
            "Table_name": "gal_mst_tbranch",
            "Column_1": "branch_gid,branch_name",
            "Column_2": "",
            "Where_Common": "branch",
            "Where_Primary": "",
            "Primary_Value": "",
            "Order_by": "name"
        }
        drop_table ={"data":drop_m}
        obj = view_master.All_Tables_Values_Get()
        obj.actn = 'FABRANCH'
        obj.entity_gid = 1
        params = {'Action':obj.actn, 'Entity_Gid': obj.entity_gid}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(drop_table.get('data'))
        resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def imageconvert(request):
    if request.method == 'POST' and request.FILES['file']:
            f = request.FILES['file']
            name = request.POST['name']
            data = base64.b64encode(f.read())
            print(data)
            base = name ,"+",data
            return HttpResponse(base)

def save_asset(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Asset_Make()
        obj.act = jsondata.get('params').get('Action')
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        obj.entity = jsondata.get('params').get('Employee_Gid')
        params = { "Action":obj.act, "Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub,"Employee_Gid" :obj.entity }
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_MAKER", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

#     location details
def branch_details(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Location()
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        params = {"Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_LOCATION", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def save_location(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Location()
        obj.act = jsondata.get('params').get('Action')
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        obj.entity = jsondata.get('params').get('Employee_Gid')
        params = {"Action": obj.act, "Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub,"Employee_Gid" :obj.entity}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_LOCATION", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def writeoff_summary(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Asset_Make()
        obj.act = jsondata.get('params').get('Action')
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        obj.entity = jsondata.get('params').get('Employee_Gid')
        params = { "Action":obj.act, "Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub,"Employee_Gid" :obj.entity }
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_TRAN", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def cat_change(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Tran()
        obj.grp = jsondata.get('Group')
        obj.typ = jsondata.get('Type')
        obj.sub = jsondata.get('Sub_Type')
        obj.act = jsondata.get('Action')
        obj.emp_gid = jsondata.get('Employee_Gid')
        params = {"Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub, "Action": obj.act, "Employee_Gid": obj.emp_gid}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('json'))
        resp = requests.post("" + ip + "/FA_TRAN", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def cp_datechange(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Tran()
        obj.grp = jsondata.get('Group')
        obj.typ = jsondata.get('Type')
        obj.sub = jsondata.get('Sub_Type')
        obj.act = jsondata.get('Action')
        obj.emp_gid = jsondata.get('Employee_Gid')
        params = {"Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub, "Action": obj.act, "Employee_Gid": obj.emp_gid}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('json'))
        resp = requests.post("" + ip + "/FA_TRAN", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def asset_checker(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Asset_Make()
        obj.act = jsondata.get('params').get('Action')
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        obj.entity = jsondata.get('params').get('Employee_Gid')
        params = { "Action":obj.act, "Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub,"Employee_Gid" :obj.entity }
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_MAKER", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

 #_asset_category
def fa_category(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Category()
        obj.grp = jsondata.get('Group')
        obj.typ = jsondata.get('Type')
        obj.sub = jsondata.get('Sub_Type')
        obj.act = jsondata.get('Action')
        obj.emp_gid = jsondata.get('Employee_Gid')
        params = {"Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub, "Action": obj.act,
                  "Employee_Gid": obj.emp_gid}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('json'))
        resp = requests.post("" + ip + "/FA_CATEGORY", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def fa_category_get(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Category()
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        params = {"Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_CATEGORY", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def drop_branch(request):
    if request.method == 'POST':
        drop_b = {
            "Table_name": "ap_mst_tcategory",
            "Column_1": "category_gid,category_name",
            "Column_2": "",
            "Where_Common": "category",
            "Where_Primary": "",
            "Primary_Value": "",
            "Order_by": "name"
        }
    drop_tables={"data":drop_b}
    obj= view_sales.SalesOrder_Register()
    obj.action = 'Debit'
    obj.entity_gid = 1
    params = {'Action': obj.action, 'Entity_Gid': obj.entity_gid}
    headers = {"content-type": "application/json", "Authorization": "" + token + ""}
    datas = json.dumps(drop_tables.get('data'))
    resp = requests.post("" + ip + "/All_Tables_Values_Get", params=params, data=datas, headers=headers,
                             verify=False)
    response = resp.content.decode("utf-8")
    return HttpResponse(response)

def sale_make(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Asset_Make()
        obj.act = jsondata.get('params').get('Action')
        obj.grp = jsondata.get('params').get('Group')
        obj.channel = jsondata.get('params').get('Channel')
        obj.so_header_date = jsondata.get('params').get('So_Header_date')
        obj.entity = jsondata.get('params').get('Employee_Gid')
        params = {"Action": obj.act, "Group": obj.grp,"Employee_Gid": obj.entity,"Channel": obj.channel,"So_Header_date":obj.so_header_date}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_SALE", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def dep_calculation(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FA_Asset_Make()
        obj.act = jsondata.get('params').get('Action')
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        obj.entity = jsondata.get('params').get('Employee_Gid')
        params = {"Action": obj.act, "Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub, "Employee_Gid": obj.entity}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FA_DEPRECIATION", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)

def fin_year(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = view_fa.FinYear()
        obj.act = jsondata.get('params').get('Action')
        obj.grp = jsondata.get('params').get('Group')
        obj.typ = jsondata.get('params').get('Type')
        obj.sub = jsondata.get('params').get('Sub_Type')
        obj.entity = jsondata.get('params').get('Employee_Gid')
        params = {"Action": obj.act, "Group": obj.grp, "Type": obj.typ, "Sub_Type": obj.sub,"Employee_Gid" :obj.entity}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('params').get('json'))
        resp = requests.post("" + ip + "/FIN_YEAR", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


