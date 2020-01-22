from datetime import datetime, timedelta
import io

import pandas as pd
import xlsxwriter
from django.shortcuts import render
from xlsxwriter import Workbook
from Bigflow.Transaction.Model import mFET, mSales
from Bigflow.Report import views_API
import json
import requests
from Bigflow.Purchase.Model import mPurchase
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.http import HttpResponse
import Bigflow.Core.models as common
from Bigflow.menuClass import utility
import base64
ip = common.localip()
headers = {"content-type": "application/json", "Authorization": "" + common.token() + ""}
# ip = common.localip()
token = common.token()

def StockSummaryIndex(request):
    return render(request, "Stock_Summary.html")


#Control sheet summary
def Control_Sheet_summary(request):
    return render(request, "Control_sheet_summary.html")


#sales &Outstanding_control
def Controlsheet(request):
    return render(request, "Sales_Outstanding_Control_Sheet.html")

#Outstanding_control
def os_Controlsheet(request):
    return render(request, "Outstanding_controlsheet.html")



#stock_controlsheet
def stock_controlsheet(request):
    return render(request, "stock_controlsheet.html")


#Excel UPload for Control-sheet
def Control_Sheet(request):
     if request.method == 'POST':
        encrypt_ex = base64.b64encode(request.FILES['file'].read())#convert excel to base64

        dcrypt_ex = encrypt_ex.decode("utf-8")
        entry_id = request.session['Entity_gid']
        excel_file = request.FILES['file']#geting the excel file from angular
        group = request.POST['Group']
        action = request.POST['Action']

        # subtype = request.POST['SubType']

        ex_type = request.POST['Type']
        drop_value = request.POST['Drop_value']
        created_by = json.dumps(request.session['Emp_gid'])
        name = request.POST['name']
        File_Extension = name.split('.')
        # File_Extension = json.dumps(File_Extension[1])
        File_Extension = File_Extension[1]

        df = pd.read_excel(excel_file)
        params = {'Group': "" + group + "", 'Action': "" + action + "", 'Type': "" + ex_type + "",
                  'Create_by': "" + created_by + ""}

        if drop_value == 'outstanding':
            try:
                df = pd.read_excel(excel_file, skiprows=[0, 1, 2, 3, 4, 5, 6, 8])
                # df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
                # print(df)
                df = df.iloc[:-1]
                final_df = df[["Party's Name", 'Date', 'Ref. No.', 'Pending','Opening']]
                final_df['Opening'] = final_df['Opening'].replace('Dr', ' ', regex=True)
                delivery_date = final_df['Date'].dt.strftime('%Y-%m-%d')
                final_df['Date'] = delivery_date
                final_df.columns = ['Customer_Name', 'Invoice_Date', 'Invoice_No', 'Pending_Amount','Amount']

                jdata = final_df.to_dict(orient='records')


                param = {'Group': "" + 'CONTROL_OUTSTANDING' + "", 'Action': "" + 'INSERT' + "", 'Type': "" + 'CONTROL_OUTSTANDING' + "",'SubType':"" + 'TALLY' +"",
                        'Create_by': "" + created_by + ""}

                resultdata = {
                    "Params": {
                        "DETAILS": {
                            "OUTSTANDING_DETAILS": jdata

                        },
                        "File": [{
                            "File_Name": name,
                            "File_Extension": File_Extension,
                            "File_Base64data": dcrypt_ex
                        }],

                        "CLASSIFICATION": {"Entity_Gid": entry_id}
                    }
                }
                dta = json.dumps(resultdata)
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}

                resp = requests.post("" + ip + "/Control_Sheet", params=param, data=dta, headers=headers, verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)


            except:
                ld_dict = {"DATA": 'ERROR_OCCURED.'}
                return HttpResponse(ld_dict)

        elif drop_value == 'stock':
            try:
                df = pd.read_excel(excel_file, skiprows=[0, 1, 2, 3, 4, 5, 6, 7,8,9,10,11])
                date = request.POST['Date']
                Godown_Gid = request.POST['Godown_Gid']
                df = df.iloc[:-1]
                df['Quantity'].fillna(0, inplace=True)
                final_df = df[['Unnamed: 0','Quantity']]
                final_df['Quantity'] = final_df['Quantity'].replace('NaN', 0, regex=True)
                final_df.columns = ['Particulars','Quantity']
                jdata = final_df.to_dict(orient='records')
                param = {'Group': "" + 'CONTROL_STOCK' + "", 'Action': "" + 'INSERT' + "", 'Type': "" + 'CONTROL_STOCK' + "",'SubType':"" + 'TALLY' +"",
                        'Create_by': "" + created_by + ""}
                resultdata = {
                    "Params": {
                        "DETAILS": {
                            "STOCK_DETAILS": jdata,
                            "Date": date,
                            "Godown_Gid": Godown_Gid
                        },
                        "File": [{
                            "File_Name": name,
                            "File_Extension": File_Extension,
                            "File_Base64data": dcrypt_ex
                        }],
                        "CLASSIFICATION": {"Entity_Gid": entry_id}
                    }
                }
                dta = json.dumps(resultdata)
                headers = {"content-type": "application/json", "Authorization": "" + token + ""}
                resp = requests.post("" + ip + "/Control_Sheet", params=param, data=dta, headers=headers, verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)

            except:
                ld_dict = {"DATA": 'ERROR_OCCURED.'}
                return HttpResponse(ld_dict)

        else:
            try:

                final_df = df[['Party Name','Item Name', 'Date', 'Voucher Number', 'Billed Quantity', 'Rate', 'Amount']]
                # final_df['Date']=pd.to_datetime(final_df['Date'])
                delivery_date = final_df['Date'].dt.strftime('%Y-%m-%d')
                final_df['Date'] = delivery_date
                final_df.columns=['Customer_Name','Product_Name', 'Invoice_Date', 'Invoice_No', 'Quantity', 'Per_Rate', 'Amount']
                jdata= final_df.to_dict(orient='records')
                resultdata = {
                    "Params": {
                        "DETAILS": {
                            "SALE_DETAILS": jdata

                        },
                        "File": [{
                            "File_Name": name,
                            "File_Extension": File_Extension,
                            "File_Base64data": dcrypt_ex
                        }],

                        "CLASSIFICATION": {"Entity_Gid": entry_id}
                    }
                }
                dta = json.dumps(resultdata)

                headers = {"content-type": "application/json", "Authorization": "" + token + ""}

                resp = requests.post("" + ip + "/Control_Sheet", params=params, data=dta, headers=headers, verify=False)
                response = resp.content.decode("utf-8")
                return HttpResponse(response)
            except:
                 ld_dict = {"DATA": 'ERROR_OCCURED.'}

                 return HttpResponse(ld_dict)


