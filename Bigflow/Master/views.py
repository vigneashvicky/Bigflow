from django.shortcuts import render
from Bigflow.Master.Model import mMasters
from Bigflow.Transaction.Model import mFET
from django.http import JsonResponse
import Bigflow.Core.models as common
from rest_framework.views import APIView
from pandas import ExcelWriter
import pandas as pd
import json
import datetime
from django.http import HttpResponse
#from Bigflow.menuClass import utility as utl

import Bigflow.Core.models as common
# mail
import requests
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives
from Bigflow.settings import BASE_DIR

ip = common.localip()
token = common.token()


def employeeIndex(request):
    return render(request, "employee/bigflow_mst_employee.html")


def Ccbs_Maker_fun(request):
    return render(request, "CCBS/Ccbs_Maker.html")


def Ccbs_Approver_fun(request):
    return render(request, "CCBS/Ccbs_Approver.html")


def Ccbs_Maker_Popup_fun(request):
    return render(request, "CCBS/Ccbs_Maker_Popup.html")


def Cat_Subcat_fun(request):
    return render(request, "CCBS/Cat_Subcat_Summary.html")


def Cat_Subcat_Popup(request):
    return render(request, "CCBS/Cat_Subcat_Add_Summary.html")


def Cc_Bb_Summary(request):
    return render(request, "CCBS/Cc_Bb_Summary.html")


def Cc_Bb_Popup(request):
    return render(request, "CCBS/Cc_Bs_Add_Summary.html")


def employeesummaryIndex(request):
    # utl.check_authorization(request)(request)
    return render(request, "employee/bigflow_mst_employee_summary.html")


def employeeadrsIndex(request):
    return render(request, "employee/bigflow_mst_employee_adrs.html")


def employeecntctIndex(request):
    return render(request, "employee/bigflow_mst_employee_cntct.html")


def employeeviewIndex(request):
    return render(request, "employee/bigflow_mst_employee_view.html")


def empattendanceIndex(request):
    return render(request, "employee/emp_attendance.html")


def emprouteIndex(request):
   # utl.check_authorization(request)(request)
    return render(request, "employee/emp_Route.html")


def emproutedaymapping(request):
   # utl.check_authorization(request)(request)
    return render(request, "employee/emp_routedaymapping.html")


def courier_index(request):
    return render(request, "employee/bigflow_mst_courier.html")


def executivemapping_index(request):
    # utl.check_authorization(request)(request)
    return render(request, "employee/bigflow_mst_executivemapping.html")


def city(request):
  #  utl.check_authorization(request)(request)
    return render(request, "City/bigflow_mst_city.html")


# Supplier create
def supplierIndex(request):
    return render(request, "Supplier/Supplier_Create.html")


def supplierSumryIndex(request):
    return render(request, "Supplier/Supplier_Smry.html")

def Product_Add_Popup(request):
    return render(request,"Product/Product_Add_popup.html")

def Product_Add_Popupcarton(request):
    return render(request, "Product/Product_Add_Popupcarton.html")

def Product_Type_Popup(request):
    return render(request,"Product/Product_Type_popup.html")




