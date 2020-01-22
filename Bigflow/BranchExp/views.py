from django.shortcuts import render
from django.db import connection
import pandas as pd
from django.http import JsonResponse, HttpResponse
import json
from Bigflow.BranchExp.model import mBranch as mbranch

import json
import numpy as np
import requests
import base64
import Bigflow.Core.models as common
token = ""
ip = common.localip()

def Branch_Template(request,template_name):
    template_name = template_name
    if template_name is not '':
         return render(request, template_name+".html")

def outputReturn(tubledtl, index):
    temp = tubledtl[0].split(',')
    if (len(temp) > 1):
        if (index == 0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return temp[0]


def test(request):
    cursor = connection.cursor()
    parameters = ()
    cursor.callproc('apro', parameters)
    columns = [x[0] for x in cursor.description]
    rows = cursor.fetchall()
    rows = list(rows)
    grn_dtl = pd.DataFrame(rows, columns=columns)
    jdata = grn_dtl.to_json(orient='records')
    return JsonResponse(json.loads(jdata), safe=False)

def change_value(request):
    cursor = connection.cursor()
    jsondata = json.loads(request.body.decode('utf-8'))
    id = jsondata.get('id')
    parameters = (id)
    query = """update a_table set column3 = 'APPROVED' where id = %s"""
    cursor.execute(query, parameters)
    return JsonResponse(json.loads(""), safe=False)

def change_value_l(request):
    cursor = connection.cursor()
    jsondata = json.loads(request.body.decode('utf-8'))
    value = jsondata.get('value')
    sup = jsondata.get('status')
    parameters = (value,sup)
    query = """insert into a_table  (colmn1,column_id,column2,column3,suppl) values ('rent',3,'value',%s,%s)"""
    cursor.execute(query, parameters)
    parameters = (sup)
    query = """insert into a_table  (colmn1,column_id,column2,column3,suppl) values ('rent',6,'status','Pending',%s)"""
    cursor.execute(query, parameters)
    return JsonResponse(json.loads(""), safe=False)

def Get_expense(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'EXPENSE_DATA':
            objgrp = jsondata.get('Group')
            objtyp = jsondata.get('Type')
            objsubtyp = jsondata.get('Sub_Type')
            params = {'Group': "" + objgrp + "", 'Type': "" + objtyp + "", 'SubType': "" + objsubtyp + ""}
            headers = {"content-type": "application/json", "Authorization": "" + objgrp + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/Expense_Process", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)

def Set_expense(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Group')) == 'EXPENSE_DATA':
            objgrp = jsondata.get('Group')
            objtyp = jsondata.get('Type')
            objsubtyp = jsondata.get('Action')
            params = {'Group': "" + objgrp + "", 'Type': "" + objtyp + "", 'Action': "" + objsubtyp + ""}
            headers = {"content-type": "application/json", "Authorization": "" + objgrp + ""}
            datas = json.dumps(jsondata)
            resp = requests.post("" + ip + "/Expense_ProcessSet", params=params, data=datas, headers=headers,
                                 verify=False)
            response = resp.content.decode("utf-8")
            return HttpResponse(response)


def insertNewBranchDetails(request):
    jsondata = json.loads(request.body.decode('utf-8'))
    if (jsondata.get('Type')) == 'INSERT':
        type = jsondata.get('Type')
        sub_type = jsondata.get('Sub_Type')
        datas = json.dumps(jsondata.get('data'))
        params = {'Type': type, 'Sub_Type': sub_type}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        result = requests.post("" + ip + "/Br_Property_Proccess_Set", params=params, headers=headers, data=datas,
                               verify=False)
        results = result.content.decode("utf-8")
        return JsonResponse(json.loads(results), safe=False)
    elif (jsondata.get('Type')) == 'update':
        type = jsondata.get('Type')
        sub_type = jsondata.get('Sub_Type')
        datas = json.dumps(jsondata.get('data'))
        params = {'Type': type, 'Sub_Type': sub_type}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}
        result = requests.post("" + ip + "/Br_Property_Proccess_Set", params=params, headers=headers, data=datas,
                               verify=False)
        results = result.content.decode("utf-8")
        return JsonResponse(json.loads(results), safe=False)



# def insertNewBranchDetails(request):
#     if request.method=='POST':
#         propertyset=mbranch.BranchExp_model()
#         jsondata = json.loads(request.body.decode('utf-8'))
#         if (jsondata.get('params').get('Type')) == 'Insert':
#             propertyset.type=jsondata.get('params').get('Type')
#             propertyset.sub_type=jsondata.get('params').get('Sub_Type')
#             propertyset.json_classification = json.dumps(jsondata.get('params').get('classification'))
#             propertyset.filter_json=json.dumps(jsondata.get('params').get('filters'))
#             result = outputReturn(propertyset.property_set(),0)
#             return JsonResponse(result, safe=False)


def br_maker_summary(request):
    return render(request, "Br_MakerSummary.html")
def brPropertyApproval(request):
    return render(request, "Br_PropertyApproval.html")

def brGetPropertyType(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        if (jsondata.get('Type'))== 'PRODUCT':
            type = jsondata.get('Type')
            datas= json.dumps(jsondata.get('Params'))
            entity_gid = request.session['Entity_gid']
            params = {'Type': type,'entity_gid':entity_gid}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Br_Property_Proccess_Get", params=params, headers=headers, data=datas,
                                   verify=False)
            results = result.content.decode("utf-8")
            return JsonResponse(json.loads(results), safe=False)

def brGetPropertyDetails(request):
    if request.method=='POST':
        jsondata=json.loads(request.body.decode('utf-8'))
        if(jsondata.get('Type'))=='PROPERTY':
            Type = jsondata.get('Type')
            Sub_Type = jsondata.get('Sub_Type')
            datas = json.dumps(jsondata.get('data').get('params'))
            params = {'Type': Type, 'Sub_Type': Sub_Type}
            headers = {"content-type": "application/json", "Authorization": "" + token + ""}
            result = requests.post("" + ip + "/Br_Property_Proccess_Get", params=params,headers=headers,data=datas,verify=False)
            results = result.content.decode("utf-8")
            return JsonResponse(json.loads(results), safe=False)