def Four_Line_Mis(request):
    return render(request, "Four_Line_MIS.html")

def performance_excel(request):
    if request.method == 'GET':
        jsondata = json.loads(request.GET['Main'])
        jsondata1=json.loads(request.GET['Sub'])
        obj_totalsales = mSales.Sales_Model()
        obj_totalsales.type = jsondata.get('Type')
        obj_totalsales.sub_type = jsondata.get('Sub_Type')
        obj_totalsales.jsonData = json.dumps(jsondata1.get('Params').get('FILTER'))
        obj_totalsales.json_classification = \
            json.dumps(jsondata1.get('Params').get('CLASSIFICATION'))
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        response['Content-Disposition'] = 'attachment; filename="PythonExport.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df_view = obj_totalsales.get_sales()
        df_view['CUSTOMER_NAME']=df_view['customer_name']
        df_view['EMPLOYEE_NAME']=df_view['employee_name']
        df_view['BRANCH_NAME']=df_view['branch_name']
        df_view['DEPARTMENT_NAME']=df_view['dept_name']
        df_view['LOCATION_NAME']=df_view['location_name']
        df_view['MONTH_WISE']=df_view['mntdate']
        df_view['SALES']=df_view['invtot']
        df_view['RECEIPT']=df_view['reptamt']
        df_view['CREDIT']=df_view['cramt']
        df_view['OUTSTANDING']=df_view['oss']
        final=df_view[['CUSTOMER_NAME','EMPLOYEE_NAME','BRANCH_NAME','DEPARTMENT_NAME','LOCATION_NAME','MONTH_WISE','SALES','RECEIPT','CREDIT','OUTSTANDING']]
        final.to_excel(writer, 'Sheet1')
        writer.save()
        return response