def Supplier_Master(request):
    jsondata = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        if (jsondata.get('Group')) == 'Supplier_Get':
            group = jsondata.get('Group')
            type = jsondata.get('Type')
            subtype = jsondata.get('SubType')
            params = {'Group': "" + group + "", 'Type': "" + type + "",
                      'SubType': "" + subtype + ""}
            datas = json.dumps(jsondata.get('data'))
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/Supplier_Mast", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'Supplier_Set' and (jsondata.get('Action')) == 'SUPP_INSERT':
            group = jsondata.get('Group')
            action = jsondata.get('Action')
            params = {'Group': "" + group + "", 'Action': "" + action + ""}
            datas = json.dumps(jsondata.get('key'))
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/Supplier_Mast", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'Supplier_Set' and (jsondata.get('Action')) == 'SUPP_UPDATE':
            group = jsondata.get('Group')
            action = jsondata.get('Action')
            params = {'Group': "" + group + "", 'Action': "" + action + ""}
            datas = json.dumps(jsondata.get('value'))
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/Supplier_Mast", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'Supplier_Set' and (jsondata.get('Action')) == 'SUPPLIER_GROUP_INSERT':
            group = jsondata.get('Group')
            action = jsondata.get('Action')
            params = {'Group': "" + group + "", 'Action': "" + action + ""}
            datas = json.dumps(jsondata.get('value'))
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/Supplier_Mast", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
        elif (jsondata.get('Group')) == 'Supplier_Set' and (jsondata.get('Action')) == 'SUPPLIER_GROUP_UPDATE':
            group = jsondata.get('Group')
            action = jsondata.get('Action')
            params = {'Group': "" + group + "", 'Action': "" + action + ""}
            datas = json.dumps(jsondata.get('value'))
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/Supplier_Mast", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)     

        elif (jsondata.get('Group')) == 'Active_INactive_supplier':
            group = jsondata.get('Group')
            action = jsondata.get('Action')
            params = {'Group': "" + group + "", 'Action': "" + action + ""}
            datas = json.dumps(jsondata.get('data'))
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            resp = requests.post("" + ip + "/Supplier_Mast", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def Supplierproduct_index(request):
    # utl.check_authorization(request)(request)
    return render(request, "Supplier/Supplier_Rate.html")





def productorservice(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'GET_ALL_PRODUCT':

            grp = jsondata.get('Group')
            typ = jsondata.get('Type')
            sbtyp = jsondata.get('Sub_Type')
            params = {'Group': "" + grp + "", 'Type': "" + typ + "", 'Sub_Type': "" + sbtyp + ""}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            datas = json.dumps(jsondata.get('data'))
            resp = requests.post("" + ip + "/All_product_get", params=params, data=datas, headers=headers, verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)
# All_product_get

def All_product_get(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        params = {'Group': 'GET_ALL_PRODUCT', 'Type': 'PRODUCT', 'Sub_Type': 'ALL'}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata)
        resp = requests.post("" + ip + "/All_product_get", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def ccbs_master(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        group = jsondata.get('Group')
        type = jsondata.get('Type')
        sub_type = jsondata.get('Sub_type')
        params = {'Group': "" + group + "", 'Type': "" + type + "", 'Sub_type': "" + sub_type + ""}
        datas = json.dumps(jsondata.get('data'))
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('data'))
        resp = requests.post("" + ip + "/ccbsapi", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def main_category_master(request):
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        dict_dept = obj_master.get_main_category()
        print(len(dict_dept))
        i = 0;
        res = [];
        while i < len(dict_dept):
            res.append(dict_dept[i].to_json(orient='records'))
            i = i + 1;
        print(res);
        return HttpResponse(json.dumps(res));


def cat_subcat_master(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        group = jsondata.get('Group')
        type = jsondata.get('Type')
        sub_type = jsondata.get('Sub_type')
        params = {'Group': "" + group + "", 'Type': "" + type + "", 'Sub_type': "" + sub_type + ""}
        datas = json.dumps(jsondata.get('data'))
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        datas = json.dumps(jsondata.get('data'))
        resp = requests.post("" + ip + "/ccbsapi", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def get_exemapping(request):
    if request.method == 'GET':
        objexe = mMasters.Masters()
        objexe.employee_gid = 0
        objexe.action = ''
        objexe.entity_gid = request.session['Entity_gid']
        df_executive = objexe.getexecmapping()
        jdata = df_executive.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


# //suppliercode
def suppcode(request):
    if request.method == 'POST':
        obj = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj.array = jsondata.get('Action')
        obj_cancel_data = obj.suppliercode()
        jdata = obj_cancel_data[0]
        return JsonResponse(jdata, safe=False)


def department(request):
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        obj_master.table_name = request.GET['table_name']
        obj_master.gid = request.GET['gid']
        obj_master.entity_gid = request.session['Entity_gid']
        dict_dept = obj_master.get_Masters()
        return JsonResponse(json.dumps(dict_dept), safe=False)


def employee_get(request):
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        obj_master.employee_gid = request.GET['emp_gid']
        obj_master.employee_name = request.GET['emp_name']
        obj_master.cluster_gid = request.GET['li_cluster_gid']
        obj_master.cluster = request.GET['cluster']
        obj_master.jsonData = json.dumps({"entity_gid": [request.session['Entity_gid']], "client_gid": []})
        df_view = obj_master.get_employee()
        jdata = df_view.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def employee_getexcel(request):
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        obj_master.employee_gid = 0
        obj_master.employee_name = ''
        obj_master.cluster_gid = 0
        obj_master.cluster = 'ALL'
        obj_master.jsonData = json.dumps({"entity_gid": [request.session['Entity_gid']], "client_gid": []})
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        response['Content-Disposition'] = 'attachment; filename="PythonExport.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view = obj_master.get_employee()
        df_view.to_excel(writer, 'Sheet1')
        writer.save()
        return response


def execmapping_excel(request):
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        obj_master.employee_gid = 0
        obj_master.employee_name = ''
        obj_master.cluster_gid = 0
        obj_master.cluster = 'ALL'
        obj_master.entity_gid = request.session['Entity_gid']
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        response['Content-Disposition'] = 'attachment; filename="execmapping.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view = obj_master.getexecmapping()
        df_view.to_excel(writer, 'Sheet1')
        writer.save()
        return response


def departmentIndex(request):
    return render(request, "employee/bigflow_mst_department.html")


def deptjson(request):
    form = mMasters.Masters
    form.entity_gid = request.session['Entity_gid']
    jdata = form.get_department(request)
    if request.method == 'GET':
        return JsonResponse(json.dumps(jdata), safe=False)


def departjson(request):
    if request.method == 'POST':
        obj_setdept = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_setdept.action = jsondata.get('parms').get('action')
        obj_setdept.department_gid = jsondata.get('parms').get('li_dept_gid')
        obj_setdept.department_code = jsondata.get('parms').get('ls_dept_code')
        obj_setdept.department_name = jsondata.get('parms').get('ls_dept_name')
        obj_setdept.entity_gid = request.session['Entity_gid']
        obj_setdept.Employee_gid = request.session['Emp_gid']
        out_message = outputReturn(obj_setdept.set_department(), 0)
        return JsonResponse(out_message, safe=False)


def depteditjson(request):
    print(request.method)
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        print(jsondata)
        f1 = jsondata.get('parms').get('dept_gid')
        result = mMasters.Masters.get_departedit(f1)
        if (result != ''):
            print(result)
            output = result
            return JsonResponse(json.dumps(output), safe=False)


def deptdeletejson(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        print(jsondata)
        f1 = jsondata.get('parms').get('dept_gid')
        result = mMasters.Masters.get_departdelete(f1)
        if (result != ''):
            print(result)
            output = result
            return JsonResponse(json.dumps(output), safe=False)


def deptactivejson(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        print(jsondata)
        f1 = jsondata.get('parms').get('dept_gid')
        result = mMasters.Masters.get_departactive(f1)
        if (result != ''):
            print(result)
            output = result
            return JsonResponse(json.dumps(output), safe=False)


def deptinactivejson(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        print(jsondata)
        f1 = jsondata.get('parms').get('dept_gid')
        result = mMasters.Masters.get_departinactive(f1)
        if (result != ''):
            print(result)
            output = result
            return JsonResponse(json.dumps(output), safe=False)


def courier_summary_get(request):
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        # obj_master.employee_gid = request.GET['emp_gid']
        obj_master.entity_gid = request.session['Entity_gid']
        df_view = obj_master.get_courier_summary()
        jdata = df_view.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def cluster_get(request):
    if request.method == 'GET':
        obj_masCluster = mMasters.Masters()
        obj_masCluster.action = request.GET['action']
        obj_masCluster.cluster_parent_gid = request.GET['parent_gid']
        obj_masCluster.hierarchy_gid = request.GET['hierarchy_gid']
        obj_masCluster.jsondata = json.dumps({"entity_gid": [request.session['Entity_gid']], "client_gid": []})
        dict_clust = obj_masCluster.get_cluster()
        jdata = dict_clust.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def get_custgroup(request):
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        obj_master.table_name = 'customergroup'
        obj_master.entity_gid = request.session['Entity_gid']
        dict_custgrp = obj_master.get_Masters()
        return JsonResponse(json.dumps(dict_custgrp), safe=False)


def get_contctgroup(request):
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        obj_master.table_name = 'contacttype'
        obj_master.entity_gid = request.session['Entity_gid']
        dict_custgrp = obj_master.get_Masters()
        return JsonResponse(json.dumps(dict_custgrp), safe=False)


def get_employeeddl(request):
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        obj_master.table_name = 'employee'
        obj_master.entity_gid = request.session['Entity_gid']
        dict_custgrp = obj_master.get_Masters()
        return JsonResponse(json.dumps(dict_custgrp), safe=False)


def Customer_Index(request):
    # utl.check_authorization(request)(request)
    return render(request, "Customer/bigflow_mst_customer.html")


def customergrp_get(request):
    if request.method == 'GET':
        custgrp = mMasters.Masters()
        custgrp.custgrp_gid = request.GET['custgrp_gid']
        custgrp.entity_gid = request.session['Entity_gid']
        cust = custgrp.get_custgrp()
        jdata = cust.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def emp_customer_map_set(request):
    if request.method == 'POST':
        obj_emp_cust_map = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_emp_cust_map.Employee_gid = jsondata.get('parms').get('emp_gid')
        insertjson = jsondata.get('parms').get('emp_gid')
        out_message = obj_emp_cust_map


def customer_get(request):
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        obj_master.jsonData = request.GET['jsonData']
        obj_master.entity_gid = request.session['Entity_gid']
        customer = obj_master.get_customer()
        jdata = customer.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def customer_getexcel(request):
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        obj_master.jsonData = '{}'
        obj_master.entity_gid = request.session['Entity_gid']
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        response['Content-Disposition'] = 'attachment; filename="PythonExpor.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view = obj_master.get_customer()
        df_view.to_excel(writer, 'Sheet1')
        writer.save()
        return response


def custpin_excel(request):
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        customer = obj_master.get_pincust()
        jdata = customer.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def customeredt_get(request):
    if request.method == 'GET':
        custedt = mMasters.Masters()
        custedt.customer_gid = request.GET['cust_gid']
        custedt.entity_gid = request.session['Entity_gid']
        customer = custedt.get_customer()
        jdata = customer.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def customercreateIndex(request):
    return render(request, "Customer/bigflow_mst_customercreate.html")


def locationddl(request):
    if request.method == 'GET':
        dict_loct = mMasters.Masters()
        dict_loct.entity_gid = request.session['Entity_gid']
        locti = dict_loct.get_Location()
        jdata = locti.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def stateddl(request):
    if request.method == 'GET':
        statdddl = mMasters.Masters()
        statdddl.table_name = 'state'
        statdddl.entity_gid = request.session['Entity_gid']
        statdddl.gid = 0
        state = statdddl.get_ddl()
        jdata = state.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def empddl(request):
    if request.method == 'GET':
        employee = mMasters.Masters()
        employee.table_name = 'employee'
        employee.entity_gid = request.session['Entity_gid']
        employee.gid = 0
        employname = employee.get_ddl()
        jdata = employname.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def districtddl(request):
    if request.method == 'GET':
        distddl = mMasters.Masters()
        distddl.state_gid = request.GET['state_gid']
        distddl.entity_gid = request.session['Entity_gid']
        district = distddl.get_district()
        jdata = district.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def allpinget(request):
    if request.method == 'GET':
        obj_pin = mMasters.Masters()
        obj_pin.pincode_no = request.GET['pincode']
        obj_pin.entity_gid = request.session['Entity_gid']
        district = obj_pin.get_pincode()
        jdata = district.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def cityddl(request):
    if request.method == 'GET':
        ctyddl = mMasters.Masters()
        ctyddl.district_gid = request.GET['district_gid']
        ctyddl.entity_gid = request.session['Entity_gid']
        city = ctyddl.get_city()
        jdata = city.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def pincode(request):
    if request.method == 'GET':
        pincd = mMasters.Masters()
        pincd.city_gid = request.GET['city_gid']
        pincd.entity_gid = request.session['Entity_gid']
        pincode = pincd.get_pincode()
        jdata = pincode.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def customerset(request):
    if request.method == 'POST':
        custset = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        custset.action = jsondata.get('parms').get('Action')
        custset.create_by = request.session['Emp_gid']
        custset.entity_gid = request.session['Entity_gid']
        if custset.action == 'Insert':
            loct_gid = jsondata.get('parms').get('details').get('Location')
            if (loct_gid == None):
                custset.pincode_gid = jsondata.get('parms').get('details').get('pincodegid')
                custset.location_name = jsondata.get('parms').get('details').get('loccity')
                custset.cluster_gid = jsondata.get('parms').get('details').get('cluster')
                custset.location_code = '500'
                loc_gid = outputReturn(custset.set_Location(), 0)
            else:
                loc_gid = jsondata.get('parms').get('details').get('Location')
            if (loc_gid > 0):
                custset.location_gid = loc_gid
                custset.add_refcode = 'CUST'
                custset.address1 = jsondata.get('parms').get('details').get('Address1')
                custset.address2 = jsondata.get('parms').get('details').get('Address2')
                custset.address3 = jsondata.get('parms').get('details').get('Address3')
                custset.pincode_no = jsondata.get('parms').get('details').get('pincode')
                custset.state_gid = jsondata.get('parms').get('details').get('state')
                custset.district_gid = jsondata.get('parms').get('details').get('district')
                custset.city_gid = jsondata.get('parms').get('details').get('city')
                address_gid = outputReturn(custset.set_address(), 0)
                if (address_gid > 0):
                    custset.address_gid = address_gid
                    custset.custgrp_gid = jsondata.get('parms').get('details').get('custgrp_gid')
                    custset.customer_name = jsondata.get('parms').get('details').get('cust_name')
                    custset.customer_code = jsondata.get('parms').get('details').get('cust_code')
                    custset.cust_type = jsondata.get('parms').get('details').get('cust_type')
                    custset.custcate_gid = jsondata.get('parms').get('details').get('custcate_gid')
                    custset.constitution_gid = jsondata.get('parms').get('details').get('custconstitut_gid')
                    custset.salemode_gid = jsondata.get('parms').get('details').get('custsalemode_gid')
                    custset.size_gid = jsondata.get('parms').get('details').get('custsize_gid')
                    custset.landmark = jsondata.get('parms').get('details').get('LNDMRK')
                    custset.cust_billingname = jsondata.get('parms').get('details').get('BILLINGANME')
                    custset.cust_subtype = jsondata.get('parms').get('details').get('cust_subtype')
                    result = outputReturn(custset.set_customer(), 0)
                    if (result > 0):
                        custset.contact_gid = result
                        custset.cont_refcode = 'CUST'
                        custset.cont_refgid = result
                        custset.contacttype_gid = jsondata.get('parms').get('details').get('ContactType')
                        custset.conper1 = jsondata.get('parms').get('details').get('Personname')
                        custset.designation_gid = jsondata.get('parms').get('details').get('Designation')
                        custset.landline_no = jsondata.get('parms').get('details').get('Landline1')
                        custset.landline_no1 = jsondata.get('parms').get('details').get('Landline2')
                        custset.mobile_no = jsondata.get('parms').get('details').get('Mobilenum')
                        custset.mobile_no1 = jsondata.get('parms').get('details').get('Mobilenum2')
                        custset.email = jsondata.get('parms').get('details').get('Emailid')
                        if (jsondata.get('parms').get('details').get('BirthDate') != ''):
                            custset.cont_dob = common.convertDate(
                                jsondata.get('parms').get('details').get('BirthDate'))
                        else:
                            custset.cont_dob = ''
                        if (jsondata.get('parms').get('details').get('Wedingday') != ''):
                            custset.wedding_day = common.convertDate(
                                jsondata.get('parms').get('details').get('Wedingday'))
                        else:
                            custset.wedding_day = ''
                        resultc = outputReturn(custset.set_contact(), 0)
                        gstno = jsondata.get('parms').get('details').get('GSTNO')
                        if (gstno == '' or gstno == None):
                            courier = jsondata.get('parms').get('details').get('COURIER')
                            if (courier == '' or courier == None):
                                return JsonResponse(result, safe=False)
                            else:
                                custset.jsondata = '{}'
                                custset.cust_courier_gid = jsondata.get('parms').get('details').get('cust_courier_gid')
                                custset.customer_gid = result
                                custset.courier_gid = jsondata.get('parms').get('details').get('COURIER')
                                custset.remark = ''
                                custset.from_date = jsondata.get('parms').get('details').get('COURIER_fromdate')
                                custset.to_date = jsondata.get('parms').get('details').get('COURIER_todate')
                                resultcou = outputReturn(custset.set_courierdetails(), 0)
                                if (resultcou > 0):
                                    return JsonResponse(resultcou, safe=False)
                                else:
                                    return JsonResponse('Courier Not Inserted', safe=False)
                        else:
                            custset.gstno = gstno
                            custset.tax_code = 'GST'
                            custset.subtax_name = 'CGST'
                            custset.ref_name = 'CUST_GST'
                            custset.tax_type = 'C'
                            custset.reftbl_code = jsondata.get('parms').get('details').get('cust_code')
                            result1 = outputReturn(custset.set_taxdetails(), 0)
                            if (result1 > 0):
                                courier = jsondata.get('parms').get('details').get('COURIER')
                                if (courier == '' or courier == None):
                                    return JsonResponse(result1, safe=False)
                                else:
                                    custset.jsondata = '{}'
                                    custset.cust_courier_gid = jsondata.get('parms').get('details').get(
                                        'cust_courier_gid')
                                    custset.customer_gid = result
                                    custset.courier_gid = jsondata.get('parms').get('details').get('COURIER')
                                    custset.remark = ''
                                    custset.from_date = jsondata.get('parms').get('details').get('COURIER_fromdate')
                                    custset.to_date = jsondata.get('parms').get('details').get('COURIER_todate')
                                    resultcou = outputReturn(custset.set_courierdetails(), 0)
                                    if (resultcou > 0):
                                        return JsonResponse(resultcou, safe=False)
                                    else:
                                        return JsonResponse('Courier Not Inserted', safe=False)
                            else:
                                return JsonResponse('GST Not Inserted', safe=False)


                    else:
                        return JsonResponse('Customer Not Inserted', safe=False)
                else:
                    return JsonResponse('Address Not Inserted', safe=False)
            else:
                return JsonResponse('Location Not Inserted', safe=False)
        else:
            custset.location_gid = jsondata.get('parms').get('details').get('Location')
            custset.pincode_gid = jsondata.get('parms').get('details').get('pincodegid')
            custset.location_name = jsondata.get('parms').get('details').get('loccity')
            custset.cluster_gid = jsondata.get('parms').get('details').get('cluster')
            custset.location_code = '500'
            loc_result = outputReturn(custset.set_Location(), 0)
            if (loc_result == 'SUCCESS'):
                custset.add_refcode = 'CUST'
                custset.address1 = jsondata.get('parms').get('details').get('Address1')
                custset.address2 = jsondata.get('parms').get('details').get('Address2')
                custset.address3 = jsondata.get('parms').get('details').get('Address3')
                custset.pincode_no = jsondata.get('parms').get('details').get('pincode')
                custset.state_gid = jsondata.get('parms').get('details').get('state')
                custset.district_gid = jsondata.get('parms').get('details').get('district')
                custset.city_gid = jsondata.get('parms').get('details').get('city')
                address_gid = jsondata.get('parms').get('details').get('Address_gid')
                if (address_gid > 0):
                    custset.action = 'Update'
                    custset.address_gid = address_gid
                    add_result = outputReturn(custset.set_address(), 0)
                else:
                    custset.action = 'Insert'
                    outmsg = outputReturn(custset.set_address(), 0)
                    if (outmsg > 0):
                        address_gid = outmsg
                        add_result = 'SUCCESS'
                if (add_result == 'SUCCESS'):
                    custset.action = 'Update'
                    custset.custgrp_gid = jsondata.get('parms').get('details').get('custgrp_gid')
                    custset.customer_name = jsondata.get('parms').get('details').get('cust_name')
                    custset.customer_code = jsondata.get('parms').get('details').get('cust_code')
                    custset.cust_type = jsondata.get('parms').get('details').get('cust_type')
                    custset.cust_subtype = jsondata.get('parms').get('details').get('cust_subtype')
                    custset.custcate_gid = jsondata.get('parms').get('details').get('custcate_gid')
                    custset.constitution_gid = jsondata.get('parms').get('details').get('custconstitut_gid')
                    custset.salemode_gid = jsondata.get('parms').get('details').get('custsalemode_gid')
                    custset.size_gid = jsondata.get('parms').get('details').get('custsize_gid')
                    custset.landmark = jsondata.get('parms').get('details').get('LNDMRK')
                    custset.cust_billingname = jsondata.get('parms').get('details').get('BILLINGANME')
                    custset.address_gid = address_gid
                    custset.customer_gid = jsondata.get('parms').get('details').get('cust_gid')
                    result = outputReturn(custset.set_customer(), 0)
                    if (result == 'SUCCESS'):
                        custset.cont_refcode = 'CUST'
                        custset.cont_refgid = jsondata.get('parms').get('details').get('cust_gid')
                        custset.contacttype_gid = jsondata.get('parms').get('details').get('ContactType')
                        custset.conper1 = jsondata.get('parms').get('details').get('Personname')
                        custset.designation_gid = jsondata.get('parms').get('details').get('Designation')
                        custset.landline_no = jsondata.get('parms').get('details').get('Landline1')
                        custset.landline_no1 = jsondata.get('parms').get('details').get('Landline2')
                        custset.mobile_no = jsondata.get('parms').get('details').get('Mobilenum')
                        custset.mobile_no1 = jsondata.get('parms').get('details').get('Mobilenum2')
                        custset.email = jsondata.get('parms').get('details').get('Emailid')
                        if (jsondata.get('parms').get('details').get('BirthDate') != ''):
                            custset.cont_dob = common.convertDate(
                                jsondata.get('parms').get('details').get('BirthDate'))
                        else:
                            custset.cont_dob = ''
                        if (jsondata.get('parms').get('details').get('Wedingday') != ''):
                            custset.wedding_day = common.convertDate(
                                jsondata.get('parms').get('details').get('Wedingday'))
                        else:
                            custset.wedding_day = ''
                        contact_gid = jsondata.get('parms').get('details').get('contact_gid')
                        if (contact_gid != 0 and contact_gid != None):
                            custset.contact_gid = contact_gid
                            custset.action = 'Update'
                            out_message = outputReturn(custset.set_contact(), 0)
                        else:
                            custset.action = 'Insert'
                            outmsg1 = outputReturn(custset.set_contact(), 0)
                            if (outmsg1 > 0):
                                out_message = 'SUCCESS'
                        if (out_message == 'SUCCESS'):
                            GSTno = jsondata.get('parms').get('details').get('GSTNO')
                            GSTgid = jsondata.get('parms').get('details').get('GSTNO_gid')
                            if (GSTno != 0 and GSTno != None and GSTno != '' and out_message != 0):
                                if (GSTgid == 0 or GSTgid == None):
                                    custset.action = 'Insert'
                                    custset.gstno = jsondata.get('parms').get('details').get('GSTNO')
                                    custset.tax_code = 'GST'
                                    custset.subtax_name = 'CGST'
                                    custset.ref_name = 'CUST_GST'
                                    custset.tax_type = 'C'
                                    custset.reftbl_code = jsondata.get('parms').get('details').get('cust_code')
                                    result1 = outputReturn(custset.set_taxdetails(), 0)
                                    if (result1 > 0):
                                        courier = jsondata.get('parms').get('details').get('COURIER')
                                        cust_courier_gid = jsondata.get('parms').get('details').get('cust_courier_gid')
                                        if (cust_courier_gid == 0 or cust_courier_gid == None):
                                            custset.action = 'Insert'
                                            custset.jsondata = '{}'
                                            custset.cust_courier_gid = jsondata.get('parms').get('details').get(
                                                'cust_courier_gid')
                                            custset.customer_gid = result
                                            custset.courier_gid = jsondata.get('parms').get('details').get('COURIER')
                                            custset.remark = ''
                                            custset.from_date = jsondata.get('parms').get('details').get(
                                                'COURIER_fromdate')
                                            custset.to_date = jsondata.get('parms').get('details').get('COURIER_todate')
                                            resultcou = outputReturn(custset.set_courierdetails(), 0)
                                            if (resultcou > 0):
                                                return JsonResponse(resultcou, safe=False)
                                            else:
                                                return JsonResponse('Courier Not Inserted', safe=False)
                                        else:
                                            custset.action = 'Update'
                                            custset.jsondata = '{}'
                                            custset.courier_gid = jsondata.get('parms').get('details').get('COURIER')
                                            result1 = outputReturn(custset.set_courierdetails(), 0)
                                            if (result1 == 'SUCCESS'):
                                                return JsonResponse(result, safe=False)
                                            else:
                                                return JsonResponse('Courier Not Updated', safe=False)

                                    else:
                                        return JsonResponse('GST Not Inserted', safe=False)
                                else:
                                    custset.action = 'Update'
                                    custset.gstno = jsondata.get('parms').get('details').get('GSTNO')
                                    custset.taxdtl_gid = GSTgid
                                    result1 = outputReturn(custset.set_taxdetails(), 0)
                                    if (result1 == 'SUCCESS'):
                                        courier = jsondata.get('parms').get('details').get('COURIER')
                                        cust_courier_gid = jsondata.get('parms').get('details').get('cust_courier_gid')
                                        if (cust_courier_gid == 0 or cust_courier_gid == None):
                                            custset.action = 'Insert'
                                            custset.jsondata = '{}'
                                            #custset.cust_courier_gid = jsondata.get('parms').get('details').get('cust_courier_gid') to custset.cust_courier_gid =0 by sakthivel
                                            custset.cust_courier_gid =0
                                            custset.courier_gid = jsondata.get('parms').get('details').get('COURIER')
                                            custset.remark = ''
                                            custset.from_date = jsondata.get('parms').get('details').get(
                                                'COURIER_fromdate')
                                            custset.to_date = jsondata.get('parms').get('details').get('COURIER_todate')
                                            courier_update=custset.set_courierdetails()
                                            resultcou = outputReturn(courier_update, 0)
                                            resultcou1 = outputReturn(courier_update, 1)
                                            if (resultcou > 0):
                                                return JsonResponse(resultcou1, safe=False)
                                            else:
                                                return JsonResponse('Courier Not Inserted', safe=False)
                                        else:
                                            custset.action = 'Update'
                                            custset.jsondata = '{}'
                                            # courier_gid to cust_courier_gid by sakthivel
                                            custset.cust_courier_gid = jsondata.get('parms').get('details').get(
                                                'cust_courier_gid')
                                            custset.courier_gid= jsondata.get('parms').get('details').get('COURIER')
                                            result1 = outputReturn(custset.set_courierdetails(), 0)
                                            if (result1 == 'SUCCESS'):
                                                return JsonResponse(result, safe=False)
                                            else:
                                                return JsonResponse('Courier Not Updated', safe=False)
                                    else:
                                        return JsonResponse('GST Not Updated', safe=False)
                            else:
                                courier = jsondata.get('parms').get('details').get('COURIER')
                                cust_courier_gid = jsondata.get('parms').get('details').get('cust_courier_gid')
                                if (cust_courier_gid == 0 or cust_courier_gid == None):
                                    custset.action = 'Insert'
                                    custset.jsondata = '{}'
                                    custset.courier_gid = jsondata.get('parms').get('details').get('COURIER')
                                    custset.cust_courier_gid = jsondata.get('parms').get('details').get(
                                        'cust_courier_gid')
                                    custset.customer_gid = result
                                    custset.remark = ''
                                    custset.from_date = jsondata.get('parms').get('details').get('COURIER_fromdate')
                                    custset.to_date = jsondata.get('parms').get('details').get('COURIER_todate')
                                    resultcou = outputReturn(custset.set_courierdetails(), 0)
                                    if (resultcou > 0):
                                        return JsonResponse(resultcou, safe=False)
                                    else:
                                        return JsonResponse('Courier Not Inserted', safe=False)
                                else:
                                    custset.action = 'Update'
                                    custset.jsondata = '{}'
                                    custset.courier_gid = jsondata.get('parms').get('details').get('COURIER')
                                    custset.cust_courier_gid = jsondata.get('parms').get('details').get(
                                        'cust_courier_gid')
                                    result1 = outputReturn(custset.set_courierdetails(), 0)
                                    if (result1 == 'SUCCESS'):
                                        return JsonResponse(result, safe=False)
                                    else:
                                        return JsonResponse('Courier Not Updated', safe=False)

                        else:
                            return JsonResponse('Contact Not Updated', safe=False)
                    else:
                        return JsonResponse('Customer Not Updated', safe=False)
                else:
                    return JsonResponse('Address Not Updated', safe=False)
            else:
                return JsonResponse('Location Not Updated', safe=False)


def outputReturn(tubledtl, index):
    temp = tubledtl[0].split(',')
    if (len(temp) > 1):
        if (index == 0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return temp[0]


def locationget(request):
    if request.method == 'GET':
        loct = mMasters.Masters()
        loct.location_gid = request.GET['location_gid']
        loct.entity_gid = request.session['Entity_gid']
        dict_loct = loct.get_Location()
        jdata = dict_loct.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def addressget(request):
    if request.method == 'GET':
        add = mMasters.Masters()
        add.address_gid = request.GET['add_gid']
        add.entity_gid = request.session['Entity_gid']
        dict_add = add.get_address()
        jdata = dict_add.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def customerdel(request):
    if request.method == 'POST':
        cust_del = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        cust_del.customer_gid = jsondata.get('params').get('cust_gid')
        cust_del.action = jsondata.get('params').get('Action')
        del_res = outputReturn(cust_del.set_customer(), 0)
        return JsonResponse(del_res, safe=False)


def getMappedLocation(request):
    if request.method == 'GET':
        obj_mapped_customer = mFET.FET_model()
        obj_mapped_customer.Employee_gid = request.GET['emp_gid']
        obj_mapped_customer.entity_gid = request.session['Entity_gid']
        df_mapped_customer = obj_mapped_customer.get_mapped_customer()
        df_mappedLocation = (df_mapped_customer[['location_gid', 'location_name']]) \
            .groupby(['location_gid', 'location_name']).size().reset_index();
        return JsonResponse(json.loads(df_mappedLocation.to_json(orient='records')), safe=False)


def setRouteDtl(request):
    if request.method == 'POST':
        obj_setroute = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8')).get('parms')
        obj_setroute.action = jsondata.get('action')
        obj_setroute.json_employee_gid = json.dumps(jsondata.get('emp_gid'))
        obj_setroute.routeHead_gid = jsondata.get('routeHead_gid')
        obj_setroute.route_code = jsondata.get('route_code')
        obj_setroute.route_name = jsondata.get('route_name')
        obj_setroute.remark = jsondata.get('remark')
        obj_setroute.jsonData = json.dumps(jsondata.get('location_dtl'))
        obj_setroute.create_by = request.session['Emp_gid']
        obj_setroute.entity_gid = request.session['Entity_gid']
        out_message = outputReturn(obj_setroute.setRouteDtl(), 1)
        return JsonResponse(out_message, safe=False)


def getRouteDtl(request):
    if request.method == 'GET':
        obj_getRouteDtl = mMasters.Masters()
        obj_getRouteDtl.action = request.GET['action']
        obj_getRouteDtl.routeHead_gid = request.GET['routeHead_gid']
        obj_getRouteDtl.route_code = request.GET['route_code']
        obj_getRouteDtl.route_name = request.GET['route_name']
        obj_getRouteDtl.json_employee_gid = request.GET['emp_gid']
        obj_getRouteDtl.entity_gid = request.session['Entity_gid']
        df_getRoute = obj_getRouteDtl.getRouteDtl()
        if request.GET['action'] == 'HEADER_DETAILS':
            df_getRoute = (
                df_getRoute[
                    ['routeheader_gid', 'routeheader_code', 'routeheader_name', 'routeheader_remarks']]).groupby(
                ['routeheader_gid', 'routeheader_code', 'routeheader_name',
                 'routeheader_remarks']).size().reset_index();
        elif request.GET['action'] == 'ROUTE_EMPLOYEE' or request.GET['action'] == 'ROUTE_LOCATION':
            df_getRoute['status'] = df_getRoute['status'].astype(bool)
            if obj_getRouteDtl.routeHead_gid == '0':
                df_getRoute = df_getRoute.drop('status', axis=1)
        return JsonResponse(json.loads(df_getRoute.to_json(orient='records')), safe=False)


def gettownn(request):
    if request.method == 'GET':
        obj_custcate = mMasters.Masters()
        obj_custcate.action = request.GET['action']
        obj_custcate.routeHead_gid = request.GET['routeHead_gid']
        obj_custcate.entity_gid = request.session['Entity_gid']
        dict_custgrp = obj_custcate.getRouteDtl()
        return JsonResponse(json.loads(dict_custgrp.to_json(orient='records')), safe=False)


def getrout(request):
    if request.method == 'GET':
        obj_custcate = mMasters.Masters()
        obj_custcate.action = request.GET['action']
        obj_custcate.json_cluster_gid = request.GET['cluster_gid']
        obj_custcate.entity_gid = request.session['Entity_gid']
        dict_custgrp = obj_custcate.getRouteDtl()
        return JsonResponse(json.loads(dict_custgrp.to_json(orient='records')), safe=False)


def CustomerTerritoryIndex(request):
    #utl.check_authorization(request)(request)
    return render(request, "Customer/customer_territory.html")


def getClusterDtl(request):
    if request.method == 'GET':
        obj_clusterDtl = mMasters.Masters()
        obj_clusterDtl.action = 'ALL'
        obj_clusterDtl.cluster_parent_gid = 0
        obj_clusterDtl.hierarchy_gid = 0
        obj_clusterDtl.jsondata = json.dumps({"entity_gid": [request.session['Entity_gid']], "client_gid": []})
        df_cluster = obj_clusterDtl.get_cluster()
        obj_clusterDtl.action = 'R'
        obj_clusterDtl.entity_gid = request.session['Entity_gid']
        df_hierarchy = obj_clusterDtl.getHierarchy()
        test = []
        for x, hier in df_hierarchy.iterrows():
            re = df_cluster[df_cluster['cluster_hierarchygid'] == hier['hierarchy_gid']]
            test.append(re)
        df_hierarchy['clustlist'] = test
        jdata = df_hierarchy.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def setCluster(request):
    if request.method == 'POST':
        obj_clstrset = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_clstrset.action = jsondata.get('parms').get('action')
        obj_clstrset.cluster_gid = jsondata.get('parms').get('li_clus_gid')
        obj_clstrset.cluster_name = jsondata.get('parms').get('ls_clus_name')
        obj_clstrset.cluster_parent_gid = jsondata.get('parms').get('li_parent_gid')
        obj_clstrset.hierarchy_gid = jsondata.get('parms').get('li_hierarchy_gid')
        obj_clstrset.entity_gid = request.session['Entity_gid']
        obj_clstrset.Employee_gid = request.session['Emp_gid']
        out_message = outputReturn(obj_clstrset.setCluster(), 0)
        return JsonResponse(out_message, safe=False)


def sideNavFilterIndex(request):
    return render(request, "Shared/sideNavFilter.html")


def dept_get(request):
    if request.method == 'GET':
        formm = mMasters.Masters()
        formm.entity_gid = request.session['Entity_gid']
        dict_add = formm.get_department()
        return JsonResponse(json.dumps(dict_add), safe=False)


def desg_get(request):
    if request.method == 'GET':
        formm = mMasters.Masters()
        formm.entity_gid = request.session['Entity_gid']
        dict_add = formm.get_designation()
        return JsonResponse(json.dumps(dict_add), safe=False)


def courier_set(request):
    if request.method == 'POST':
        obj_courier = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_courier.action = jsondata.get('parms').get('action')
        if obj_courier.action == 'Insert':
            obj_courier.courier_code = jsondata.get('parms').get('ls_courier_code')
            obj_courier.courier_name = jsondata.get('parms').get('ls_courier_name')
            out_message = obj_courier.set_courier()


# Product
def productdetails(request):
    return render(request, "Product/Product_details.html")


# def productcreate(request):
#     return render(request, "Product/Product_create.html")

def productadd(request):
    return render(request, "Product/Product_Add.html")


def productIndex(request):
    return render(request, "Product/Product_summary.html")


def productcategoryIndex(request):
    return render(request, "Product/Product_category.html")


def producttypeIndex(request):
    return render(request, "Product/Product_type.html")


def categoryget(request):
    if request.method == 'GET':
        form = mMasters.Masters
        jdata = form.get_category(request)
        return JsonResponse(json.dumps(jdata), safe=False)


def typeget(request):
    if request.method == 'GET':
        types = mMasters.Masters()
        types.prodcat_gid = request.GET['prodcat_gid']
        dict_add = types.getproduct_types()
        jdata = dict_add.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def get_custcate(request):
    if request.method == 'GET':
        obj_custcate = mMasters.Masters()
        obj_custcate.table_name = 'custcategory'
        obj_custcate.entity_gid = request.session['Entity_gid']
        dict_custgrp = obj_custcate.get_Masters()
        return JsonResponse(json.dumps(dict_custgrp), safe=False)


def get_cluster(request):
    if request.method == 'GET':
        obj_locCluster = mMasters.Masters()
        obj_locCluster.action = request.GET['action']
        obj_locCluster.jsondata = json.dumps({"entity_gid": [request.session['Entity_gid']], "client_gid": []})
        dict_locclust = obj_locCluster.get_cluster()
        jdata = dict_locclust.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def get_custdata(request):
    if request.method == 'GET':
        obj_custdata = mMasters.Masters()
        obj_custdata.table_name = request.GET['tablename']
        obj_custdata.column_name = request.GET['columnname']
        obj_custdata.entity_gid = request.session['Entity_gid']
        dict_custdata = obj_custdata.getmetadata()
        jdata = dict_custdata.to_json(orient='records')
        return JsonResponse(jdata, safe=False)

def supplierdetails(request):
    if request.method == 'POST':
        custgrpset = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        custgrpset.action = jsondata.get('params').get('Action')
        custgrpset.create_by = request.session['Emp_gid']
        custgrpset.entity_gid = request.session['Entity_gid']
        if custgrpset.action == 'SUPP_INSERT':
            custgrpset.action = 'SUPP_INSERT'
            custgrpset.custgrp_gid = jsondata.get('params').get('supplier_details').get('custgrp_gid')
            custgrpset.custgrp_name = jsondata.get('params').get('supplier_details').get('custgrp_name')
            resultsupplier = outputReturn(custgrpset.set_customergroup(), 0)
            if (resultsupplier == 'SUCCESS'):
                return JsonResponse(resultsupplier, safe=False)
            else:
                return JsonResponse('Supplier Not Updated', safe=False)


def customergroupset(request):
    if request.method == 'POST':
        custgrpset = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        custgrpset.action = jsondata.get('parms').get('Action')
        custgrpset.create_by = request.session['Emp_gid']
        custgrpset.entity_gid = request.session['Entity_gid']
        if custgrpset.action == 'Insert':
            custgrpset.add_refcode = 'CUSTGROUP'
            custgrpset.address1 = jsondata.get('parms').get('grpdetails').get('Address1')
            custgrpset.address2 = jsondata.get('parms').get('grpdetails').get('Address2')
            custgrpset.address3 = jsondata.get('parms').get('grpdetails').get('Address3')
            custgrpset.pincode_no = jsondata.get('parms').get('grpdetails').get('pincode')
            custgrpset.state_gid = jsondata.get('parms').get('grpdetails').get('state')
            custgrpset.district_gid = jsondata.get('parms').get('grpdetails').get('district')
            custgrpset.city_gid = jsondata.get('parms').get('grpdetails').get('city')
            address_gid = outputReturn(custgrpset.set_address(), 0)
            if (address_gid > 0):
                custgrpset.address_gid = address_gid
                custgrpset.custgrp_name = jsondata.get('parms').get('grpdetails').get('custgrp_name')
                custgrpset.custgrp_code = jsondata.get('parms').get('grpdetails').get('custgrp_code')
                custgrpset.conper1 = jsondata.get('parms').get('grpdetails').get('custgrp_cpname1')
                custgrpset.desig1 = jsondata.get('parms').get('grpdetails').get('custgrp_desig1')
                custgrpset.mobile_no = jsondata.get('parms').get('grpdetails').get('custgrp_mobileno1')
                custgrpset.landline_no = jsondata.get('parms').get('grpdetails').get('custgrp_landline1')
                custgrpset.conper2 = jsondata.get('parms').get('grpdetails').get('custgrp_cpname2')
                custgrpset.desig2 = jsondata.get('parms').get('grpdetails').get('custgrp_desig2')
                custgrpset.mobile_no1 = jsondata.get('parms').get('grpdetails').get('custgrp_mobileno2')
                custgrpset.landline_no1 = jsondata.get('parms').get('grpdetails').get('custgrp_landline2')
                custgrpset.entity_gid =  request.session['Entity_gid']
                custgrpset.client_gid = jsondata.get('parms').get('grpdetails').get('grpclient_gid')
                result = outputReturn(custgrpset.set_customergroup(), 0)
                return JsonResponse(result, safe=False)
            else:
                return JsonResponse('Address Not Inserted', safe=False)
        else:
            address_gid = jsondata.get('parms').get('grpdetails').get('Address_gid')
            if (address_gid > 0):
                custgrpset.action = 'Update'
                custgrpset.address_gid = address_gid
                custgrpset.add_refcode = 'CUSTGROUP'
                custgrpset.address1 = jsondata.get('parms').get('grpdetails').get('Address1')
                custgrpset.address2 = jsondata.get('parms').get('grpdetails').get('Address2')
                custgrpset.address3 = jsondata.get('parms').get('grpdetails').get('Address3')
                custgrpset.pincode_no = jsondata.get('parms').get('grpdetails').get('pincode')
                custgrpset.state_gid = jsondata.get('parms').get('grpdetails').get('state')
                custgrpset.district_gid = jsondata.get('parms').get('grpdetails').get('district')
                custgrpset.city_gid = jsondata.get('parms').get('grpdetails').get('city')
                add_result = outputReturn(custgrpset.set_address(), 0)

                custgrpset.custgrp_name = jsondata.get('parms').get('grpdetails').get('custgrp_name')
                custgrpset.custgrp_code = jsondata.get('parms').get('grpdetails').get('custgrp_code')
                custgrpset.conper1 = jsondata.get('parms').get('grpdetails').get('custgrp_cpname1')
                custgrpset.desig1 = jsondata.get('parms').get('grpdetails').get('custgrp_desig1')
                custgrpset.mobile_no = jsondata.get('parms').get('grpdetails').get('custgrp_mobileno1')
                custgrpset.landline_no = jsondata.get('parms').get('grpdetails').get('custgrp_landline1')
                custgrpset.conper2 = jsondata.get('parms').get('grpdetails').get('custgrp_cpname2')
                custgrpset.desig2 = jsondata.get('parms').get('grpdetails').get('custgrp_desig2')
                custgrpset.mobile_no1 = jsondata.get('parms').get('grpdetails').get('custgrp_mobileno2')
                custgrpset.landline_no1 = jsondata.get('parms').get('grpdetails').get('custgrp_landline2')
                custgrpset.client_gid = jsondata.get('parms').get('grpdetails').get('grpclient_gid')
                custgrpset.custgrp_gid = jsondata.get('parms').get('grpdetails').get('custgrp_gid')
                custgrpset.address_gid = address_gid
                resultaddress = outputReturn(custgrpset.set_customergroup(), 0)
                if (resultaddress == 'SUCCESS'):
                    return JsonResponse(resultaddress, safe=False)
                else:
                    return JsonResponse('Customer Group Not Updated', safe=False)

            else:
                custgrpset.action = 'Insert'
                custgrpset.add_refcode = 'CUSTGROUP'
                custgrpset.address1 = jsondata.get('parms').get('grpdetails').get('Address1')
                custgrpset.address2 = jsondata.get('parms').get('grpdetails').get('Address2')
                custgrpset.address3 = jsondata.get('parms').get('grpdetails').get('Address3')
                custgrpset.pincode_no = jsondata.get('parms').get('grpdetails').get('pincode')
                custgrpset.state_gid = jsondata.get('parms').get('grpdetails').get('state')
                custgrpset.district_gid = jsondata.get('parms').get('grpdetails').get('district')
                custgrpset.city_gid = jsondata.get('parms').get('grpdetails').get('city')
                addr = custgrpset.set_address()
                add_result = outputReturn(addr, 1)
                add_gid = outputReturn(addr, 0)
            if (add_result == 'SUCCESS'):
                custgrpset.action = 'update'
                custgrpset.custgrp_name = jsondata.get('parms').get('grpdetails').get('custgrp_name')
                custgrpset.custgrp_code = jsondata.get('parms').get('grpdetails').get('custgrp_code')
                custgrpset.conper1 = jsondata.get('parms').get('grpdetails').get('custgrp_cpname1')
                custgrpset.desig1 = jsondata.get('parms').get('grpdetails').get('custgrp_desig1')
                custgrpset.mobile_no = jsondata.get('parms').get('grpdetails').get('custgrp_mobileno1')
                custgrpset.landline_no = jsondata.get('parms').get('grpdetails').get('custgrp_landline1')
                custgrpset.conper2 = jsondata.get('parms').get('grpdetails').get('custgrp_cpname2')
                custgrpset.desig2 = jsondata.get('parms').get('grpdetails').get('custgrp_desig2')
                custgrpset.mobile_no1 = jsondata.get('parms').get('grpdetails').get('custgrp_mobileno2')
                custgrpset.landline_no1 = jsondata.get('parms').get('grpdetails').get('custgrp_landline2')
                custgrpset.client_gid = jsondata.get('parms').get('grpdetails').get('grpclient_gid')
                custgrpset.custgrp_gid = jsondata.get('parms').get('grpdetails').get('custgrp_gid')
                custgrpset.address_gid = add_gid
                result = outputReturn(custgrpset.set_customergroup(), 0)
                if (result == 'SUCCESS'):
                    return JsonResponse(result, safe=False)
                else:
                    return JsonResponse('Customer Group Not Updated', safe=False)
            else:
                return JsonResponse('Address Not Updated', safe=False)



def exemapping(request):
    if request.method == 'POST':
        obj_exec = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_exec.action = jsondata.get('parms').get('Action')
        obj_exec.exemapjson = jsondata.get('parms').get('custemp')
        obj_exec.from_date = datetime.datetime.strptime(jsondata.get('parms').get('from_date'), "%d/%m/%Y").strftime(
            "%Y-%m-%d")
        obj_exec.to_date = datetime.datetime.strptime(jsondata.get('parms').get('to_date'), "%d/%m/%Y").strftime(
            "%Y-%m-%d")
        obj_exec.employee_gid = request.session['Emp_gid']
        obj_exec.entity_gid = request.session['Entity_gid'];
        result = outputReturn(obj_exec.set_exemapping(), 1)
    return JsonResponse(result, safe=False);


def employeeset(request):
    if request.method == 'POST':

        addrss = 0
        employ = 0
        obj_sales = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        # getempdetail = jsondata.get('parms').get('empdetail')
        obj_sales.action = jsondata.get('parms').get('Action')
        obj_sales.create_by = request.session['Emp_gid']
        obj_sales.entity_gid = request.session['Entity_gid']
        if obj_sales.action != '':
            obj_sales.add_refcode = 'EMP'
            obj_sales.address1 = jsondata.get('parms').get('empdetail').get('address1')
            obj_sales.address2 = jsondata.get('parms').get('empdetail').get('address2')
            obj_sales.address3 = jsondata.get('parms').get('empdetail').get('address3')
            obj_sales.pincode_no = jsondata.get('parms').get('empdetail').get('pincode')
            obj_sales.state_gid = jsondata.get('parms').get('empdetail').get('state')
            obj_sales.district_gid = jsondata.get('parms').get('empdetail').get('district')
            obj_sales.city_gid = jsondata.get('parms').get('empdetail').get('city')
            obj_sales.address_gid = jsondata.get('parms').get('empdetail').get('Address_gid')
            obj_sales.create_by = request.session['Emp_gid']
            obj_sales.empdetail = jsondata.get('parms').get('data')
            addres = outputReturn(obj_sales.set_address(), 0)
        if (addres > 0):
            obj_sales.employee_gid = 0
            obj_sales.employee_code = jsondata.get('parms').get('empdetail').get('Employeecode')
            obj_sales.employee_name = jsondata.get('parms').get('empdetail').get('Employeename')
            obj_sales.gender = jsondata.get('parms').get('empdetail').get('Employeegndr')
            obj_sales.emp_dob = jsondata.get('parms').get('empdetail').get('Employeedob')
            obj_sales.emp_doj = jsondata.get('parms').get('empdetail').get('Employeedoj')
            obj_sales.department_gid = jsondata.get('parms').get('empdetail').get('Employeedept')
            obj_sales.designation_gid = jsondata.get('parms').get('empdetail').get('Employeedesgn')
            obj_sales.emp_sup_name = jsondata.get('parms').get('empdetail').get('Employeesprvsr')
            obj_sales.emp_sup_gid = jsondata.get('parms').get('empdetail').get('Employeesprvsrgid')
            obj_sales.address_gid = addres
            obj_sales.hierarchy_gid = jsondata.get('parms').get('empdetail').get('Employeehier')
            obj_sales.branch_gid = jsondata.get('parms').get('empdetail').get('Employeebranch')
            obj_sales.jsonData = json.dumps(jsondata.get('jsondata1').get('jsondata1'))
            obj_sales.emp_mobileno = jsondata.get('parms').get('empdetail').get('Employeemob')
            obj_sales.email = jsondata.get('parms').get('empdetail').get('Employeemail')
            employ = outputReturn(obj_sales.set_employee(), 0)
        if (employ > 0):
            obj_sales.contact_gid = addrss
            obj_sales.cont_refcode = 'EMP'
            obj_sales.cont_refgid = employ
            obj_sales.contacttype_gid = jsondata.get('parms').get('empdetail').get('ContactType')
            obj_sales.conper1 = jsondata.get('parms').get('empdetail').get('Personname')
            obj_sales.designation_gid = jsondata.get('parms').get('empdetail').get('Designation')
            obj_sales.landline_no = jsondata.get('parms').get('empdetail').get('Landline1')
            obj_sales.landline_no1 = jsondata.get('parms').get('empdetail').get('Landline2')
            obj_sales.mobile_no = jsondata.get('parms').get('empdetail').get('Mobilenum')
            obj_sales.mobile_no1 = jsondata.get('parms').get('empdetail').get('Mobilenum2')
            obj_sales.email = jsondata.get('parms').get('empdetail').get('Emailid')
            obj_sales.cont_dob = jsondata.get('parms').get('empdetail').get('BirthDate')
            obj_sales.wedding_day = jsondata.get('parms').get('empdetail').get('Wedingday')
            out_message = outputReturn(obj_sales.set_contact(), 0)
            return JsonResponse(out_message, safe=False)

def empactinact(request):
    if request.method == 'POST':
        empact = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        empact.employee_gid = jsondata.get('params').get('Emp_gid')
        empact.entity_gid = request.session['Entity_gid']
        empact.action = jsondata.get('params').get('Action')
        actinact_res = outputReturn(empact.set_employee(), 0)
        return JsonResponse(actinact_res, safe=False)

def employeeupset(request):
    if request.method == 'POST':
        addrss = 0
        employ = 0
        obj_sales = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_sales.action = jsondata.get('parms').get('Action')
        obj_sales.create_by = request.session['Emp_gid']
        obj_sales.entity_gid = request.session['Entity_gid']
        if obj_sales.action != '':
            obj_sales.add_refcode = 'EMP'
            obj_sales.address1 = jsondata.get('parms').get('empdetail').get('address1')
            obj_sales.address2 = jsondata.get('parms').get('empdetail').get('address2')
            obj_sales.address3 = jsondata.get('parms').get('empdetail').get('address3')
            obj_sales.pincode_no = jsondata.get('parms').get('empdetail').get('pincode')
            obj_sales.state_gid = jsondata.get('parms').get('empdetail').get('state')
            obj_sales.district_gid = jsondata.get('parms').get('empdetail').get('district')
            obj_sales.city_gid = jsondata.get('parms').get('empdetail').get('city')
            obj_sales.address_gid = jsondata.get('parms').get('empdetail').get('Address_gid')
            obj_sales.create_by = request.session['Emp_gid']
            obj_sales.empdetail = jsondata.get('parms').get('data')
            addres = outputReturn(obj_sales.set_address(), 0)
        if (addres != 0):
            obj_sales.employee_gid = jsondata.get('parms').get('empdetail').get('empl_gid')
            obj_sales.employee_code = jsondata.get('parms').get('empdetail').get('Employeecode')
            obj_sales.employee_name = jsondata.get('parms').get('empdetail').get('Employeename')
            obj_sales.gender = jsondata.get('parms').get('empdetail').get('Employeegndr')
            obj_sales.emp_dob = jsondata.get('parms').get('empdetail').get('Employeedob')
            obj_sales.emp_doj = jsondata.get('parms').get('empdetail').get('Employeedoj')
            obj_sales.department_gid = jsondata.get('parms').get('empdetail').get('Employeedept')
            obj_sales.designation_gid = jsondata.get('parms').get('empdetail').get('Employeedesgn')
            obj_sales.emp_sup_name = jsondata.get('parms').get('empdetail').get('Employeesprvsr')
            obj_sales.emp_sup_gid = jsondata.get('parms').get('empdetail').get('Employeesprvsrgid')
            obj_sales.address_gid = jsondata.get('parms').get('empdetail').get('Address_gid')
            obj_sales.hierarchy_gid = jsondata.get('parms').get('empdetail').get('Employeehier')

            obj_sales.jsonData = json.dumps(jsondata.get('jsondata1').get('jsondata1'))
            obj_sales.emp_mobileno = jsondata.get('parms').get('empdetail').get('Employeemob')
            obj_sales.email = jsondata.get('parms').get('empdetail').get('Employeemail')
            employ = outputReturn(obj_sales.set_employee(), 0)
        if (employ != 0):
            obj_sales.contact_gid = jsondata.get('parms').get('empdetail').get('contact_gid')
            obj_sales.cont_refcode = 'EMP'
            obj_sales.cont_refgid = 1
            obj_sales.contacttype_gid = jsondata.get('parms').get('empdetail').get('ContactType')
            obj_sales.conper1 = jsondata.get('parms').get('empdetail').get('Personname')
            obj_sales.designation_gid = jsondata.get('parms').get('empdetail').get('Designation')
            obj_sales.landline_no = jsondata.get('parms').get('empdetail').get('Landline1')
            obj_sales.landline_no1 = jsondata.get('parms').get('empdetail').get('Landline2')
            obj_sales.mobile_no = jsondata.get('parms').get('empdetail').get('Mobilenum')
            obj_sales.mobile_no1 = jsondata.get('parms').get('empdetail').get('Mobilenum2')
            obj_sales.email = jsondata.get('parms').get('empdetail').get('Emailid')
            obj_sales.cont_dob = jsondata.get('parms').get('empdetail').get('BirthDate')
            obj_sales.wedding_day = jsondata.get('parms').get('empdetail').get('Wedingday')
            out_message = outputReturn(obj_sales.set_contact(), 0)
            return JsonResponse(out_message, safe=False)


def employedit_get(request):
    if request.method == 'GET':
        custedt = mMasters.Masters()
        custedt.employee_gid = request.GET['empl_gid']
        custedt.cluster = request.GET['cluster']
        custedt.jsonData = json.dumps({"entity_gid": [request.session['Entity_gid']], "client_gid": []})
        customer = custedt.get_employee()
        jdata = customer.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def hierarchy(request):
    if request.method == 'GET':
        types = mMasters.Masters()
        types.action = 'E'
        types.entity_gid = request.session['Entity_gid']
        dict_add = types.getHierarchy()
        jdata = dict_add.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def branchview(request):
    if request.method == 'GET':
        types = mMasters.Masters()
        types.action = 'E'
        types.entity_gid = request.session['Entity_gid']
        dict_add = types.getBranch()
        jdata = dict_add.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def commondropdown(request):
    if request.method == 'GET':
        obj_dropdown = mMasters.Masters()
        obj_dropdown.table_name = request.GET['table_name']
        obj_dropdown.gid = request.GET['search_gid']
        obj_dropdown.name = request.GET['search_name']
        obj_dropdown.entity_gid = request.session['Entity_gid']
        df_dropdown = obj_dropdown.get_ddl()
        jdata = df_dropdown.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def getroute(request):
    if request.method == 'GET':
        custedt = mMasters.Masters()
        custedt.action = request.GET['action']
        custedt.route_code = request.GET['slice']
        custedt.entity_gid = request.session['Entity_gid']
        customer = custedt.getRouteDtl()
        jdata = customer.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def texteditor(request):
    return render(request, "Admin/bigflow_mst_Texteditor.html")
def userreport(request):
    return render(request, "Common/userreport.html")
def trandatadetails(request):
   if request.method == 'POST':
       jsondata = json.loads(request.body.decode('utf-8'))
       action = jsondata.get('Type')
       type = jsondata.get('Sub_Type')
       # classification = jsondata.get('classification')
       main = json.dumps(jsondata.get('data'))
       params = {'Type': "" + action + "",
                 'Sub_Type': "" +type + ""}
       headers = {"content-type": "application/json", "Authorization": "" + token + ""}
       resp = requests.post("" + ip + "/Agaentsmry", params=params, data=main, headers=headers)
       #print(resp)
       response = resp.content.decode("utf-8")
       # a = json.loads(response)
       bb = (json.loads(response)).get('DATA')
       # print(list(b))
       # bb=[{'employee_gid': 1, 'employee_code': 'VS0001', 'employee_name': 'P. PON SIVAKUMAR', 'ref_name': 'PR',
       #      'ref_gid': 1, 'tran_by': 0, 'number_of_count': 0, 'tran_from': 0, 'number_of_count1': 0,
       #      'tran_fromdate': None, 'tran_fromdate1': None, 'total': 1},
       #     {'employee_gid': 1, 'employee_code': 'VS0001', 'employee_name': 'P. PON SIVAKUMAR', 'ref_name': 'POMAKER',
       #      'ref_gid': 2, 'tran_by': 0, 'number_of_count': 0, 'tran_from': 0, 'number_of_count1': 0, 'tran_fromdate': None,
       #      'tran_fromdate1': None, 'total': 2},
       #     {'employee_gid': 2, 'employee_code': 'VS0001', 'employee_name': 'P. PON SIVAKUMAR', 'ref_name': 'POMAKER',
       #      'ref_gid': 2, 'tran_by': 0, 'number_of_count': 0, 'tran_from': 0, 'number_of_count1': 0,
       #      'tran_fromdate': None, 'tran_fromdate1': None, 'total': 33}
       #     ]
       unique={each['employee_gid']:each for each in bb}.values()
       #print(unique)
       a=list(unique)
       #print(a[0])
       newlist=[];
       for i in range(0,len(a)):
           res={}
           res = dict((k, a[i].get(k)) for k in ['employee_gid', 'employee_name','employee_code']  if k in a[i])
           for j in range(0,len(bb)):
               if a[i].get('employee_gid') == bb[j].get('employee_gid'):
                   res[bb[j].get('ref_name')]=bb[j].get('total')
           newlist.append(res)
       print(newlist)
       return JsonResponse(newlist, safe=False)


def mailtemplate(request):
    return render(request, "Admin/bigflow_mst_mail-template.html")


def mailtemplatesummary(request):
    return render(request, "Admin/bigflow_mst_mail-template-smmry.html")


def sendmailTemplate(request):
    # if request.method == 'POST':
    #    jsondata = json.loads(request.body.decode('utf-8'))
    # subject ="Hey {name}".format(name="selva") #jsondata.get('params').get('sendjson').get('Subject')
    from_email = 'selvakumaremmy@gmail.com'
    to = "vsolvstab@gmail.com"  # jsondata.get('params').get('sendjson').get('To')
    cc = ["vsolvstab1@gmail.com"]  # jsondata.get('params').get('sendjson').get('Cc')
    ctx = {
        'Mode': 'selva',
    }
    subject = "Hey {name}".format(name=ctx['Mode'])
    # message ="<p>this is testing :<br/></p><p>               {InvNo} hello<br/></p>"
    # out = re.sub("<.*?>", "", message)
    # message = out.format(InvNo=ctx['InvNo'])
    message = get_template('MailTemplate/T1.html').render(ctx)
    msg = EmailMultiAlternatives(subject, message, to=[to], from_email=from_email, cc=cc)
    msg.attach_alternative(message, "text/html")
    msg.send()
    return JsonResponse("success", safe=False)


def Templatecreation(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        Templatename = jsondata.get('params').get('templatename')
        content = jsondata.get('params').get('tag')
        f = open('Bigflow/Master/templates/MailTemplate/%s.html' % Templatename, 'w')
        f.write(content)
        f.close()
        return JsonResponse("success", safe=False)


def EditTemplate(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        Temp_name = jsondata.get('params').get('mail_templatename')
        fh = open(BASE_DIR + '/Bigflow/Master/templates/MailTemplate/%s.html' % Temp_name)
        html = fh.read()
        return JsonResponse(html, safe=False)


def getquerydata(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        query = mMasters.Masters()
        query.mail_headergid = jsondata.get('params').get('mail_headergid')
        query.mail_headername = jsondata.get('params').get('mail_headername')
        query.mail_detailgid = jsondata.get('params').get('mail_detailgid')
        out = query.mailquery_get()
        if query.mail_headergid == 0:
            query_groupby = (out[['mailqueryheader_gid', 'mailqueryheader_name']]).groupby(
                ['mailqueryheader_gid', 'mailqueryheader_name']).size().reset_index();
        else:
            query_groupby = out
        jdata = query_groupby.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def MailTemplate_set(request):
    if request.method == 'POST':
        Template = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        Template.action = jsondata.get('params').get('action')
        Template.type = jsondata.get('params').get('type')
        Template.Template_json = jsondata.get('params').get('Template_json')
        Htmlconversion_data = Template.Template_json.get('TEMPLATEDETAIL')
        Templatename = Htmlconversion_data[0]['template_name']
        content = jsondata.get('params').get('Temphtml')
        Template.entity_gid = request.session['Entity_gid']
        Template.employee_gid = request.session['Emp_gid']
        out = outputReturn(Template.set_MailTemplte(), 1)
        if out == 'SUCCESS':
            f = open('Bigflow/Master/templates/MailTemplate/%s.html' % Templatename, 'w')
            f.write(content)
            f.close()
        return JsonResponse(out, safe=False)


def getTemplatedata(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        Temp = mMasters.Masters()
        Temp.mail_templategid = jsondata.get('params').get('mail_templategid')
        Temp.mail_templatename = jsondata.get('params').get('mail_templatename')
        Temp.mail_templatecode = jsondata.get('params').get('mail_templatecode')
        out = Temp.mailtemplate_get()
        jdata = out.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def getuniquecode(request):
    if request.method == 'GET':
        uniq = mMasters.Masters()
        uniq.action = request.GET['action']
        uniq.type = request.GET['type']
        uniq.json_unique = request.GET['jsondata']
        uniq.entity_gid = request.session['Entity_gid']
        uniqu_code = uniq.get_unique()
        jdata = uniqu_code.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def gettaxdetails(request):
    if request.method == 'GET':
        taxdtl = mMasters.Masters()
        taxdtl.type = request.GET['type']
        taxdtl.group = request.GET['group']
        taxdtl.json_unique = request.GET['jsondata']
        taxdtl.entity_gid = request.session['Entity_gid']
        df_taxdetl = taxdtl.get_taxdetails()
        jdata = df_taxdetl.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def commentset(request):
    if request.method == 'POST':
        cmt_dtl = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        cmt_dtl.action = jsondata.get('params').get('action')
        cmt_dtl.type = jsondata.get('params').get('type')
        cmt_dtl.jsonData = jsondata.get('params').get('json')
        cmt_dtl.entity_gid = request.session['Entity_gid']
        cmt_dtl.create_by = request.session['Emp_gid']
        out_message = outputReturn(cmt_dtl.set_cmddetails(), 0)
        return JsonResponse(out_message, safe=False)


def commentget(request):
    if request.method == 'POST':
        cmt_dtl = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        cmt_dtl.action = jsondata.get('params').get('action')
        cmt_dtl.type = jsondata.get('params').get('type')
        cmt_dtl.jsonData = jsondata.get('params').get('json')
        cmt_dtl.entity_gid = request.session['Entity_gid']
        cmt_dtl.create_by = request.session['Emp_gid']
        cmt_data = cmt_dtl.get_cmddetails()
        jdata = cmt_data.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def employee_executive(request):
    if request.method == 'GET':
        obj_dropdown = mMasters.Masters()
        obj_dropdown.action = 'DEBIT'
        json_data = '{"Table_name":"gal_mst_temployee","Column_1":"employee_gid,employee_name,employee_dept_gid","Column_2":"","Where_Common":"employee","Where_Primary":"dept_gid","Primary_Value":"2","Order_by":"name"}'
        obj_dropdown.jsonData = json_data
        obj_dropdown.entity_gid = request.session['Entity_gid']
        df_dropexec = obj_dropdown.get_alltablevalue()
        jdata = df_dropexec.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def employee_allexecutive(request):
    if request.method == 'GET':
        obj_dropdown = mMasters.Masters()
        obj_dropdown.action = 'DEBIT'
        json_data = '{"Table_name":"gal_mst_temployee","Column_1":"employee_gid,employee_name,employee_dept_gid","Column_2":"","Where_Common":"employee","Where_Primary":"dept_gid","Primary_Value":"","Order_by":"name"}'
        obj_dropdown.jsonData = json_data
        obj_dropdown.entity_gid = request.session['Entity_gid']
        df_dropexec = obj_dropdown.get_alltablevalue()
        jdata = df_dropexec.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def city_get(request):
    if request.method == 'GET':
        obj_city = mMasters.Masters()
        df_city = obj_city.get_city()
        jdata = df_city.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def city_set(request):
    if request.method == 'POST':
        cityset = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        cityset.action = jsondata.get('parms').get('action')
        cityset.jsonData = jsondata.get('parms').get('cityjson')
        cityset.entity_gid = request.session['Entity_gid']
        cityset.create_by = request.session['Emp_gid']
        df_cityset = outputReturn(cityset.set_city(), 0)
        return JsonResponse(df_cityset, safe=False)


def suppplierproductmap_set(request):
    if request.method == 'POST':
        supplierproductset = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        supplierproductset.action = jsondata.get('parms').get('action')
        supplierproductset.jsonData = jsondata.get('parms').get('supplierratejson')
        supplierproductset.entity_gid = request.session['Entity_gid']
        supplierproductset.create_by = request.session['Emp_gid']
        df_supplierproductset = outputReturn(supplierproductset.set_supplierproductmap(), 0)
        return JsonResponse(df_supplierproductset, safe=False)


def suppplierproductmap_get(request):
    if request.method == 'POST':
        productname = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        productname.action = 'Full_wise'
        productname.supplier_gid = jsondata.get('params').get('supplier_gid')
        productname.product_gid = jsondata.get('params').get('product_gid')
        productname.char_active = jsondata.get('params').get('char_active')
        data = productname.get_productnames()
        jdata = data.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


# Client

def client(request):
  #  utl.check_authorization(request)(request)
    return render(request, "Client/bigflow_mst_client.html")


def clientcreate(request):
    return render(request, "Client/bigflow_mst_clientcreate.html")


# client
def client_get(request):
    if request.method == 'GET':
        obj_master = mMasters.Masters()
        client_gid = request.GET['client_gid']
        if (client_gid != ''):
            obj_master.client_gid = request.GET['client_gid']
            obj_master.entity_gid = request.session['Entity_gid']
            customer = obj_master.get_client()
            jdata = customer.to_json(orient='records')
            return JsonResponse(jdata, safe=False)
        else:
            obj_master.entity_gid = request.session['Entity_gid']
            customer = obj_master.get_client()
            jdata = customer.to_json(orient='records')
            return JsonResponse(jdata, safe=False)


def client_set(request):
    if request.method == 'POST':
        clientset = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8'))
        clientset.action = jsondata.get('parms').get('action')
        clientset.jsonData = jsondata.get('parms').get('clientjson')
        clientset.entity_gid = request.session['Entity_gid']
        clientset.create_by = request.session['Emp_gid']
        df_cityset = outputReturn(clientset.set_client(), 0)
        return JsonResponse(df_cityset, safe=False)


def SetCityPincode(request):
    if request.method=='POST':
        jsondata=json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Action')=='Insert' and (jsondata.get('Type')=='State_Insert')):
            Action = jsondata.get('Action')
            Type = jsondata.get('Type')
            datas = json.dumps(jsondata.get('data').get('params'))
            Emp_gid = jsondata.get('create_by')
            param = {'Action': Action,'Type':Type,'Emp_gid': Emp_gid}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Master_State_Details", params=param, headers=headers, data=datas,
                                   verify=False)
            result = result.content.decode("utf-8")
            return JsonResponse(json.loads(result), safe=False)
        elif (jsondata.get('Action')=='Insert' and (jsondata.get('Type')=='District_Insert')):
            Action = jsondata.get('Action')
            Type = jsondata.get('Type')
            datas = json.dumps(jsondata.get('data').get('params'))
            Emp_gid = jsondata.get('create_by')
            param = {'Action': Action,'Type':Type,'Emp_gid': Emp_gid}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Master_State_Details", params=param, headers=headers, data=datas,
                                   verify=False)
            result = result.content.decode("utf-8")
            return JsonResponse(json.loads(result), safe=False)
        elif(jsondata.get('Action'))=='insert':
            Action=jsondata.get('Action')
            datas=json.dumps(jsondata.get('data').get('params'))
            Emp_gid=request.session['Emp_gid']
            Entity_gid=request.session['Entity_gid']
            param={'Action':Action,'Entity_gid':Entity_gid,'Emp_gid':Emp_gid}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Master_State_Details", params=param,headers=headers,data=datas,verify=False)
            result = result.content.decode("utf-8")
            results=json.loads(result)
            results=results[0]
            results=results.split(",")
            results=results[1]
            return JsonResponse(results, safe=False)