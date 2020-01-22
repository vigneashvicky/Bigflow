from django.shortcuts import render
from Bigflow.inward.model import mInvoice
from django.http import JsonResponse
import json
import datetime
import pandas as pd


def inward_summary(request):
    return render(request, "inw_inwardsummary.html");

def setinwarddetails(request):
    return render(request, "inw_trn_inwardcreate.html");


def inward_create(request):
    if request.method == 'POST':
        inward_hdl =  mInvoice.inward_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        inward_hdl.action = jsondata.get('params').get('Action')
        inward_hdl.type = jsondata.get('params').get('Type')
        inward_hdl.inwardheader_json = jsondata.get('params').get('lj_header')
        inward_hdl.inwarddetail_json = jsondata.get('params').get('lj_details')
        inward_hdl.entity_gid = 1
        inward_hdl.employee_gid = request.session['Emp_gid']
        inward_header = outputSplit(inward_hdl.set_inward(), 1)
        return JsonResponse(inward_header, safe=False)

def outputSplit(tubledtl,index):
    temp=tubledtl[0].split(',')
    if(len(temp)>1):
        if (index==0):
            return int(temp[0])
        else:
            return temp[1]
    else:
        return  temp[0]

def get_inwardsummary(request):
    if request.method == 'POST':
        obj_inwardheader = mInvoice.inward_model()
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_inwardheader.action = jsondata.get('params').get('Action')
        obj_inwardheader.type = jsondata.get('params').get('Type')
        obj_inwardheader.inwardheader_json = jsondata.get('params').get('lj_filters')
        obj_inwardheader.entity_gid = 1
        df_preschedule = obj_inwardheader.get_inward()
        jdata = df_preschedule.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)

def invoice_crt(request):
    return render(request,"inw_trn_invoice.html")