def get_totalsales_and_totaloutstanding(request):
    if request.method == 'POST':
        jsondata=json.loads(request.body.decode('utf-8'))
        obj = views_API.StockAPI()
        obj.group=jsondata.get('Group')
        obj.sub_type = jsondata.get('Sub_Type')
        obj.type = jsondata.get('Type')
        params={
                'Group': "" + obj.group + "",
                'Type': "" + obj.type + "",
                'Sub_Type': "" + obj.sub_type + ""
               }
        datas=json.dumps(jsondata.get('data'))
        resp=requests.post(""+ip+"/Report_Total_Sales",params=params,data=datas,headers=headers,verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)




#get controlsheetsummary
def getControl_Sheet(request):
    jsondata = json.loads(request.body.decode('utf-8'))
    if (jsondata.get('Group')) == 'INITIAL_SUMMARY':
       group=jsondata.get('Group')
       type = jsondata.get('Type')
       subtype = jsondata.get('SubType')
       emp_gid = jsondata.get('Employee_Gid')
       # data = jsondata.get('darta')

       params = {'Group': "" + group + "",  'Type': "" + type + "",
                 'SubType': "" + subtype + "", 'Employee_Gid': "" + str(emp_gid) + ""}
       headers = {"content-type": "application/json", "Authorization": "" + token + ""}

       datas = json.dumps(jsondata.get('darta'))
       resp = requests.post("" + ip + "/Control_Sheet", params=params, data=datas, headers=headers, verify=False)
       response = resp.content.decode("utf-8")

       return HttpResponse(response)


