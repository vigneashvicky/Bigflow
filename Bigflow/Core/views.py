from django.shortcuts import render
import json
from django.http import JsonResponse
from Bigflow.Master.Model import mMasters
from Bigflow.Transaction.Model import mFET
import Bigflow
import datetime
import socket
import Bigflow.Core.models as common
from dateutil.relativedelta import relativedelta

mMaster = Bigflow.mMasters.Masters()
mcommon = Bigflow.common
mCore = Bigflow.mCore


def loginIndex(request):
    request.session.flush()
    return render(request, "Shared/bigFlowLogin.html")


def setip_out(request):
    if request.method == 'GET':
        obj_position = mMaster
        obj_position.action = request.GET['action']
        obj_position.ipaddress = {'ipaddress': socket.gethostname()}
        obj_position.jsonData = json.loads(request.GET['jsonData'])
        obj_position.jsonData.update(obj_position.ipaddress)
        obj_position.entity_gid = request.session['Entity_gid']
        obj_position.create_by = request.session['Emp_gid']
        df_position = mcommon.outputReturn(obj_position.set_ip(), 0)
        return JsonResponse(df_position, safe=False)


def setip_sys(request):
    if request.method == 'POST':
        obj_position = mMaster
        jsondata = json.loads(request.body.decode('utf-8'))
        obj_position.action = jsondata.get('parms').get('action')
        obj_position.ipaddress = {'ipaddress': socket.gethostname()}
        obj_position.jsonData = jsondata.get('parms').get('jsonData')
        obj_position.jsonData.update(obj_position.ipaddress)
        obj_position.entity_gid = request.session['Entity_gid']
        obj_position.create_by = request.session['Emp_gid']
        df_position = mcommon.outputReturn(obj_position.set_ip(), 0)
        return JsonResponse(df_position, safe=False)