#sale summary
def getComparesale(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        group = jsondata.get('Group')
        type = jsondata.get('Type')
        subtype = jsondata.get('SubType')
        emp_gid = jsondata.get('Employee_Gid')
        # data = jsondata.get('darta')

        params = {'Group': "" + group + "", 'Type': "" + type + "",
                  'SubType': "" + subtype + "", 'Employee_Gid': "" + str(emp_gid) + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}

        datas = json.dumps(jsondata.get('darta'))
        resp = requests.post("" + ip + "/Control_Sheet", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")


        return HttpResponse(response)



#outstanding summary
def getCompareos(request):
    if request.method == 'POST':
        jsondata = json.loads(request.body.decode('utf-8'))
        group = jsondata.get('Group')
        type = jsondata.get('Type')
        subtype = jsondata.get('SubType')
        emp_gid = jsondata.get('Employee_Gid')
        # data = jsondata.get('darta')

        params = {'Group': "" + group + "", 'Type': "" + type + "",
                  'SubType': "" + subtype + "", 'Employee_Gid': "" + str(emp_gid) + ""}
        headers = {"content-type": "application/json", "Authorization": "" + token + ""}

        datas = json.dumps(jsondata.get('darta'))
        resp = requests.post("" + ip + "/Control_Sheet", params=params, data=datas, headers=headers, verify=False)
        response = resp.content.decode("utf-8")


        return HttpResponse(response)



def setupdate(request):
    if request.method == 'POST':
        jsondata=json.loads(request.body.decode('utf-8'))
        obj = views_API.StockAPI()
        obj.group=jsondata.get('Group')
        obj.action = jsondata.get('Action')
        obj.type = jsondata.get('Type')
        obj.create_by = json.dumps(jsondata.get('Create_by'))
        params={
                'Group': "" + obj.group + "",
                'Action': "" + obj.action + "",
                'Type': "" + obj.type + "",
                'Create_by': "" + obj.create_by + ""
               }
        datas=json.dumps(jsondata.get('data'))
        resp=requests.post(""+ip+"/Stock_Summary_API",params=params,data=datas,headers=headers,verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)


def StockSum(request):
    if request.method == "POST":
        jsondata = json.loads(request.body.decode('utf-8'))
        obj = views_API.StockAPI()
        obj.group = jsondata.get('Group')
        obj.type = jsondata.get('Type')
        obj.sub_type = jsondata.get('Sub_Type')
        obj.from_date = jsondata.get('From_Date')
        obj.to_date = jsondata.get('To_Date')
        obj.Product_Gid = jsondata.get('Product_Gid')
        obj.Supplier_Gid = json.dumps(jsondata.get('Supplier_Gid'))
        obj.Entity_Gid = json.dumps(jsondata.get('Entity_Gid'))
        params = {'Group': "" + obj.group + "", 'Type': "" + obj.type + "", 'Sub_Type': "" + obj.sub_type + "",
                  'From_Date': "" + obj.from_date + "", 'To_Date': "" + obj.to_date + "",
                  'Product_Gid':  obj.Product_Gid ,
                  'Supplier_Gid': "" + obj.Supplier_Gid + "", 'Entity_Gid': "" + obj.Entity_Gid + ""}
        datas = json.dumps(jsondata.get('data'))
        resp = requests.post("" + ip + "/Stock_Summary_API", params=params, data=datas, headers=headers,
                             verify=False)
        response = resp.content.decode("utf-8")
        return HttpResponse(response)



def stcksumry_overall_rept(request):
    if request.method == "GET" :
        jsondata = json.loads(request.GET['Main'])
        obj = views_API.StockAPI()
        before_date = (datetime.strptime(jsondata.get('Cur_date'), '%Y-%m-%d') - timedelta(days=6)).strftime('%Y-%m-%d')
        obj.group = jsondata.get('Group')
        obj.type = jsondata.get('Type')
        obj.sub_type = jsondata.get('Sub_Type')
        obj.from_date = jsondata.get('From_Date')
        obj.to_date = jsondata.get('To_Date')
        obj.Product_Gid = jsondata.get('Product_Gid')
        obj.Supplier_Gid = json.dumps(jsondata.get('Supplier_Gid'))
        obj.Entity_Gid = json.dumps(jsondata.get('Entity_Gid'))
        params = {'Group': "" + obj.group + "", 'Type': "" + obj.type + "", 'Sub_Type': "" + obj.sub_type + "",
                  'From_Date': "" + obj.from_date + "", 'To_Date': "" + obj.to_date + "",
                  'Product_Gid': obj.Product_Gid,
                  'Supplier_Gid': "" + obj.Supplier_Gid + "", 'Entity_Gid': "" + obj.Entity_Gid + ""}
        datas = json.dumps(jsondata.get('data'))
        resp = requests.post("" + ip + "/Stock_Summary_API", params=params, data=datas, headers=headers,
                             verify=False)
        stock_curdate = resp.content.decode("utf-8")
        data = json.loads(stock_curdate)
        data = data.get('DATA')
        df_curstk = pd.DataFrame(data)
        data = {"Params":
               { "FILTER":{"date":before_date}}}
        datas = json.dumps(data)
        resp = requests.post("" + ip + "/Stock_Summary_API", params=params, data=datas, headers=headers,
                             verify=False)
        stock_todate = resp.content.decode("utf-8")
        data = json.loads(stock_todate)
        data = data.get('DATA')
        df_tostk = pd.DataFrame(data)
        obj_sales = mPurchase.Purchase_model()
        obj_sales.type = 'SUMMARY_DATEWISE'
        obj_sales.sub_type = 'ALL'
        obj_sales.fliter = {"From_Date":before_date,"To_Date":jsondata.get('Cur_date')}
        obj_sales.classification = {"Entity_Gid":1}
        obj_sales.create_by = '1'
        data = obj_sales.get_salescount()
        df_sales = data
        df_cus = df_curstk[['product_name','stockbalance_cb']]
        df_yes = df_tostk[['stockbalance_cb']]
        df_cus['yesclsstk'] = df_tostk[['stockbalance_cb']]
        f_data = []
        headerdate = []
        for x,row in df_cus.iterrows():
            product_name = row["product_name"]
            yescb = row["yesclsstk"]
            curcb = row["stockbalance_cb"]
            dteonly=0
            for y,row in df_sales.iterrows():
               if row["product_name"] == product_name:
                   dteonly = {}
                   date = row["Dates"]
                   headerdate.append(date)
                   qty = int(row["qty"])
                   d = {'product_name':product_name,'cb1':yescb,date:qty,'cb2':curcb}
                   dteonly={date:qty}
                   for e in f_data:
                       for u in list(e):
                           prodname = e[u]
                           if(product_name == prodname):
                               e.update(dteonly)
                               d={}
                               pass
                   f_data.append(d)
        headerdate = list(dict.fromkeys(headerdate))
        headerdate.sort(key=lambda date: datetime.strptime(date, "%d-%m-%Y"))
        headerdate.insert(0, "product_name")
        headerdate.insert(1, "cb1")
        headerdate.append("cb2")
        XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type=XLSX_MIME)
        response['Content-Disposition'] = 'attachment; filename="Stock Details.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        while ({} in f_data):
            f_data.remove({})
        dff = pd.DataFrame(f_data, columns=headerdate)
        dff.index = range(1, len(dff) + 1)
        dff.to_excel(writer, sheet_name='Stock', index_label='SL NO',
                         freeze_panes=(1, 0),
                         header=headerdate)
        writer.save()
        return response



def getOutstandingDetails(employee_gid):
    type = 'OUTSTANDING_REPORT_INVOICE_WISE'
    sub_type = 'BUCKET'
    params = {'Type': "" + type + "", 'Sub_Type': "" + sub_type + ""}
    filterDetails = {}
    if employee_gid != '0':
        filterDetails['Employee_Gid'] = employee_gid
    data = {'parms': {'filter': filterDetails, 'classification': {'Entity_Gid': [1]}}};
    resp = requests.post("" + ip + "/Outstanding_AR", params=params, data=json.dumps(data), headers=headers,
                         verify=False)
    response_data = resp.content.decode("utf-8")
    response_data = json.loads(response_data)
    dff = pd.DataFrame(response_data.get('DATA'))

    outstandingList = []
    head_columns = ['S.No', 'Customer Name', 'Location', 'Invoice No', 'Invoice Date', 'Quantity', 'Bill Amount'
        , 'Due Amount', 'Due Days', '< 30', '30 - 45', '45 - 60', '60 - 75', '75 - 90', '90 - 120', '120 - 150',
                    '150 - 180', '> 180', 'Last pmt Date', 'Payment Amt', 'Aging Days','Employee Name']
    for y, df in dff.iterrows():
        outstanding = {head_columns[0]: y + 1, head_columns[1]: df['customer_name']
            , head_columns[2]: df['location_name']
            , head_columns[3]: df['fetsoutstanding_invoiceno'], head_columns[4]: df['fetsoutstanding_invoicedate']
            , head_columns[5]: df['total_sale_qty'], head_columns[6]: df['fetsoutstanding_netamount']
            , head_columns[7]: df['balance_amount'], head_columns[8]: df['Due_Days']}
        due_days = df['Due_Days']
        default_vale= 0
        if (due_days <= 30):
            outstanding[head_columns[9]] = df['balance_amount']
        else:
            outstanding[head_columns[9]] = default_vale

        if (due_days > 30 and due_days <= 45):
            outstanding[head_columns[10]] = df['balance_amount']
        else:
            outstanding[head_columns[10]] =default_vale

        if (due_days > 45 and due_days <= 60):
            outstanding[head_columns[11]] = df['balance_amount']
        else:
            outstanding[head_columns[11]] = default_vale

        if (due_days > 60 and due_days <= 75):
            outstanding[head_columns[12]] = df['balance_amount']
        else:
            outstanding[head_columns[12]] = default_vale

        if (due_days > 75 and due_days <= 90):
            outstanding[head_columns[13]] = df['balance_amount']
        else:
            outstanding[head_columns[13]] = default_vale

        if (due_days > 90 and due_days <= 120):
            outstanding[head_columns[14]] = df['balance_amount']
        else:
            outstanding[head_columns[14]] = default_vale

        if (due_days > 120 and due_days <= 150):
            outstanding[head_columns[15]] = df['balance_amount']
        else:
            outstanding[head_columns[15]] = default_vale
        if (due_days > 150 and due_days <= 180):
            outstanding[head_columns[16]] = df['balance_amount']
        else:
            outstanding[head_columns[16]] = default_vale
        if (due_days > 180):
            outstanding[head_columns[17]] = df['balance_amount']
        else:
            outstanding[head_columns[17]] = default_vale
        outstanding[head_columns[18]] = df['last_paid_date']
        outstanding[head_columns[19]] = df['last_paid_amount']
        outstanding[head_columns[20]] = df['aging_days']
        outstanding[head_columns[21]] = df['employee_name']
        outstandingList.append(outstanding)
    df_data = pd.DataFrame(outstandingList)
    if df_data.empty:
        df_data = pd.DataFrame(columns=head_columns)
    df_data = df_data[head_columns]
    return df_data


def outstandingExcel(request):
    if request.method == 'GET':
        employee_gid = request.GET['employee_gid']
        head_columns = ['S.No', 'Customer Name', 'Location', 'Invoice No', 'Invoice Date', 'Quantity', 'Bill Amount'
            , 'Due Amount', 'Due Days', '< 30', '30 - 45', '45 - 60', '60 - 75', '75 - 90', '90 - 120', '120 - 150',
                        '150 - 180', '> 180', 'Last pmt Date', 'Payment Amt', 'Aging Days','Employee Name']
        bhead_columns = ['S.No', 'Customer Name','Employee Name','Bill Amount'
            , 'Due Amount', '< 30', '30 - 45', '45 - 60', '60 - 75', '75 - 90', '90 - 120', '120 - 150',
                         '150 - 180', '> 180']
        df_data = getOutstandingDetails(employee_gid)
        df_group = df_data.groupby([head_columns[1],head_columns[21]])[
            [head_columns[6], head_columns[7], head_columns[9], head_columns[10]
                , head_columns[11], head_columns[12], head_columns[13], head_columns[14]
                , head_columns[15], head_columns[16], head_columns[17]]].sum()
        payment19 = df_data['Payment Amt'].sum()
        Due7 = df_data['Due Amount'].sum()
        greater30 = df_data['< 30'].sum()
        thiry = df_data['30 - 45'].sum()
        fourtyfive = df_data['45 - 60'].sum()
        sixty = df_data['60 - 75'].sum()
        seventyfive = df_data['75 - 90'].sum()
        ninty = df_data['90 - 120'].sum()
        one20 =df_data['120 - 150'].sum()
        one50 =df_data['150 - 180'].sum()
        greter180 = df_data['> 180'].sum()
        Bill6 = df_data['Bill Amount'].sum()
        # df_data = df_data.applymap(str)
        # df_group = df_data(head_columns[1]).aggregate({head_columns[6]: Total
        #                                                           , head_columns[7]: 'sum'
        #                                                           , head_columns[9]: 'sum', head_columns[10]: 'sum'
        #                                                           , head_columns[11]: 'sum', head_columns[12]: 'sum'
        #                                                           , head_columns[13]: 'sum', head_columns[14]: 'sum'
        #                                                           , head_columns[15]: 'sum', head_columns[16]: 'sum'
        #                                                           , head_columns[17]: 'sum', head_columns[18]: 'max'
        #                                                           , head_columns[19]: 'max', head_columns[20]: 'max'})
        df_group = df_group.reset_index()
        df_group.index = range(1, len(df_group) + 1)
        total_row_count = len(df_data.index) + 3
        column_count = len(df_data.columns) - 1
        btotal_row_count = len(df_group.index) + 3
        bcolumn_count = len(df_group.columns)
        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        writer.book = workbook
        df_data.to_excel(writer, sheet_name='OutstandingReport', startrow=3, startcol=0, index=False
                         , freeze_panes=(4, 0)
                         )
        df_group.to_excel(writer, sheet_name='Branchwise', startrow=3, startcol=0, index=True, index_label='S.No'
                          , freeze_panes=(4, 0))
        header = []
        tableheaderFormat = utility.tableHeader(workbook)
        for i in range(0, len(head_columns)):
            head = {'header': head_columns[i], 'header_format': tableheaderFormat}
            if (i == 5):
                head['total_string'] = 'Total'
            if (i == 6):
                head['total_string'] = str(Bill6)
            if (i == 7):
                head['total_string'] = str(Due7)
            if (i == 9):
                head['total_string'] = str(greater30)
            if (i == 10):
                head['total_string'] = str(thiry)
            if (i == 11):
                head['total_string'] = str(fourtyfive)
            if (i == 12):
                head['total_string'] = str(sixty)
            if (i == 13):
                head['total_string'] = str(seventyfive)
            if (i == 14):
                head['total_string'] = str(ninty)
            if (i == 15):
                head['total_string'] = str(one20)
            if (i == 16):
                head['total_string'] = str(one50)
            if (i == 17):
                head['total_string'] = str(greter180)
            if (i == 19):
                head['total_string'] = str(payment19)
            header.append(head)
        ws = writer.sheets['OutstandingReport']
        ws.add_table(3, 0, total_row_count + 1, column_count,
                     {'header_row': True, 'style': 'Table Style Light 2', 'banded_rows': 0, 'banded_columns': 0
                         , 'total_row': 1
                         , 'autofilter': True, 'columns': header})
        header_format = utility.headerFormat(workbook)
        subheader_format = utility.subHeaderFormat(workbook)
        ws.merge_range(0, 0, 0, column_count, 'VSOLV ENGINEERING INDIA PVT LTD', header_format)
        ws.merge_range(1, 0, 1, column_count, 'CUSTOMER OUTSTANDING REPORT', subheader_format)
        ws.merge_range(2, 0, 2, 3, 'Date: ' + datetime.datetime.today().strftime("%d/%m/%Y"),
                       subheader_format)

        if employee_gid != 0:
            header_text = request.GET['employee_name']
        if employee_gid == '0':
            header_text = 'ALL Employee'
        ws.merge_range(2, 4, 2, column_count, header_text, subheader_format)
        # ws.set_row(row=3, cell_format=tableHeader(workbook))
        number_format = utility.numberFormat(workbook)
        ws.set_column(6, 7, cell_format=number_format)
        ws.set_column(9, 17, cell_format=number_format)
        ws.set_column(19, 19, cell_format=number_format)

        # branchwise
        header = []
        for i in range(0, len(bhead_columns)):
            head = {'header': bhead_columns[i], 'header_format': tableheaderFormat}
            if (i == 2):
                head['total_string'] = 'Total'
            if (i == 3):
                head['total_string'] = str(Bill6)
            if (i == 4):
                head['total_string'] = str(Due7)
            if (i == 5):
                head['total_string'] = str(greater30)
            if (i == 6):
                head['total_string'] = str(thiry)
            if (i == 7):
                head['total_string'] = str(fourtyfive)
            if (i == 8):
                head['total_string'] = str(sixty)
            if (i == 9):
                head['total_string'] = str(seventyfive)
            if (i == 10):
                head['total_string'] = str(ninty)
            if (i == 11):
                head['total_string'] = str(one20)
            if (i == 12):
                head['total_string'] = str(one50)
            if (i == 13):
                head['total_string'] = str(greter180)
            header.append(head)
        ws = writer.sheets['Branchwise']
        ws.add_table(3, 0, btotal_row_count + 1, bcolumn_count,
                     {'header_row': True, 'style': 'Table Style Light 2', 'banded_rows': 0, 'banded_columns': 0
                         , 'total_row': 1
                         , 'autofilter': True, 'columns': header})
        ws.merge_range(0, 0, 0, bcolumn_count, 'VSOLV ENGINEERING INDIA PVT LTD', header_format)
        ws.merge_range(1, 0, 1, bcolumn_count
                       , 'CUSTOMER OUTSTANDING REPORT - Branchwise', subheader_format)
        ws.merge_range(2, 0, 2, 3, 'Date: ' + datetime.datetime.today().strftime("%d/%m/%Y"),
                       subheader_format)

        if employee_gid != 0:
            header_text = request.GET['employee_name']
        if employee_gid == '0':
            header_text = 'ALL Employee'
        ws.merge_range(2, 4, 2, bcolumn_count, header_text, subheader_format)
        # ws.set_column(3, 4, cell_format=number_format)
        ws.set_column(2, 2, cell_format=number_format)
        ws.set_column(11, 11, cell_format=number_format)
        ws.set_column(2, 10, cell_format=number_format)
        ws.set_column(12, 12, cell_format=number_format)
        # ws.set_column(19, 19, cell_format=number_format)
        writer.save()
        workbook.close()
        return getReponse(output, "Outstanding Report.xlsx")


def getReponse(ioStream, fileName):
    ioStream.seek(0)
    response = HttpResponse(ioStream.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=" + fileName
    ioStream.close()
    return response


def outstandingReportIndex(request):
    utility.sendFlashNotification("", "", ['dsfsdf', ])
    return render(request, "Overall_Report.html")


def querysummaryIndex(request):
    return  render(request,"Query_Summary.html")