def loginpswd(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        f1 = jsondata.get('parms').get('username')
        f2 = jsondata.get('parms').get('password')
        result = mCore.get_login(f1, f2)
        if (result[1][0] == 'SUCCESS'):
            emp_id = result[0][0].get('employee_gid')
            emp_name = result[0][0].get('employee_name')
            date = result[0][0].get('date')
            request.session.flush()
            request.session['date'] = date
            request.session['Emp_gid'] = emp_id
            request.session['Emp_name'] = emp_name
            request.session['Entity_gid'] = result[0][0].get('entity_gid')
            request.session['Entity_state_gid'] = 1
            request.session['Entity_detail_gid'] = 1
            output = result[0][0]
            return JsonResponse(json.dumps(output), safe=False)
        else:
            return JsonResponse(json.dumps('FAIL'), safe=False)
    else:
        return render(request, "Shared/bigFlowLogin.html")


def welcomeIndex(request):
    return render(request, "welcome.html")

def StateAdd(request):
    return render(request, "Shared/State_popup.html")

def pdfviewer(request):
    return render(request, "Shared/pdfviewier.html")

def menuList(request):
    if request.method == 'GET':
        emp_gid = request.session['Emp_gid'];
        result = mCore.menulist(emp_gid)
        if (result[1][0] == 'FOUND'):
            output = result[0]
            return JsonResponse(json.dumps(output), safe=False)
    else:
        request.session.flush()
        return render(request, "Shared/bigFlowLogin.html")


def loaderspinnerIndex(request):
    return render(request, "Shared/loaderSpinner.html")


def customercuecardIndex(request):
    return render(request, "Sidepanel/customer_cuecard.html")


def customercuecardviewIndex(request):
    return render(request, "Shared/customer_cuecardview.html")


def customersnapshotIndex(request):
    return render(request, "Sidepanel/customer_snapshot.html")


def customerentityoutcomeIndex(request):
    return render(request, "Sidepanel/customer_entityoutcome.html")


def customercreditapproveIndex(request):
    return render(request, "Sidepanel/customer_creditapprove.html")


def customeractivitytrendIndex(request):
    return render(request, "Sidepanel/customer_activitytrend.html")


def customersnapstviewIndex(request):
    return render(request, "Shared/customer_snapshtview.html")


def customerentityviewIndex(request):
    return render(request, "Shared/customer_entityview.html")


def customeractivitytrendviewIndex(request):
    return render(request, "Shared/customer_activitytrendview.html")


def customercreditapproveviewIndex(request):
    return render(request, "Shared/customer_creditapproveview.html")


def commentviewindex(request):
    return render(request, "Shared/comment.html")


def viewDetailsIndex(request):
    return render(request, "Shared/viewDetails.html")


def commondispatch(request):
    return render(request, "Shared/commondispatch.html")


def customerSales(request):
    if request.method == 'GET':
        if (request.GET['todate'] != request.GET['fromdate']):
            ddd = (request.GET['todate'])
            today = datetime.datetime.strptime(ddd, "%d/%m/%Y")
            fdate = datetime.date(today.year, today.month, 1)
            # tdate = fdate + relativedelta(months=-11)
            # teee=relativedelta(dt1=fdate,dt2=tdate)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            # return JsonResponse(header, safe=False)
            mMaster.action = 'customerwisesale'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET['cust_gid'] + ',"fromdate":"' + common.convertDate(
                request.GET['fromdate']) + '","todate":"' + common.convertDate(request.GET['todate']) + '"}'
            df_custsales = mMaster.getcustomersales()
            mMaster.entity_gid = request.session['Entity_gid']
            df_product = (df_custsales[['product_gid', 'product_name']]) \
                .groupby(['product_gid', 'product_name']).size().reset_index();
        else:
            today = datetime.date.today()
            fdate = datetime.date(today.year, today.month, 1)
            # tdate = fdate + relativedelta(months=-11)
            # teee=relativedelta(dt1=fdate,dt2=tdate)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            # return JsonResponse(header, safe=False)
            mMaster.action = 'customerwisesale'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET[
                'cust_gid'] + ',"fromdate":"' + '' + '","todate":"' + '' + '"}'
            mMaster.entity_gid = request.session['Entity_gid']
            df_custsales = mMaster.getcustomersales()
            df_product = (df_custsales[['product_gid', 'product_name']]) \
                .groupby(['product_gid', 'product_name']).size().reset_index();
        sales_details = []
        for x, item in df_product.iterrows():
            details = {'product_gid': item['product_gid'], 'product_name': item['product_name']}
            for y in header:
                month_dtl = {}
                d = df_custsales[
                    (df_custsales['sales_month'] == y['month']) & (df_custsales['sales_year'] == y['year']) & (
                            df_custsales['product_gid'] == item['product_gid']
                    )]
                if d.empty:
                    month_dtl['sales_qty'] = ''
                    month_dtl['sales_amt_wogst'] = ''
                    details[y['month_year']] = month_dtl
                else:
                    month_dtl['sales_qty'] = d['sales_qty'].iloc[0]
                    month_dtl['sales_amt_wogst'] = d['sales_amt_wogst'].iloc[0]
                    details[y['month_year']] = month_dtl
            sales_details.append(details)
        datadetails = {'customer_name': df_custsales['customer_name'].iloc[0],
                       'employee_name': df_custsales['employee_name'].iloc[0], 'sales_details': sales_details,
                       'headers': header}
        return JsonResponse(datadetails, safe=False)


def dp_get(request):
    if request.method == 'GET':
        if (request.GET['todate'] != request.GET['fromdate']):
            ddd = (request.GET['todate'])
            today = datetime.datetime.strptime(ddd, "%d/%m/%Y")
            fdate = datetime.date(today.year, today.month, 1)
            # tdate = fdate + relativedelta(months=-11)
            # teee=relativedelta(dt1=fdate,dt2=tdate)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            # return JsonResponse(header, safe=False)
            mMaster.action = 'dpprice'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET['cust_gid'] + ',"fromdate":"' + common.convertDate(
                request.GET['fromdate']) + '","todate":"' + common.convertDate(request.GET['todate']) + '"}'
            mMaster.entity_gid = request.session['Entity_gid']
            df_custdp = mMaster.getcustomersales()
            df_product = (df_custdp[['product_gid', 'product_name']]) \
                .groupby(['product_gid', 'product_name']).size().reset_index();
        else:
            today = datetime.date.today()
            fdate = datetime.date(today.year, today.month, 1)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            # return JsonResponse(header, safe=False)
            mMaster.action = 'dpprice'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET[
                'cust_gid'] + ',"fromdate":"' + '  ' + '","todate":"' + '' + '"}'
            mMaster.entity_gid = request.session['Entity_gid']
            df_custdp = mMaster.getcustomersales()
            df_product = (df_custdp[['product_gid', 'product_name']]) \
                .groupby(['product_gid', 'product_name']).size().reset_index();
        dp_details = []
        for x, item in df_product.iterrows():
            detail = {'product_gid': item['product_gid'], 'product_name': item['product_name']}
            for y in header:
                month_dtl = {}
                d = df_custdp[
                    (df_custdp['sales_month'] == y['month']) & (df_custdp['sales_year'] == y['year']) & (
                            df_custdp['product_gid'] == item['product_gid']
                    )]
                if d.empty:
                    month_dtl['dpamount'] = ''
                    month_dtl['sales_amt_wgst'] = ''
                    detail[y['month_year']] = month_dtl
                else:
                    month_dtl['dpamount'] = d['dpamount'].iloc[0]
                    month_dtl['sales_amt_wgst'] = d['dpamount'].iloc[0] - d['sales_amt_wogst'].iloc[0]
                    detail[y['month_year']] = month_dtl
            dp_details.append(detail)
        datadetails = {'customer_name': df_custdp['customer_name'].iloc[0],
                       'employee_name': df_custdp['employee_name'].iloc[0], 'dp_details': dp_details,
                       'headers': header}
        return JsonResponse(datadetails, safe=False)


def get_categorygroup(request):
    if request.method == 'GET':
        obj_cat = mMasters.Masters()
        obj_cat.table_name = 'custcategory'
        obj_cat.entity_gid = request.session['Entity_gid']
        dict_custgrp = obj_cat.get_Masters()
        return JsonResponse(json.dumps(dict_custgrp), safe=False)


def outstnd_get(request):
    if request.method == 'GET':
        if (request.GET['todate'] != request.GET['fromdate']):
            ddd = (request.GET['todate'])
            today = datetime.datetime.strptime(ddd, "%d/%m/%Y")
            fdate = datetime.date(today.year, today.month, 1)
            # tdate = fdate + relativedelta(months=-11)
            # teee=relativedelta(dt1=fdate,dt2=tdate)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            # return JsonResponse(header, safe=False)
            mMaster.action = 'outstanding'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET['cust_gid'] + ',"fromdate":"' + common.convertDate(
                request.GET['fromdate']) + '","todate":"' + common.convertDate(request.GET['todate']) + '"}'
            mMaster.entity_gid = request.session['Entity_gid']
            df_custdp = mMaster.getcustomersales()
            df_product = (df_custdp[['customer_gid', 'customer_name']]) \
                .groupby(['customer_gid', 'customer_name']).size().reset_index();
        else:
            today = datetime.date.today()
            fdate = datetime.date(today.year, today.month, 1)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            mMaster.action = 'outstanding'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET[
                'cust_gid'] + ',"fromdate":"' + '' + '","todate":"' + '' + '"}'
            mMaster.entity_gid = request.session['Entity_gid']
            df_custdp = mMaster.getcustomersales()
            df_product = (df_custdp[['customer_gid', 'customer_name']]) \
                .groupby(['customer_gid', 'customer_name']).size().reset_index();
        os_details = []
        for x, item in df_product.iterrows():
            details = {'customer_gid': item['customer_gid'], 'customer_name': item['customer_name']}
            for y in header:
                month_dtl = {}
                d = df_custdp[
                    (df_custdp['sales_month'] == y['month']) & (df_custdp['sales_year'] == y['year']) & (
                            df_custdp['customer_gid'] == item['customer_gid']
                    )]
                if d.empty:
                    month_dtl['outstanding_amt'] = ''
                    details[y['month_year']] = month_dtl
                else:
                    month_dtl['outstanding_amt'] = d['outstanding_amt'].iloc[0]
                    details[y['month_year']] = month_dtl
                    os_details.append(details)
        datadetails = {'customer_name': df_custdp['customer_name'].iloc[0], 'os_details': os_details,
                       'headers': header}
        return JsonResponse(datadetails, safe=False)


def convertDate(stringDate):
    return datetime.datetime.strptime(stringDate, "%d/%m/%Y").strftime("%Y-%m-%d")


def payred_get(request):
    if request.method == 'GET':
        if (request.GET['todate'] != request.GET['fromdate']):
            ddd = (request.GET['todate'])
            today = datetime.datetime.strptime(ddd, "%d/%m/%Y")
            fdate = datetime.date(today.year, today.month, 1)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            mMaster.action = 'payableamount'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET['cust_gid'] + ',"fromdate":"' + common.convertDate(
                request.GET['fromdate']) + '","todate":"' + common.convertDate(request.GET['todate']) + '"}'
            mMaster.entity_gid = request.session['Entity_gid']
            df_custdp = mMaster.getcustomersales()
            df_product = (df_custdp[['customer_gid', 'customer_name']]) \
                .groupby(['customer_gid', 'customer_name']).size().reset_index();
        else:
            today = datetime.date.today()
            fdate = datetime.date(today.year, today.month, 1)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            mMaster.action = 'payableamount'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET[
                'cust_gid'] + ',"fromdate":"' + '' + '","todate":"' + '' + '"}'
            mMaster.entity_gid = request.session['Entity_gid']
            df_custdp = mMaster.getcustomersales()
            df_product = (df_custdp[['customer_gid', 'customer_name']]) \
                .groupby(['customer_gid', 'customer_name']).size().reset_index();
        PayRec_details = []
        for x, item in df_product.iterrows():
            details = {'customer_gid': item['customer_gid'], 'customer_name': item['customer_name']}
            for y in header:
                month_dtl = {}
                d = df_custdp[
                    (df_custdp['sales_month'] == y['month']) & (df_custdp['sales_year'] == y['year']) & (
                            df_custdp['customer_gid'] == item['customer_gid']
                    )]
                if d.empty:
                    month_dtl['payableamt'] = ''
                    details[y['month_year']] = month_dtl
                else:
                    month_dtl['payableamt'] = d['payableamt'].iloc[0]
                    details[y['month_year']] = month_dtl
            PayRec_details.append(details)
        datadetails = {'customer_name': df_custdp['customer_name'].iloc[0], 'PayRec_details': PayRec_details,
                       'headers': header}
        return JsonResponse(datadetails, safe=False)


def getentityget(request):
    if request.method == 'GET':
        today = datetime.date.today()
        f_date = datetime.date(today.year, 1, 1)
        t_date = f_date + relativedelta(months=11)
        if (request.GET['todate'] != request.GET['fromdate']):
            d = common.convertDateTime(request.GET['fromdate'])
            t = common.convertDateTime(request.GET['todate'])
            f_date = datetime.date(d.year, 1, 1)
            t_date = datetime.date(t.year, 12, 31)
        year_dif = (t_date.year - f_date.year) + 1
        detail_list = []
        mMaster.action = 'ALL'
        mMaster.type = ""
        mMaster.jsonData = '{"customer_gid":' + request.GET[
            'cust_gid'] + ',"fromdate":"' + str(f_date) + '","todate":"' + str(t_date) + '"}'
        mMaster.entity_gid = request.session['Entity_gid']
        df_custdp = mMaster.getentity()
        temp = f_date
        for x in range(0, year_dif):
            detail = {}
            detail = {'Year': temp.year}
            highestval = 0
            highestcol = 0
            highestout = 0
            for x in range(12):
                month_dtl = {}
                # for sales
                sale = df_custdp[0][
                    (df_custdp[0]['sales_month'] == temp.month) & (df_custdp[0]['sales_year'] == temp.year)]
                if sale.empty:
                    month_dtl['sales_amt_wogst'] = ''
                else:
                    month_dtl['sales_amt_wogst'] = (sale['sales_amt_wogst'].iloc[0])
                    if highestval < month_dtl['sales_amt_wogst']:
                        highestval = month_dtl['sales_amt_wogst']
                # for collection
                collection = df_custdp[1][
                    (df_custdp[1]['sales_month'] == temp.month) & (df_custdp[1]['sales_year'] == temp.year)]
                if collection.empty:
                    month_dtl['payableamt'] = ''
                else:
                    month_dtl['payableamt'] = (collection['payableamt'].iloc[0])
                    if highestcol < month_dtl['payableamt']:
                        highestcol = month_dtl['payableamt']
                # for outstanding
                outstanding = df_custdp[2][
                    (df_custdp[2]['sales_month'] == temp.month) & (df_custdp[2]['sales_year'] == temp.year)]
                if outstanding.empty:
                    month_dtl['outstanding_amt'] = ''
                else:
                    month_dtl['outstanding_amt'] = (outstanding['outstanding_amt'].iloc[0])
                    if highestout < (outstanding['outstanding_amt'].iloc[0]):
                        highestout = (outstanding['outstanding_amt'].iloc[0])
                detail[temp.month] = month_dtl
                temp = temp + relativedelta(months=1)
            detail['highestval'] = {'highestval': highestval}
            detail['highestcol'] = {'highestcol': highestcol}
            detail['highestout'] = {'highestout': highestout}
            detail_list.append(detail)
    return JsonResponse(detail_list, safe=False)


def getapprove(request):
    if request.method == 'GET':
        objenti = mFET.FET_model()
        objenti.action = 'OutstandingCustomer'
        objenti.customer_gid = request.GET['cust_gid']
        objenti.limit = 30
        result_ent = objenti.get_FEToutstanding_fet()
        jdata = result_ent.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def getproposed(request):
    if request.method == 'GET':
        objenti = mMasters.Masters()
        objenti.action = 'proposedbill'
        objenti.type = ""
        objenti.jsonData = ' {"customer_gid": ' + request.GET['cust_gid'] + ',"soheader_gid":' + request.GET[
            'soheader_gid'] + '}'
        objenti.entity_gid = request.session['Entity_gid']
        result_ent = objenti.getcreditapprv()
        jdata = result_ent.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


# def pendingsmry(request):
#     if request.method == 'GET':
#         obj_pendingsmry = mMasters.Masters()
#         obj_pendingsmry.customer_gid = request.GET['cust_gid']
#         df_pendingsmry = obj_pendingsmry.get_pendingsummary_get()
#         return JsonResponse(json.dumps(df_pendingsmry), safe=False)
def pendingsmry(request):
    if request.method == 'GET':
        obj_pendingsmry = mMasters.Masters()
        obj_pendingsmry.action = 'Pendingsummary'
        obj_pendingsmry.customer_gid = request.GET['cust_gid']
        result_ent = obj_pendingsmry.get_pendingsummary_get()
        jdata = result_ent.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def snapsales(request):
    if request.method == 'GET':
        if (request.GET['todate'] != request.GET['fromdate']):
            ddd = (request.GET['todate'])
            today = datetime.datetime.strptime(ddd, "%d/%m/%Y")
            fdate = datetime.date(today.year, today.month, 1)
            # tdate = fdate + relativedelta(months=-11)
            # teee=relativedelta(dt1=fdate,dt2=tdate)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            # return JsonResponse(header, safe=False)
            mMaster.action = 'customerwisesale'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET['cust_gid'] + ',"fromdate":"' + common.convertDate(
                request.GET['fromdate']) + '","todate":"' + common.convertDate(request.GET['todate']) + '"}'
            mMaster.entity_gid = request.session['Entity_gid']
            df_custsales = mMaster.getcustomersales()
            df_product = (df_custsales[['customer_gid', 'customer_name']]) \
                .groupby(['customer_gid', 'customer_name']).size().reset_index();
        else:
            today = datetime.date.today()
            fdate = datetime.date(today.year, today.month, 1)
            # tdate = fdate + relativedelta(months=-11)
            # teee=relativedelta(dt1=fdate,dt2=tdate)
            temp = fdate
            header = []
            for x in range(12):
                data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
                temp = temp + relativedelta(months=-1)
                header.append(data)
            # return JsonResponse(header, safe=False)
            mMaster.action = 'customerwisesale'
            mMaster.name = ''
            mMaster.jsonData = '{"customer_gid":' + request.GET[
                'cust_gid'] + ',"fromdate":"' + '' + '","todate":"' + '' + '"}'
            mMaster.entity_gid = request.session['Entity_gid']
            df_custsales = mMaster.getcustomersales()
            df_product = (df_custsales[['customer_gid', 'customer_name']]) \
                .groupby(['customer_gid', 'customer_name']).size().reset_index();
        sales_details = []
        for x, item in df_product.iterrows():
            details = {'customer_gid': item['customer_gid'], 'customer_name': item['customer_name']}
            for y in header:
                month_dtl = {}
                d = df_custsales[
                    (df_custsales['sales_month'] == y['month']) & (df_custsales['sales_year'] == y['year']) & (
                            df_custsales['customer_gid'] == item['customer_gid']
                    )]
                if d.empty:
                    month_dtl['sales_qty'] = ''
                    month_dtl['sales_amt_wgst'] = ''
                    details[y['month_year']] = month_dtl
                else:
                    month_dtl['sales_qty'] = d['sales_qty'].iloc[0]
                    month_dtl['sales_amt_wgst'] = d['sales_amt_wgst'].iloc[0]
                    details[y['month_year']] = month_dtl
            sales_details.append(details)
        datadetails = {'customer_name': df_custsales['customer_name'].iloc[0],
                       'employee_name': df_custsales['employee_name'].iloc[0], 'sales_details': sales_details,
                       'headers': header}
        return JsonResponse(datadetails, safe=False)


def getactivity(request):
    if request.method == 'GET':
        ddd = (request.GET['todate'])
        today = datetime.datetime.strptime(ddd, "%Y-%m-%d")
        fdate = datetime.date(today.year, today.month, 1)
        temp = fdate
        header = []
        header_month = []
        for x in range(120):
            data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
            temp = temp + relativedelta(months=1)
            header.append(data)
        mMaster.action = 'SALES'
        mMaster.entity_gid = request.session['Entity_gid']
        mMaster.jsonData = '{"customer_gid":' + request.GET['cust_gid'] + '}'
        df_sales = mMaster.getactivitytrend()
        df_product = (df_sales[['Activity_Year']]) \
            .groupby(['Activity_Year']).size().reset_index();
        for x in range(12):
            data = {'month': x + 1}
            header_month.append(data)
    sales_details = []
    for x, item in df_product.iterrows():
        details = {'Activity_Year': str(item['Activity_Year'])}
        for y in header:
            month_dtl = {}
            if item['Activity_Year'] == y['year']:
                d = df_sales[
                    (df_sales['period'] == y['month']) & (df_sales['Activity_Year'] == y['year'])
                    ]
                if d.empty:
                    month_dtl['cuecards_value'] = ''
                    details[y['month']] = month_dtl
                else:
                    month_dtl['cuecards_value'] = d['cuecards_value'].iloc[0]
                    details[y['month']] = month_dtl
        sales_details.append(details)
    datadetails = {'customer_name': df_sales['customer_name'].iloc[0],
                   'sales_details': sales_details,
                   'headers': header,
                   'header_month': header_month}
    return JsonResponse(datadetails, safe=False)


def getactivitycol(request):
    if request.method == 'GET':
        ddd = (request.GET['todate'])
        today = datetime.datetime.strptime(ddd, "%Y-%m-%d")
        fdate = datetime.date(today.year, today.month, 1)
        temp = fdate
        header = []
        header_month = []
        for x in range(120):
            data = {'month': temp.month, 'year': temp.year, 'month_year': str(temp.month) + '-' + str(temp.year)}
            temp = temp + relativedelta(months=1)
            header.append(data)
        mMaster.action = 'PAYMENT'
        mMaster.entity_gid = request.session['Entity_gid']
        mMaster.jsonData = '{"customer_gid":' + request.GET['cust_gid'] + '}'
        df_sales = mMaster.getactivitytrend()
        df_product = (df_sales[['Activity_Year']]) \
            .groupby(['Activity_Year']).size().reset_index();
        for x in range(12):
            data = {'month': x + 1}
            header_month.append(data)
    collection_details = []
    for x, item in df_product.iterrows():
        details = {'Activity_Year': str(item['Activity_Year'])}
        for y in header:
            month_dtl = {}
            if item['Activity_Year'] == y['year']:
                d = df_sales[
                    (df_sales['period'] == y['month']) & (df_sales['Activity_Year'] == y['year'])
                    ]
                if d.empty:
                    month_dtl['cuecards_value'] = ''
                    details[y['month']] = month_dtl
                else:
                    month_dtl['cuecards_value'] = d['cuecards_value'].iloc[0]
                    details[y['month']] = month_dtl
        collection_details.append(details)
    datadetails = {'customer_name': df_sales['customer_name'].iloc[0],
                   'collection_details': collection_details,
                   'headers': header,
                   'header_month': header_month}
    return JsonResponse(datadetails, safe=False)


def setPosition(request):
    if request.method == 'GET':
        jsondata = json.loads(request.GET['details'])
        obj_position = mCore.login()
        obj_position.action = 'INSERT'
        obj_position.latlong_gid = 0
        obj_position.employee_gid = request.session['Emp_gid']
        obj_position.latitude = jsondata.get('latitude')
        obj_position.longitude = jsondata.get('longitude')
        obj_position.entity_gid = request.session['Entity_gid']
        obj_position.create_by = request.session['Emp_gid']
        df_position = mcommon.outputReturn(obj_position.setposition(), 0)
        return JsonResponse(df_position, safe=False)


def getposition(request):
    if request.method == 'GET':
        obj_poisionget = mCore.login()
        obj_poisionget.action = request.GET['action']
        obj_poisionget.employee_gid = request.GET['emp_gid']
        obj_poisionget.from_date = mcommon.convertDate(request.GET['date'])
        if request.GET['todate'] == '':
            obj_poisionget.to_date = ''
        else:
            obj_poisionget.to_date = mcommon.convertDate(request.GET['todate'])
        obj_poisionget.entity_gid = request.session['Entity_gid']
        df_position = obj_poisionget.getposition()
        # df_position.rename(columns={'latlong_latitude': 'tesse', 'oldName2': 'newName2'}, inplace=True)
        jdata = df_position.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def getdayroute(request):
    if request.method == 'GET':
        obj_dayrouteget = mMasters.Masters()
        obj_dayrouteget.action = request.GET['action']
        obj_dayrouteget.employee_gid = request.GET['emp_gid']
        obj_dayrouteget.from_date = request.GET['date']
        if request.GET['todate'] == '':
            obj_dayrouteget.to_date = ''
        else:
            obj_dayrouteget.to_date = request.GET['todate']
        obj_dayrouteget.entity_gid = request.session['Entity_gid']
        df_dayroute = obj_dayrouteget.dayrouteget()
        # df_position.rename(columns={'latlong_latitude': 'tesse', 'oldName2': 'newName2'}, inplace=True)
        jdata = df_dayroute.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def setDayroute(request):
    if request.method == 'GET':
        jsondata = json.loads(request.GET['day'])
        obj_position = mMasters.Masters()
        obj_position.action = request.GET['action']
        obj_position.jsonData = jsondata
        obj_position.entity_gid = request.session['Entity_gid']
        obj_position.create_by = request.session['Emp_gid']
        df_position = obj_position.dayrouteset()
        return JsonResponse(df_position, safe=False)


def routedaymap(request):
    if request.method == 'GET':
        objenti = mMasters.Masters()
        objenti.action = 'ROUTE_DAYS'
        objenti.json_employee_gid = ' {"routeemp_gid": ' + request.GET['emp_gid'] + '}'
        objenti.entity_gid = request.session['Entity_gid']
        result_ent = objenti.getRouteDtl()
        jdata = result_ent.to_json(orient='records')
        return JsonResponse(jdata, safe=False)


def employedaymap(request):
    if request.method == 'POST':
        obj_setroute = mMasters.Masters()
        jsondata = json.loads(request.body.decode('utf-8')).get('parms')
        obj_setroute.action = jsondata.get('action')
        obj_setroute.json_employee_gid = json.dumps(jsondata.get('emp_det'))
        obj_setroute.create_by = request.session['Emp_gid']
        obj_setroute.entity_gid = request.session['Entity_gid']
        out_message = mcommon.outputReturn(obj_setroute.setRouteDtl(), 1)
        return JsonResponse(out_message, safe=False)


def collectionperformanceIndex(request):
    return render(request, "report/collection_performance_monthwise.html")


def getcollectionperformance(request):
    if request.method == 'GET':
        obj_col_per = mCore.login()
        obj_col_per.action = request.GET['action']
        obj_col_per.type = request.GET['type']
        obj_col_per.from_date = common.convertDate(request.GET['f_date'])
        obj_col_per.to_date = common.convertDate(request.GET['t_date'])
        obj_col_per.customer_gid = request.GET['cust_gid']
        obj_col_per.entity_gid = request.session['Entity_gid']
        out_message = obj_col_per.getcollectionperformance()
        jdata = out_message.to_json(orient='records')
        return JsonResponse(json.loads(jdata), safe=False)


def selectSupplierIndex(request):
    return render(request, "Shared/select_suppliers.html")


def selectproductIndex(request):
    return render(request, "Shared/select_product.html")


def selectEmployeeIndex(request):
    return render(request, "Shared/select_employee.html")
