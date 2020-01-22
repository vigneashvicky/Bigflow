from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Bigflow.Master import views as MasterViews
from Bigflow.Master.Model import mMasters
from Bigflow.Transaction import views
from Bigflow.Transaction.Model import mFET, mSales
from Bigflow.Collection.Model import mCollection
from Bigflow.AP.model import mAP
from Bigflow.UserMgmt import views as UM_View
from Bigflow.Core import class1
from Bigflow.inward.model import mInvoice
import pandas as pd
from django.http import HttpResponse
from django.conf import settings
import Bigflow

mCore = Bigflow.mCore
import base64
from Bigflow.settings import BASE_DIR, MEDIA_URL
from rest_framework import authentication, permissions
import datetime


class login(APIView):

    def get(self, request):
        obj_login = mMasters.Masters
        jsondata = json.loads(request.body.decode('utf-8')).get('ls_json')

        user_name = jsondata.get('parms').get('username')
        user_password = jsondata.get('parms').get('password')

        out_message = mCore.get_login(user_name, user_password)
        return Response(out_message)

    def post(self, request):
        # jsondata = json.loads(request.body.decode('utf-8')).get('ls_json')
        jsondata = json.loads(request.body.decode('utf-8'))
        user_name = jsondata.get('username')
        user_password = jsondata.get('password')

        # serializer = loginSerializer(data=request.data)
        #
        #
        # if serializer.is_valid(raise_exception=True):
        #     new_data = serializer.data

        out_message = mCore.get_login(user_name, user_password)

        if out_message[1][0] == 'SUCCESS':
            ld_dict = {"DATA": out_message[0][0], "MESSAGE": out_message[1][0]}
        elif out_message[1][0] == 'FAIL':
            ld_dict = {"MESSAGE": out_message[1][0]}

        return Response(ld_dict)


class UM_RightsMenu(APIView):

    def get(self, request):
        obj_menu = class1.login
        obj_menu.employee_gid = self.request.query_params.get("emp_gid")
        obj_menu.char = self.request.query_params.get("Is_Mobile")
        # Validation
        out_message = class1.menulist(obj_menu.employee_gid, obj_menu.char)
        if out_message[1][0] == 'FOUND':
            ld_dict = {"DATA": out_message[0], "MESSAGE": out_message[1][0]}
        elif out_message[1][0] == 'NOT_FOUND':
            ld_dict = {"MESSAGE": out_message[1][0]}
        return Response(ld_dict)


class FET_Schedule(APIView):
    # Used to GET the Day's Schedule Data.
    def post(self, request):
        try:
            obj_schedule = mFET.FET_model()
            obj_schedule.employee_gid = self.request.query_params.get("emp_gid")
            obj_schedule.action = self.request.query_params.get("action")
            obj_schedule.date = self.request.query_params.get("date")
            obj_schedule.create_by = self.request.query_params.get("emp_gid")

            jsondata = json.loads(request.body.decode('utf-8'))

            obj_schedule.jsonData = json.dumps(jsondata.get("Classification"))

            ld_schedule = obj_schedule.get_preschedule_fet()
            json_data = ld_schedule.get("DATA").to_json(orient='records')

            if ld_schedule.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(json_data), "MESSAGE": "FOUND"}
            elif ld_schedule.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"DATA": json.loads(json_data), "MESSAGE": ld_schedule.get("MESSAGE")}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_schedule.get("MESSAGE")}
            return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class FET_ScheduleHistory(APIView):
    def get(self, request):
        try:
            obj_history = mFET.FET_model()
            obj_history.from_date = ''
            obj_history.to_date = ''
            obj_history.customer_gid = self.request.query_params.get("Customer_Gid")
            obj_history.employee_gid = self.request.query_params.get("Employee_Gid")
            obj_history.limit = self.request.query_params.get("Limit")
            obj_history.entity_gid = self.request.query_params.get("Entity_Gid")

            out_message = obj_history.get_schedule_view_fet()
            if out_message.empty == False:
                json_data = json.loads(out_message.to_json(orient='records'))
                return Response({"MESSAGE": "FOUND", "DATA": json_data})
            else:
                return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class FET_ReviewProcess(APIView):
    def post(self, request):
        global lst_outstanding
        try:
            if self.request.query_params.get("Group"):
                obj_sales = mFET.FET_model()
                obj_sales.schedule_gid = self.request.query_params.get("Schedule_Gid")
                obj_sales.entity_gid = self.request.query_params.get("Entity_Gid")
                # For Getting The Sale Details
                ld_out_data = obj_sales.get_schedule_review()
                if ld_out_data.get("MESSAGE") == 'FOUND':
                    lst_out_sales = json.loads(ld_out_data.get("DATA").to_json(orient='records'))
                    if len(lst_out_sales) > 0:
                        obj_sales.customer_gid = lst_out_sales[0].get("soheader_customer_gid")
                    else:
                        return Response({"MESSAGE": "NOT_FOUND"})
                        # Get The Outstanding Details.
                    obj_outstanding = mSales.Sales_Model()
                    jsondata = json.loads(request.body.decode('utf-8'))
                    obj_outstanding.type = 'OUTSTANDING_POSITION'
                    obj_outstanding.sub_type = 'FET_REVIEW'
                    obj_outstanding.jsonData = json.dumps({"Customer_Gid": obj_sales.customer_gid})
                    obj_outstanding.json_classification = json.dumps(jsondata.get('Params').get("CLASSIFICATION"))
                    ld_out_outstanding = obj_outstanding.get_salesquery_summaryOutstanding()
                    if ld_out_outstanding.get("MESSAGE") == 'FOUND':
                        lst_outstanding = json.loads(ld_out_outstanding.get("DATA").to_json(orient='records'))
                    else:
                        return Response({"MESSAGE": "NOT_FOUND"})
                    ### get The Pending POD Details.
                    obj_outstanding.type = "SALES_FET"
                    obj_outstanding.sub_type = "PENDING_POD"
                    obj_outstanding.jsonData = json.dumps({"Customer_Gid": obj_sales.customer_gid})
                    obj_outstanding.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                    obj_outstanding.create_by = 0
                    ld_out_message = obj_outstanding.get_INV_Dispatch()
                    if ld_out_message.get("MESSAGE") == 'FOUND':
                        lst_pod = json.loads(ld_out_message.get("DATA").to_json(orient='records'))
                    else:
                        return Response({"MESSAGE": "NOT_FOUND"})
                    #### ALL Data.
                    ld_alldata = {"SALES_DATA": lst_out_sales, "OUTSTANDING_POSITION": lst_outstanding,
                                  "SALES_POD": lst_pod}

                    return Response({"MESSAGE": "FOUND", "DATA": ld_alldata})


                elif ld_out_data.get("MESSAGE") == 'NOT_FOUND':
                    return Response({"MESSAGE": "NOT_FOUND"})


        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class TEST(APIView):
    def post(self, request):
        try:
            taxdtl = views
            jsondata = json.loads(request.body.decode('utf-8'))
            request.session['Entity_gid'] = 1
            lj_sales_fav_pdct = taxdtl.sales_fav_product(request)
            test = lj_sales_fav_pdct.content
            return Response(json.loads(test))
        except:
            return Response({"MESSAGE": "ERROR_OCCURED"})


class FET_Customer_Filter(APIView):  # Client TO DO
    def get(self, request):
        try:
            obj_customer = views
            request.session['Entity_gid'] = self.request.query_params.get("Entity_gid")
            request.session['Emp_gid'] = int(self.request.query_params.get("Emp_gid"))
            request.session['date'] = self.request.query_params.get("date")
            lj_customer_filter = obj_customer.getCustomerFilterlist(request)
            lj_output = lj_customer_filter.content.decode('utf-8')
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(lj_output)})
        except Exception as e:
            return Response({"MESSAGE": "NOT_FOUND", "DATA": str(e)})


class Customer_Mapped(APIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        try:
            obj_customer = mFET.FET_model()
            obj_customer.action = self.request.query_params.get("action")
            obj_customer.employee_gid = self.request.query_params.get("emp_gid")
            obj_customer.entity_gid = self.request.query_params.get("Entity_gid")
            out_message = obj_customer.get_mapped_customer()
            if out_message.empty == False:
                jdata = out_message.to_json(orient='records')
                ld_cust = {"DATA": json.loads(jdata), "MESSAGE": "FOUND"}
            else:
                ld_cust = {"MESSAGE": "NOT_FOUND"}
            return Response(ld_cust)
        except:
            return Response({"MESSAGE": "ERROR_OCCURED"})


class FET_Schedule_Set(APIView):
    def post(self, request):
        try:
            obj_schedule = views
            request.session['Entity_gid'] = self.request.query_params.get("Entity_gid")
            request.session['Emp_gid'] = self.request.query_params.get("Emp_gid")
            lj_out_message = obj_schedule.add_schdle(request)

            out_message = json.loads(json.loads(json.dumps(lj_out_message.content.decode('utf-8'))))
            # Two Loads to Convert the Actual

            lscheck = out_message[0]

            if lscheck.isdigit() or lscheck == 'SUCCESS':
                return Response({"MESSAGE": "SUCCESS", "DATA": out_message})
            else:
                return Response({"MESSAGE": "FAIL", "DATA": out_message})

        except Exception as e:
            return Response({"MESSAGE": "Error Occured"})


class FET_Schedule_Update(APIView):
    def post(self, request):
        obj_schedule = mFET.FET_model()
        obj_schedule.action = self.request.query_params.get("Type")
        if obj_schedule.action == 'SCHEDULE':
            obj_schedule.type = obj_schedule.action
            obj_schedule.sub_type = self.request.query_params.get("Sub_Type")
            jsondata = json.loads(request.body.decode('utf-8')).get('PARMS').get('Schedule_Update')
            obj_schedule.customer_gid = jsondata.get('Cust_Gid')
            obj_schedule.employee_gid = jsondata.get('Emp_Gid')
            obj_schedule.schedule_name = jsondata.get('ScheduleType_Name')
            obj_schedule.followup_reason_gid = jsondata.get('FollowUpReason_Gid')
            obj_schedule.ls_followup_date = jsondata.get('FollowUp_Date')
            obj_schedule.schedule_ref_gid = jsondata.get('Ref_Gid')
            obj_schedule.create_by = jsondata.get('Create_By')
            obj_schedule.remark = jsondata.get('Remark')

            # Validations.
            if obj_schedule.schedule_ref_gid != 0 and obj_schedule.ls_followup_date != '':
                return Response(
                    {"MESSAGE": "Error", "DATA": "Incorrect Parameters,Can't Update Ref gid and Followup Date."})

            out_message = obj_schedule.set_schedule_update()

            if out_message[0] == 'SUCCESS':
                return Response({"MESSAGE": "SUCCESS"})
            else:
                return Response({"MESSAGE": "FAIL", "DATA": out_message})


class FET_SalesOrder(APIView):
    def post(self, request):
        try:
            obj_sales = views
            request.session['Entity_gid'] = self.request.query_params.get("Entity_gid")
            request.session['Emp_gid'] = self.request.query_params.get("Emp_gid")
            request.session['date'] = self.request.query_params.get("Date")
            lj_out_message = obj_sales.sales_order_set(request)
            lj_out_message = json.loads(lj_out_message.content.decode('utf-8'))

            if lj_out_message == 'SUCCESS' or lj_out_message.isdigit:
                return Response({"MESSAGE": "SUCCESS", "DATA": lj_out_message})
            else:
                return Response({"MESSAGE": "FAIL", "DATA": lj_out_message})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


# To Get the Sales Product from a Sales Summary
class FET_SalesOrder_Get(APIView):
    def get(self, request):
        try:
            obj_sales = mFET.FET_model()
            obj_sales.so_header_gid = self.request.query_params.get("SO_Header_gid")
            obj_sales.entity_gid = self.request.query_params.get(("Entity_gid"))
            obj_sales.action = self.request.query_params.get("Action")
            obj_sales.schedule_gid = 0
            ldf_sales = obj_sales.get_drctEdit()

            if ldf_sales.empty == False:

                lj_data = json.loads(ldf_sales.to_json(orient='records'))

                return Response({"MESSAGE": "FOUND", "DATA": lj_data})

            elif ldf_sales.empty == True:
                return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Product_Sales(APIView):
    def get(self, request):
        obj_product = mFET.FET_model()
        obj_product.name = self.request.query_params.get("Product_Name")
        obj_product.limit = self.request.query_params.get("Limit")
        ld_product = obj_product.get_product()
        if len(ld_product) != 0:
            ld_product = json.dumps(ld_product)
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(ld_product)})
        else:
            return Response({"MESSAGE": "NOT_FOUND", "DATA": ''})


class Product_Sales_Favourite(APIView):
    def get(self, request):
        obj_product = mFET.FET_model()
        obj_product.customer_gid = self.request.query_params.get("Customer_gid")
        obj_product.product_type = 1
        obj_product.entity_gid = self.request.query_params.get("Entity_gid")
        out_message = obj_product.get_sales_fav_product()
        if not out_message.empty:
            ldict = out_message.to_json(orient='records')
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(ldict)})
        else:
            return Response({"MESSAGE": "NOT_FOUND"})


class LatLong(APIView):
    def get(self, request):  #### Get Not Used
        obj_location = class1.login()
        obj_location.action = self.request.query_params.get("Action")
        if obj_location.action == "INSERT":
            obj_location.latlong_gid = 0
            obj_location.employee_gid = self.request.query_params.get("Emp_gid")
            obj_location.latitude = self.request.query_params.get("Latitude")
            obj_location.longitude = self.request.query_params.get("Londitude")
            obj_location.entity_gid = self.request.query_params.get("Entity_gid")
            obj_location.create_by = self.request.query_params.get("Emp_gid")
            out_message = obj_location.setposition()
            out_message = str(out_message[0])
            result = out_message.split(",")
            if result[1] == "SUCCESS":
                return Response({"MESSAGE": "SUCCESS"})
            else:
                return Response({"MESSAGE": "FAIL", "DATA": out_message})
        else:
            return Response({"MESSAGE": "FAIL", "DATA": "Incorrect Action Value."})

    def post(self, request):
        obj_location = class1.login()
        obj_location.action = self.request.query_params.get("Action")
        if obj_location.action == 'MULTIPLE_INSERT':
            obj_location.jsondata = json.loads(json.dumps(request.body.decode('utf-8')))
            out_message = obj_location.setposition()

            if out_message[0] == "SUCCESS":
                return Response({"MESSAGE": "SUCCESS"})
            else:
                return Response({"MESSAGE": "FAIL", "DATA": out_message})
        else:
            return Response({"MESSAGE": "FAIL", "DATA": "Incorrect Action Value."})


class Schedule_Master(APIView):
    def get(self, request):
        obj_Schedule = mFET.FET_model()
        obj_Schedule.action = self.request.query_params.get("Action")
        obj_Schedule.entity_gid = self.request.query_params.get("Entity_gid")
        if obj_Schedule.action == 'SCHEDULE_TYPE':
            ldf_Schedule_Type = obj_Schedule.get_schedule_type()
        elif obj_Schedule.action == 'FOLLOWUP_REASON':
            obj_Schedule.schedule_type_gid = self.request.query_params.get("Schedule_Type_gid")
            ldf_Schedule_Type = obj_Schedule.get_followup_reason_fet()
        else:
            return Response({"MESSAGE": "NOT_FOUND", "DATA": "Incorrect Action Value."})

        return Response({"MESSAGE": "FOUND", "DATA": json.loads(ldf_Schedule_Type.to_json(orient='records'))})


class Employee_Profile(APIView):
    def get(self, request):
        obj_Employee = mMasters.Masters()
        obj_Employee.entity_gid = self.request.query_params.get("Entity_gid")
        obj_Employee.cluster = self.request.query_params.get("Action")
        obj_Employee.employee_gid = self.request.query_params.get("Emp_gid")
        obj_Employee.jsonData = json.dumps({"entity_gid": [obj_Employee.entity_gid], "client_gid": []})
        if obj_Employee.cluster == "EMPLOYEE_EDIT":
            Out_Message = obj_Employee.get_employee()
            if Out_Message.empty == False:
                return Response({"MESSAGE": "FOUND", "DATA": json.loads(Out_Message.to_json(orient='records'))})
            else:
                return Response({"MESSAGE": "NOT_FOUND"})
        elif obj_Employee.cluster == 'HIERARCHY':
            # obj_Employee.cluster = 'Y'
            Out_Message = obj_Employee.get_employee()
            if Out_Message.empty == False:
                return Response({"MESSAGE": "FOUND", "DATA": json.loads(Out_Message.to_json(orient='records'))})
            else:
                return Response({"MESSAGE": "NOT_FOUND"})
        elif obj_Employee.cluster == 'EMP_MAP_CLUSTER_SUPERVISOR':
            obj_Employee.cluster_gid = self.request.query_params.get("Cluster_Gid")
            obj_Employee.entity_gid = self.request.query_params.get("Entity_gid")
            Out_Message = obj_Employee.get_employee()
            if Out_Message.empty == False:
                return Response({"MESSAGE": "FOUND", "DATA": json.loads(Out_Message.to_json(orient='records'))})
            else:
                return Response({"MESSAGE": "NOT_FOUND"})

        else:
            return Response({"MESSAGE": "NOT_FOUND", "DATA": "Incorrect Action Value."})


class ScheduleCustomerFET(APIView):
    def post(self, request):
        try:
            obj_Schedule = mFET.FET_model()
            obj_Schedule.action = self.request.query_params.get("Type")
            obj_Schedule.type = self.request.query_params.get("Sub_Type")
            obj_Schedule.json1 = json.loads(request.body.decode('utf-8')).get('Params').get('FILTER')
            obj_Schedule.jsondata = json.dumps(obj_Schedule.json1)
            obj_Schedule.json2 = json.loads(request.body.decode('utf-8')).get('Params').get('CLASSIFICATION')
            obj_Schedule.json_classification = json.dumps(obj_Schedule.json2)
            ld_schedule_Cust = obj_Schedule.get_schedule_customer()

            json_data = ld_schedule_Cust.get("DATA").to_json(orient='records')

            lj_data = json.loads(json_data)

            if ld_schedule_Cust.get("MESSAGE") == 'FOUND':
                ll_Schedule = json.loads(lj_data[0].get("ScheudleTask"))
                ll_NonSchedule = json.loads(lj_data[0].get("Non_ScheduleTask"))
                ll_Sales_Detail = json.loads(lj_data[0].get("Sales_Details"))
                ll_Service = json.loads(lj_data[0].get("Service"))

                # Checking Empty. Starts
                # if empty send empty list.
                if ll_Schedule[0].get('ScheduleType_Name') is None or ll_Schedule[0].get('ScheduleType_Name') == '':
                    ll_Schedule = []
                if ll_NonSchedule[0].get('ScheduleType_Name') is None or ll_NonSchedule[0].get(
                        'ScheduleType_Name') == '':
                    ll_NonSchedule = []
                if ll_Sales_Detail[0].get('SO_NO') is None or ll_Sales_Detail[0].get('SO_NO') == '':
                    ll_Sales_Detail = []
                if ll_Service[0].get('Service_Code') is None or ll_Service[0].get('Service_Code') == '':
                    ll_Service = []
                ### Checking Empty Ends

                ld_dict = {"DATA": {"ScheudleTask": ll_Schedule, "Non_ScheduleTask": ll_NonSchedule,
                                    "Sales_Details": ll_Sales_Detail, "Service": ll_Service
                                    }, "MESSAGE": "FOUND"}

            elif ld_schedule_Cust.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"DATA": json.loads(json_data), "MESSAGE": ld_schedule_Cust.get("MESSAGE")}
            else:
                ld_dict = {"MESSAGE": 'Error Occured.' + ld_schedule_Cust.get("MESSAGE")}
            return Response(ld_dict)

        except Exception as e:
            return Response({"MESSAGE": e})


class Change_Password(APIView):
    def post(self, request):
        try:
            obj_UM = UM_View
            obj_UM.action = self.request.query_params.get("Type")
            # obj_UM.jsondata = json.loads(json.dumps(request.body.decode('utf-8')))
            if obj_UM.action == 'PROFILE_EMPCHANGE_PASSWORD':
                out_message = obj_UM.Password_verifiy(request)
            else:
                return Response({"MESSAGE": "In Correct Type Supplied"})

            out_message = json.loads(out_message.content.decode('utf-8'))
            return Response({"MESSAGE": out_message})

        except Exception as e:
            return Response({"MESSAGE": e})


class Get_position(APIView):
    def get(self, request):
        try:
            obj_poisionget = mCore.login()
            obj_poisionget.action = self.request.query_params.get("Action")
            obj_poisionget.employee_gid = self.request.query_params.get("Emp_gid")
            obj_poisionget.from_date = self.request.query_params.get("From_Date")
            if self.request.query_params.get("To_Date") == '' or self.request.query_params.get("To_Date") is None:
                obj_poisionget.to_date = ''
            else:
                # obj_poisionget.to_date = Bigflow.common.convertDate(self.request.query_params.get("To_Date"))
                obj_poisionget.to_date = self.request.query_params.get("To_Date")

            obj_poisionget.entity_gid = self.request.query_params.get("Entity_gid")
            df_position = obj_poisionget.getposition()
            if not df_position.empty:
                ldict = df_position.to_json(orient='records')
                return Response({"MESSAGE": "FOUND", "DATA": json.loads(ldict)})
            else:
                return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE": e})


class FileUpload(APIView):
    # parser_classes = (FileUploadParser,)
    ### POC ::KEEP it as Reference
    def post(self, request):

        jsondata = json.loads(request.body.decode('utf-8'))

        file_list = jsondata.get('File')

        if len(file_list) != 0:
            for i in range(len(file_list)):
                file_json = file_list[i]

                file_data = file_json.get('File_Base64data')

                file_data = base64.b64decode(file_data)
                file_name = file_json.get('File_Name')
                file_extension = file_json.get('File_Extension')

                file_name_new = file_name + str(datetime.datetime.now().strftime("%Y-%m-%d:%H:%M:%S"))

                # open(BASE_DIR + '/Bigflow/media/' + file_name + file_extension, 'wb')
                lsfile_name = str((BASE_DIR + '/Bigflow/media/' + file_name_new + file_extension))

                with open(lsfile_name, 'wb') as f:
                    f.write(file_data)

        return Response("Success")


from pathlib import Path


# from datetime import datetime
def File_Upload(file_list, dir_folder, emp_id):
    file_list = json.loads(file_list)

    if len(file_list) != 0:
        lst_saved_file_list = []
        for i in range(len(file_list)):
            file_json = file_list[i]

            file_data = file_json.get('File_Base64data')
            file_data = base64.b64decode(file_data)
            file_name = file_json.get('File_Name')
            file_extension = file_json.get('File_Extension')
            file_reftable_gid = file_json.get('Ref_Table_Gid')

            file_name_new = emp_id + '_' + str(datetime.datetime.now().strftime("%y%m%d_%H%M%S"))

            current_month = datetime.datetime.now().strftime('%m')
            current_day = datetime.datetime.now().strftime('%d')
            current_year_full = datetime.datetime.now().strftime('%Y')
            # /media/  is the MEDIA_URL

            lsfile_name = str((BASE_DIR + '/Bigflow' + "/media/" + dir_folder + '/'
                               + str(current_year_full) + '/' + str(current_month) + '/' + str(current_day) + '/' +
                               file_name_new + '.' + file_extension))

            ### Added Newly
            lsfile_name_db = str((MEDIA_URL + dir_folder + '/'
                                  + str(current_year_full) + '/' + str(current_month) + '/' + str(current_day) + '/' +
                                  file_name_new + '.' + file_extension))

            path = Path(lsfile_name)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(lsfile_name, 'wb') as f:
                f.write(file_data)

                if file_reftable_gid == None:
                    file_reftable_gid = 0
                else:
                    file_reftable_gid = file_reftable_gid

                ld_saved_file = {"SavedFilePath": lsfile_name_db, "File_Name": file_name,
                                 "RefTable_Gid": file_reftable_gid}
                lst_saved_file_list.append(ld_saved_file)

        return lst_saved_file_list  ### Wip for Multiple Files




def File_Uploadforscan(file_list, dir_folder, employee_gid):
    file_list = json.loads(file_list)
    if len(file_list) != 0:
        lst_saved_file_list = []
        for i in range(len(file_list)):
            file_json = file_list[i]
            file_data = file_json.get('File_Base64data')
            file_data = base64.b64decode(file_data)
            file_name = file_json.get('File_Name')
            file_extension = file_json.get('File_Extension')
            file_reftable_gid = file_json.get('Ref_Table_Gid')
            file_name_new = file_name
            current_month = datetime.datetime.now().strftime('%m')
            current_day = datetime.datetime.now().strftime('%d')
            current_year_full = datetime.datetime.now().strftime('%Y')
            # /media/  is the MEDIA_URL
            # f = (settings.MEDIA_ROOT) + '/INWARD/dummy/'
            lsfile_name = str((settings.MEDIA_ROOT) + '/INWARD/' + str(current_year_full) + '/' + str(
                current_month) + '/' + str(current_day) + '/' + employee_gid +'/'+ 'Tempinward/'+ file_name_new + '.' + file_extension)
            # lsfile_name = str(f+file_name + '.'  + file_name_new )
            ### Added Newly
            lsfile_name_db =str((settings.MEDIA_ROOT) + '/INWARD/' + str(current_year_full) + '/' + str(
                current_month) + '/' + str(current_day) + '/' + employee_gid +'/'+ file_name_new + '.' + file_extension)
            path = Path(lsfile_name)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(lsfile_name, 'wb') as f:
                f.write(file_data)

                if file_reftable_gid == None:
                    file_reftable_gid = 0
                else:
                    file_reftable_gid = file_reftable_gid

                ld_saved_file = {"SavedFilePath": lsfile_name_db, "File_Name": file_name,
                                 "RefTable_Gid": file_reftable_gid}
                lst_saved_file_list.append(ld_saved_file)
                return HttpResponse("data:{MESSAGE:SUCCESS1222}")
### Wip for Multiple Files


class Stock_GetAPI(APIView):

    def post(self, request):
        request.session['Entity_gid'] = self.request.query_params.get("Entity_gid")
        request.session['Emp_gid'] = self.request.query_params.get("Emp_gid")
        Object_Stockget = views.stockget(request)

        out_put = json.loads(Object_Stockget.content.decode('utf-8'))
        ## List Type as Output
        if len(out_put) > 0:
            return Response({"MESSAGE": "FOUND", "DATA": out_put})
        else:
            return Response({"MESSAGE": "NOT_FOUND"})


class Stock_SetAPI(APIView):
    def post(self, request):
        request.session['Emp_gid'] = self.request.query_params.get("Emp_Gid")
        out_message = views.stockset(request)
        out_message = json.loads(out_message.content.decode('utf-8'))
        return Response({"MESSAGE": out_message})


# class Customer_view_get(APIView):
#     def post(self,request):
#         jsondata = json.loads(request.body.decode('utf-8')).get('parms')
#         Action = jsondata.get('ACTION')
#         request.session['Entity_gid'] = self.request.query_params.get("Entity_gid")
#         #request.session['Emp_gid'] = self.request.query_params.get("Emp_gid")
#         if Action == 'Common':
#             object_viewdetail = mFET.FET_model()
#             object_viewdetail.customer_gid = jsondata.get('customer_gid')
#             object_viewdetail.employee_gid = jsondata.get('emp_gid')
#             object_viewdetail.action = jsondata.get('Outstanding_Group')
#             object_viewdetail.from_date = ""
#             object_viewdetail.to_date = ""
#             object_viewdetail.limit = self.request.query_params.get("Limit")
#             outstanding_detail = object_viewdetail.get_FEToutstanding_fet() ### Sally Table
#             object_viewdetail.action = "Scheduleview"
#             collection_history = object_viewdetail.get_collection_history_fet() ### Sally table
#             object_viewdetail.employee_gid = 0
#             sales_history = object_viewdetail.get_sales_history_fet() ### Need To Change
#         if len(outstanding_detail) or len(collection_history) or len(sales_history) > 0:
#            return Response({ "MESSAGE": "FOUND",
#                          "outstanding_detail":json.loads(outstanding_detail.to_json(orient='records')),
#                          "sales_history":json.loads(sales_history.to_json(orient='records')),
#                          "collection_history": json.loads(collection_history.to_json(orient='records'))})
#         else:
#             return Response({"MESSAGE": "NOT_FOUND"})
#
class Customer_view_get(APIView):
    def post(self, request):
        jsondata = json.loads(request.body.decode('utf-8'))
        Action = jsondata.get('ACTION')
        request.session['Entity_gid'] = self.request.query_params.get("Entity_gid")
        # request.session['Emp_gid'] = self.request.query_params.get("Emp_gid")
        if Action == 'Common':
            object_viewdetail = mFET.FET_model()
            obj_collection = mCollection.Collection_model()
            ### For Outstanding
            obj_collection.type = jsondata.get('Outstanding_Type')
            obj_collection.sub_type = jsondata.get('Outstanding_SubType')
            obj_collection.filter_json = json.dumps(jsondata)
            obj_collection.Classification = json.dumps(jsondata.get('CLASSIFICATION'))
            outstanding_detail = obj_collection.get_OutstandingCustomer()

            #### For Sale
            object_viewdetail.customer_gid = jsondata.get('Customer_Gid')
            object_viewdetail.employee_gid = jsondata.get('Employee_Gid')
            object_viewdetail.from_date = ""
            object_viewdetail.to_date = ""
            object_viewdetail.entity_gid = request.session['Entity_gid']
            object_viewdetail.limit = self.request.query_params.get("Limit")
            sales_history = object_viewdetail.get_sales_history_fet()

            #### For Collection
            obj_collection.action = "COLLECTION"
            obj_collection.type = "SUMMARY"
            obj_collection.collectionheader_gid = 0
            obj_collection.name = ''
            obj_collection.date = ''
            obj_collection.jsonData = jsondata
            obj_collection.jsondata = jsondata.get('CLASSIFICATION')
            collection_history = obj_collection.get_collection_inv_map()

            ## For Get Hierarchy
            object_viewdetail.employee_gid = jsondata.get('Employee_Gid')
            object_viewdetail.group = 'CUSTOMER_OUTSTANDING_GROUP'
            object_viewdetail.create_by = jsondata.get('Employee_Gid')
            object_viewdetail.entity_gid = self.request.query_params.get("Entity_gid")

            lt_out_message = object_viewdetail.get_hierarchy()
            ls_hierarchy = lt_out_message[0]

            if ls_hierarchy == 'Y' or ls_hierarchy == 'N':
                ls_hierarchy = ls_hierarchy
            else:
                ls_hierarchy = 'N'

        if len(outstanding_detail) or len(collection_history) or len(sales_history) > 0:
            return Response({"MESSAGE": "FOUND",
                             "outstanding_detail": json.loads(outstanding_detail.to_json(orient='records')),
                             "sales_history": json.loads(sales_history.to_json(orient='records')),
                             "collection_history": json.loads(collection_history.to_json(orient='records')),
                             "outstanding_hierarchy": ls_hierarchy
                             })

        else:
            return Response({"MESSAGE": "NOT_FOUND"})


class Direct_Outcome_Summary(APIView):
    def post(self, request):
        try:
            obj_summary = views

            request.session['Emp_gid'] = self.request.query_params.get("Emp_Gid")
            request.session['Entity_gid'] = self.request.query_params.get("Entity_gid")
            out_message = obj_summary.pre_schedule_get(request)
            out_message = json.loads(out_message.content.decode('utf-8'))

            if len(out_message) > 0:
                return Response({"MESSAGE": "FOUND", "DATA": out_message})
            else:
                return Response({"MESSAGE": "NOT_FOUND"})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class FET_Approve(APIView):
    def post(self, request):
        try:
            obj_approve_sales = mSales.Sales_Model()
            obj_approve_sales.action = self.request.query_params.get("Action")

            obj_approve_leads = mFET.FET_model()
            if obj_approve_sales.action == 'PENDING':
                obj_approve_sales.date = self.request.query_params.get("Date")
                obj_approve_sales.customer_gid = self.request.query_params.get("Customer_Gid")
                obj_approve_sales.employee_gid = self.request.query_params.get("Emp_Gid")
                obj_approve_sales.limit = self.request.query_params.get("Limit")
                obj_approve_sales.jsonData = json.loads(request.body.decode('utf-8')).get('Classification')
                obj_approve_sales.jsondata = '{}'

                obj_approve_sales.jsonData = json.dumps(obj_approve_sales.jsonData)

                obj_approve_leads.action = self.request.query_params.get("Action")
                obj_approve_leads.leadref_gid = 0
                obj_approve_leads.leadref_name = ''
                obj_approve_leads.status = obj_approve_sales.action  # PENDING
                obj_approve_leads.mobile_no = ''
                obj_approve_leads.entity_gid = self.request.query_params.get("Entity_Gid")

                dfout_message_sales = obj_approve_sales.get_sales_order()
                dfout_message_leads = obj_approve_leads.get_leadrequest()

                if not dfout_message_sales.empty or not dfout_message_leads.empty:

                    ldict_sales = dfout_message_sales.to_json(orient='records')

                    lst_sales = json.loads(ldict_sales)

                    for i in range(len(lst_sales)):
                        obj_sales = mMasters.Masters()

                        obj_sales.customer_gid = lst_sales[i].get("customer_gid")
                        obj_sales.soheader_gid = lst_sales[i].get("soheader_gid")
                        ## To Call the Model SALES.................................................
                        obj_sales.action = 'proposedbill'
                        obj_sales.type = ""
                        obj_sales.jsonData = {"customer_gid": obj_sales.customer_gid,
                                              "soheader_gid": obj_sales.soheader_gid}
                        obj_sales.jsonData = json.dumps(obj_sales.jsonData)
                        obj_sales.entity_gid = self.request.query_params.get("Entity_Gid")

                        df_salesdetails = obj_sales.getcreditapprv()

                        if not df_salesdetails.empty:
                            ldict_salesdetails = df_salesdetails.to_json(orient='records')
                            lst_sales[i].update({'Sale_Details': json.loads(ldict_salesdetails)})
                        else:
                            lst_sales[i].update({'Sale_Details': []})

                        ### To Call the Model Outstanding. ##############################
                        ### a) Customer Level
                        obj_outstanding = mCollection.Collection_model()
                        jsondata = json.loads(request.body.decode('utf-8'))
                        obj_outstanding.type = jsondata.get('Outstanding_Type')
                        obj_outstanding.sub_type = jsondata.get('Outstanding_SubType')
                        obj_outstanding.filter_json = json.dumps({"Customer_Gid": lst_sales[i].get("customer_gid")})
                        obj_outstanding.Classification = json.dumps(
                            json.loads(request.body.decode('utf-8')).get('Classification'))
                        df_outstanding_details = obj_outstanding.get_OutstandingCustomer()

                        ### b) Customer Group Level
                        obj_outstanding.filter_json = json.dumps(
                            {"Outstanding_Customer_Group_Gid": lst_sales[i].get("customer_custgroup_gid")})
                        df_outstanding_details_cust_group = obj_outstanding.get_OutstandingCustomer()
                        ## a) Customer Level Data
                        if not df_outstanding_details.empty:
                            ldict_outstandingdetails = df_outstanding_details.to_json(orient='records')
                            lst_sales[i].update({'Outstanding_Details': json.loads(ldict_outstandingdetails)})
                        else:
                            lst_sales[i].update({'Outstanding_Details': []})

                        ## a) Customer Group Level Data
                        if not df_outstanding_details_cust_group.empty:
                            ldict_outstandingdetails_group = df_outstanding_details_cust_group.to_json(orient='records')
                            lst_sales[i].update(
                                {'Outstanding_Details_Group': json.loads(ldict_outstandingdetails_group)})
                        else:
                            lst_sales[i].update({'Outstanding_Details_Group': []})

                        ### To Call the Model PDC Details.

                        obj_pending_collection = mCollection.Collection_model()

                        obj_pending_collection.action = "COLLECTION_INHAND"
                        obj_pending_collection.type = "PENDING"
                        obj_pending_collection.collectionheader_gid = 0
                        obj_pending_collection.name = ''
                        obj_pending_collection.date = ''
                        obj_pending_collection.jsonData = {"Customer_Gid": lst_sales[i].get("customer_gid")}
                        obj_pending_collection.jsondata = json.loads(request.body.decode('utf-8')).get('Classification')
                        df_pending_collection = obj_pending_collection.get_collection_inv_map()

                        if not df_pending_collection.empty:
                            ldict_pending_collection = df_pending_collection.to_json(orient='records')
                            lst_sales[i].update({'PDC_Pending': json.loads(ldict_pending_collection)})
                        else:
                            lst_sales[i].update({'PDC_Pending': []})

                    ldict_leads = dfout_message_leads.to_json(orient='records')

                    return Response(
                        {"MESSAGE": "FOUND", "DATA": {"SALES": lst_sales, "LEADS": json.loads(ldict_leads)}})

                else:
                    return Response({"MESSAGE": "NOT_FOUND"})
            elif obj_approve_sales.action == 'SALES_DATA':

                obj_approve_sales = views
                request.session['Emp_gid'] = self.request.query_params.get("Emp_Gid")
                request.session['Entity_gid'] = self.request.query_params.get("Entity_Gid")

                if request.session['Emp_gid'] == None or request.session['Emp_gid'] == '':
                    return Response({"MESSAGE": "ERROR_OCCURED", "DATA": "Emp Gid Is Needed"})

                if request.session['Entity_gid'] == None or request.session['Entity_gid'] == '':
                    return Response({"MESSAGE":"ERROR_OCCURED","DATA":"Entity Gid Is Needed"})

                out_message = obj_approve_sales.sale_approval(request)
                out_message = json.loads(out_message.content.decode('utf-8'))

                if out_message == 'SUCCESS':
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL", "DATA": str(out_message)})
            else:
                return Response({"MESSAGE": "ERROR_OCCURED", "DATA": "Incorrect Action"})



        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class FET_Review(APIView):  ### Approve and Not Approve
    def post(self, request):
        try:
            obj_fetreview = mFET.FET_model()
            obj_fetreview.action = self.request.query_params.get("Action")
            obj_fetreview.jsonData = json.loads(request.body.decode('utf-8')).get('Filter')
            obj_fetreview.jsondata = json.loads(request.body.decode('utf-8')).get('Classification')
            obj_fetreview.jsonData = json.dumps(obj_fetreview.jsonData)
            obj_fetreview.jsondata = json.dumps(obj_fetreview.jsondata)
            dfout_message = obj_fetreview.get_empvsSchedule()

            if not dfout_message.empty:
                if obj_fetreview.action == 'SCHEDULE_SNAPSHOT':
                    dfout_message['lj_data'] = dfout_message['lj_data'].apply(json.loads)
                ldict = dfout_message.to_json(orient='records')
                return Response({"MESSAGE": "FOUND", "DATA": json.loads(ldict)})
            else:
                return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

    def get(self, request):
        if request.method == 'GET':
            data = {}
            obj_empvsschedule = mFET.FET_model()
            if (self.request.query_params.get('localaction') == 'noexcel'):
                obj_empvsschedule.action = self.request.query_params.get('action')
                if self.request.query_params.get('emp_gid') == '0':
                    data['employee_gid'] = self.request.query_params.get('login_emp_gid')
                else:
                    data['employee_gid'] = self.request.query_params.get('emp_gid')
                if (self.request.query_params.get('f_date') != ''):
                    data['fromdate'] = self.request.query_params.get('f_date')
                if (self.request.query_params.get('t_date') != ''):
                    data['todate'] = self.request.query_params.get('t_date')
                if (self.request.query_params.get('fu_f_date') != ''):
                    data['followUp_fromdate'] = self.request.query_params.get('fu_f_date')
                if (self.request.query_params.get('fu_t_date') != ''):
                    data['followUp_todate'] = self.request.query_params.get('fu_t_date')
                if (self.request.query_params.get('rs_f_date') != ''):
                    data['reschedule_fromdate'] = self.request.query_params.get('rs_f_date')
                if (self.request.query_params.get('rs_t_date') != ''):
                    data['reschedule_todate'] = self.request.query_params.get('rs_t_date')
                data['customer_gid'] = self.request.query_params.get('cus_gid')
                data['scheduletype_gid'] = self.request.query_params.get('type_gid')
                data['customergroup_gid'] = self.request.query_params.get('custgrp')
                data['location_gid'] = self.request.query_params.get('loc_gid')
                data['login_emp_gid'] = self.request.query_params.get('login_emp_gid')
                data['Hierarchy_checked'] = self.request.query_params.get('chckd')
                obj_empvsschedule.jsonData = json.dumps(data)
                obj_empvsschedule.jsondata = json.dumps(
                    {"entity_gid": [self.request.query_params.get('entity_gid')],
                     "client_gid": [self.request.query_params.get('Cname')]})
                df_preschedule = obj_empvsschedule.get_empvsSchedule()
                # df_preschedule['login_gid'] = request.session['Emp_gid']
                jdata = df_preschedule.to_json(orient='records')
                return Response({"MESSAGE": "FOUND", "DATA": json.loads(jdata)})
            else:
                obj_empvsschedule.action = self.request.query_params.get('action')
                if self.request.query_params.get('emp_gid') == '0':
                    data['employee_gid'] = self.request.query_params.get('login_emp_gid')
                else:
                    data['employee_gid'] = self.request.query_params.get('emp_gid')
                if (self.request.query_params.get('f_date') != ''):
                    data['fromdate'] = self.request.query_params.get('f_date')
                if (self.request.query_params.get('t_date') != ''):
                    data['todate'] = self.request.query_params.get('t_date')
                if (self.request.query_params.get('fu_f_date') != ''):
                    data['followUp_fromdate'] = self.request.query_params.get('fu_f_date')
                if (self.request.query_params.get('fu_t_date') != ''):
                    data['followUp_todate'] = self.request.query_params.get('fu_t_date')
                if (self.request.query_params.get('rs_f_date') != ''):
                    data['reschedule_fromdate'] = self.request.query_params.get('rs_f_date')
                if (self.request.query_params.get('rs_t_date') != ''):
                    data['reschedule_todate'] = self.request.query_params.get('rs_t_date')
                data['customer_gid'] = self.request.query_params.get('cus_gid')
                data['scheduletype_gid'] = self.request.query_params.get('type_gid')
                data['customergroup_gid'] = self.request.query_params.get('custgrp')
                data['location_gid'] = self.request.query_params.get('loc_gid')
                data['login_emp_gid'] = self.request.query_params.get('login_emp_gid')
                obj_empvsschedule.jsonData = json.dumps(data)
                obj_empvsschedule.jsondata = json.dumps(
                    {"entity_gid": [self.request.query_params.get('entity_gid')],
                     "client_gid": [self.request.query_params.get('Cname')]})
                XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(content_type=XLSX_MIME)
                response['Content-Disposition'] = 'attachment; filename="FET Review Excel.xlsx"'
                writer = pd.ExcelWriter(response, engine='xlsxwriter')
                df_view = obj_empvsschedule.get_empvsSchedule()
                df_view.index = range(1, len(df_view) + 1)
                df_data = df_view[
                    ['employee_name', 'customer_name', 'schdate', 'scheduletype_name', 'schedule_status',
                     'followupreason_name', 'schedule_followup_date', 'schedule_reschedule_date',
                     'schedulereview_remarks',
                     'schedulereview_reviewstatus']]
                df_data.to_excel(writer, sheet_name='FET Review', index_label='SL NO', startrow=1, startcol=2,
                                 freeze_panes=(2, 0),
                                 header=['Employee Name', 'Customer Name', 'Date', 'Type', 'Status', 'Complete For',
                                         'Followup Date', 'Re-Schedule Date', 'Status Remark', 'Status'])
                writer.save()
                return response


### Common Classes.
class Comment(APIView):  ### Both Comment Set and Get.
    def post(self, request):
        try:
            obj_comment = MasterViews
            action = self.request.query_params.get("Action")
            request.session['Entity_gid'] = self.request.query_params.get("Entity_Gid")
            request.session['Emp_gid'] = self.request.query_params.get("Emp_Gid")
            if action == 'INSERT':
                ### Insert - Save the Record.
                out_message = obj_comment.commentset(request)
                out_message = json.loads(out_message.content.decode('utf-8'))
                if out_message == 'SUCCESS':
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL", "DATA": str(out_message)})

            elif action == 'FETCH':
                ljout_message = obj_comment.commentget(request)
                lj_output = ljout_message.content.decode('utf-8')
                lj_output = json.loads(lj_output)

                if len(lj_output) > 0:
                    return Response({"MESSAGE": "FOUND", "DATA": lj_output})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})
            else:
                return Response({"MESSAGE": "FAIL", "DATA": "Incorrect Action Value."})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class DeviceDetails(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Action") == "DEVICEDETAILS_SET":

                obj_device = mMasters.Masters();
                obj_device.action = self.request.query_params.get("Action")
                obj_device.entity_gid = self.request.query_params.get("Entity_Gid")
                obj_device.employee_gid = self.request.query_params.get("Emp_Gid")
                obj_device.create_by = self.request.query_params.get("Emp_Gid")
                obj_device.jsonData = json.loads(request.body.decode('utf-8'))

                out_message = obj_device.set_ip()

                if out_message[0] == 'SUCCESS':
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL", "DATA": str(out_message)})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class FET_ReviewApprove(APIView):  # Pending
    def post(self, request):
        approvedtl = views
        request.session['Entity_gid'] = self.request.query_params.get("Entity_Gid")
        request.session['Emp_gid'] = self.request.query_params.get("Emp_Gid")
        approveset = approvedtl.setschedule_review(request)
        return Response({"MESSAGE": json.loads(approveset.content.decode('utf-8'))})


class FET_Version(APIView):
    def get(self, request):
        obj_Version = mMasters.Masters()
        obj_Version.entity_gid = self.request.query_params.get("Entity_gid")
        obj_Version.action = self.request.query_params.get("Action")
        obj_Version.version_flag = self.request.query_params.get("Version_flag")
        Out_Message = obj_Version.get_Version()
        if Out_Message.empty == False:
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(Out_Message.to_json(orient='records'))})
        else:
            return Response({"MESSAGE": "NOT_FOUND"})


class Login_Get(APIView):
    def post(self, request):
        obj_Login = mMasters.Masters()
        obj_Login.entity_gid = self.request.query_params.get("Entity_gid")
        obj_Login.action = self.request.query_params.get("Action")
        obj_Login.type = self.request.query_params.get("Type")
        obj_Login.jsondata = json.loads(request.body.decode('utf-8'))
        Out_Message = obj_Login.get_Logindetail()
        if Out_Message.empty == False:
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(Out_Message.to_json(orient='records'))})
        else:
            return Response({"MESSAGE": "NOT_FOUND"})


# SALES

class sales_planning_Set(APIView):
    def post(self, request):
        try:
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_sales = mSales.Sales_Model()
            obj_sales.action = self.request.query_params.get("action")
            obj_sales.type = self.request.query_params.get("type")
            obj_sales.header = json.dumps(jsondata.get('parms').get('header'))
            obj_sales.detail = json.dumps(jsondata.get('parms').get('Details'))
            obj_sales.Classification = json.dumps(jsondata.get('parms').get('Classification'))
            obj_sales.sales = json.dumps(jsondata.get('parms').get('sales_sales'))
            request.session['Entity_gid'] = self.request.query_params.get("Entity_Gid")
            obj_sales.entity_gid = self.request.query_params.get("Entity_Gid")
            request.session['Emp_gid'] = self.request.query_params.get("Emp_Gid")
            plan = obj_sales.set_salesplanning()
            return Response({"MESSAGE": "FOUND", "DATA": plan[0]})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class sales_planning_Get(APIView):
    def post(self, request):
        try:
            obj_sales = mSales.Sales_Model()
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_sales.filter_json = json.dumps(jsondata.get('parms').get('filter'))
            obj_sales.Classification = json.dumps(jsondata.get('parms').get('classification'))
            obj_sales.type = self.request.query_params.get("type")
            obj_sales.customer_gid = self.request.query_params.get("cust_gid")
            obj_sales.year = self.request.query_params.get("year")
            obj_sales.product_type_gid = self.request.query_params.get("product_type_gid")
            obj_sales.product_gid = self.request.query_params.get("product_gid")
            obj_sales.employee_gid = self.request.query_params.get("Emp_Gid")
            plan_get = obj_sales.get_salesplanning()
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(plan_get.to_json(orient='records'))})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


# --------------check_in and check_out---------------#
class Check_In_Check_Out(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "EMPLOYEE_ACTIVITY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_employee = mFET.FET_model()
                obj_employee.action = self.request.query_params.get("Action")
                obj_employee.type = self.request.query_params.get("Type")
                obj_employee.jsonData = json.dumps(jsondata.get('Params').get('HEADER'))
                obj_employee.jsondata = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                obj_employee.create_by = self.request.query_params.get("Create_by")
                inv_out_message = obj_employee.set_check_in_check_out()
                if inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "SCHEDULED":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_employee = mFET.FET_model()
                obj_employee.action = self.request.query_params.get("Action")
                obj_employee.type = self.request.query_params.get("Type")
                obj_employee.jsonData = json.dumps(jsondata.get('Params').get('HEADER'))
                obj_employee.jsondata = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                obj_employee.create_by = self.request.query_params.get("Create_by")
                inv_out_message = obj_employee.set_check_in_check_out()
                if inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "GET_CHECKIN_CHECKOUT_DATA":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_employee = mFET.FET_model()
                obj_employee.action = self.request.query_params.get("Action")
                obj_employee.type = self.request.query_params.get("Type")
                obj_employee.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_employee.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_employee.get_check_in_check_out()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)


        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


# -------------------------------------------------------------------#

class sales_planningMIS(APIView):
    def get(self, request):
        try:
            object_sales = mSales.Sales_Model()
            object_sales.customer_gid = self.request.query_params.get("cust_gid")
            object_sales.from_date = self.request.query_params.get("fromyear")
            object_sales.to_date = self.request.query_params.get("toyear")
            object_sales.employee_gid = self.request.query_params.get("Emp_Gid")
            object_sales.product_gid = self.request.query_params.get("product_gid")
            object_sales.type = self.request.query_params.get("type")
            mis = object_sales.get_salesplanningmis()
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(mis.to_json(orient='records'))})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class sales_planning_history(APIView):
    def get(self, request):
        try:
            object_sales = mSales.Sales_Model()
            object_sales.from_date = self.request.query_params.get("fromdate")
            object_sales.to_date = self.request.query_params.get("todate")
            object_sales.customer_gid = self.request.query_params.get("cust_gid")
            object_sales.employee_gid = self.request.query_params.get("Emp_Gid")
            object_sales.entity_gid = self.request.query_params.get("entity_gid")
            object_sales.limit = self.request.query_params.get("limit")
            output = object_sales.get_salesplanning_historyget()
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(output.to_json(orient='records'))})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class sales_planning_Report(APIView):
    def get(self, request):
        try:
            object_sales = mSales.Sales_Model()
            object_sales.customer_gid = self.request.query_params.get("cust_gid")
            object_sales.from_date = self.request.query_params.get("fromyear")
            object_sales.to_date = self.request.query_params.get("toyear")
            object_sales.employee_gid = self.request.query_params.get("Emp_Gid")
            object_sales.product_gid = self.request.query_params.get("product_gid")
            object_sales.searchtype = self.request.query_params.get("searchtype")
            output = object_sales.get_salesplanning_reportget()
            return Response({"MESSAGE": "FOUND", "DATA": json.loads(output.to_json(orient='records'))})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


from Bigflow.Purchase.Model import mPurchase


class Purchase_request_API(APIView):
    def post(self, request):
        try:
            obj_prdata = mPurchase.Purchase_model()
            jsondata = json.loads(request.body.decode('utf-8'))
            prdetails = jsondata.get('params').get('prdetails')
            prheader_gid = prdetails[0].get('prheader_gid')
            #prdetail_details = jsondata.get('params').get('prdelete')
            # if prdetail_details != None:
            #     for x in prdetail_details:
            #         obj_prdata.prdetail_gid = x
            #         obj_prdata.Employee_gid = self.request.query_params.get("Employee_Gid")
            #         data = obj_prdata.set_prdelete()

            for y in prdetails:
                if prheader_gid == None:
                    obj_prdata.action = self.request.query_params.get("Action")
                    obj_prdata.date = datetime.datetime.now().strftime('%Y-%m-%d')
                    obj_prdata.Employee_gid = self.request.query_params.get("Employee_Gid")
                    obj_prdata.status = jsondata.get('params').get('status')
                    obj_prdata.branchcode = "1"
                    obj_prdata.mepnumber = ""
                    obj_prdata.totalamt = jsondata.get('params').get("pr_amt")
                    obj_prdata.commodity_gid = y.get('commdity_gid')
                    obj_prdata.entity_gid = self.request.query_params.get("entity_gid")
                    obj_prdata.create_by = self.request.query_params.get("Employee_Gid")
                    data = obj_prdata.set_prheader()[0].split(',')
                    if data != "Error":
                        # for x in prdetails:
                        obj_prdata.prheader_gid = data[0]
                        obj_prdata.product_gid = y.get('product_gid')
                        obj_prdata.product_qty = y.get('prdetails_qty')
                        obj_prdata.supplier_gid = "311"
                        # for local supplier gid =1 and for demo supplier gid=311
                        obj_prdata.Employee_gid = self.request.query_params.get("Employee_Gid")
                        obj_prdata.entity_gid = self.request.query_params.get("entity_gid")
                        data1 = obj_prdata.set_prdetails()[0].split(',')

                    # if obj_prdata.status == "Pending For Approval":
                    #     if data1[1] == "SUCCESS":
                    #         obj_prdata.action = 'Insert'
                    #         obj_prdata.ref_gid = 1
                    #         obj_prdata.reftable = obj_prdata.prheader_gid
                    #         obj_prdata.status = 'Pending For Approval'
                    #         obj_prdata.totype = 'I'
                    #         obj_prdata.to = 2
                    #         obj_prdata.remark = ''
                    #         tran = obj_prdata.set_trans()[0].split(',')
                    #         return Response({"MESSAGE": data1[1]})
                    #     else:
                        return Response({"MESSAGE": data1[1]})
                else:
                    obj_prdata.action = self.request.query_params.get("Action")
                    obj_prdata.prheader_gid = prheader_gid
                    obj_prdata.entity_gid = request.session['Entity_gid']
                    obj_prdata.create_by = request.session['Emp_gid']
                    data = obj_prdata.set_prheaderupdate()[0].split(',')
                    if data != "Error":
                        #for x in prdetails:
                        if y.get('prdetails_gid') == None:
                            obj_prdata.prheader_gid = prheader_gid
                            obj_prdata.product_gid = y.get('product_gid')
                            obj_prdata.product_qty = y.get('prdetails_qty')
                            obj_prdata.supplier_gid = "1"
                            obj_prdata.Employee_gid = self.request.query_params.get("Employee_Gid")
                            obj_prdata.entity_gid = self.request.query_params.get("entity_gid")
                            data1 = obj_prdata.set_prdetails()[0].split(',')
                            return Response({"MESSAGE": data1})
                        else:
                            obj_prdata.prdetail_gid = y.get('prdetails_gid')
                            obj_prdata.product_gid = y.get('product_gid')
                            obj_prdata.product_qty = y.get('prdetails_qty')
                            obj_prdata.supplier_gid = "1"
                            data1 = obj_prdata.set_prdetailupdate()[0].split(',')
                            return Response({"MESSAGE": data1})
                        #
                        # if obj_prdata.status == "Pending For Approval":
                        #     if data1[1] == "SUCCESS":
                        #         obj_prdata.action = 'Insert'
                        #         obj_prdata.ref_gid = 1
                        #         obj_prdata.reftable = obj_prdata.prheader_gid
                        #         obj_prdata.status = 'Pending For Approval'
                        #         obj_prdata.totype = 'I'
                        #         obj_prdata.to = 2
                        #         obj_prdata.remark = ''
                        #         tran = obj_prdata.set_trans()[0].split(',')
                        #
                        #         return Response({"MESSAGE": data1[1]})
                        #
                        #     else:
                        #         return Response({"MESSAGE": data})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


#### Scan and Save Files

class File_Save(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == 'SCAN_IMAGE_BARCODE':
                obj_file = mInvoice.inward_model
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_file.json_file = json.dumps(jsondata.get('Params').get('File'))
                obj_file.pdf_name = self.request.query_params.get("pdf_name")
                obj_file.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_file.entity = self.request.query_params.get("entity")
                file_list = json.loads(obj_file.json_file)
                if len(file_list) != 0:
                    lst_saved_file_list = []
                    for i in range(len(file_list)):
                        file_json = file_list[i]
                        file_data = file_json.get('File_Base64data')
                        file_data = base64.b64decode(file_data)
                        file_name = file_json.get('File_Name')
                        file_extension = file_json.get('File_Extension')
                        file_name_new = obj_file.employee_gid + '_' +file_name+ str(datetime.datetime.now().strftime("%y%m%d_%H%M%S"))
                        current_month = datetime.datetime.now().strftime('%m')
                        current_day = datetime.datetime.now().strftime('%d')
                        current_year_full = datetime.datetime.now().strftime('%Y')
                        # /media/  is the MEDIA_URL
                        lsfile_name = str((settings.MEDIA_ROOT) + '/INWARD/' + str(current_year_full) + '/' + str(
                            current_month) + '/' + str(current_day) + '/'+ file_name_new + '.' + file_extension)
                        lsfile_name_db = "/media/INWARD/"+str(current_year_full) + '/' + str(
                            current_month) + '/' + str(current_day) + '/'+ file_name_new + '.' + file_extension
                        path = Path(lsfile_name)
                        path.parent.mkdir(parents=True, exist_ok=True)
                        with open(lsfile_name, 'wb') as f:
                            f.write(file_data)
                            ld_saved_file = {"SavedFilePath": lsfile_name, "File_Name": file_name}
                            lst_saved_file_list.append(ld_saved_file)
                            inward_dtl = mAP.ap_model()
                            inward_dtl.action = 'UPDATE'
                            inward_dtl.type = 'FILE'
                            inward_dtl.header_json = {}
                            inward_dtl.debit_json = {}
                            inward_dtl.detail_json = {}
                            inward_dtl.status_json = {"Barcode_Name": file_name , "File_name":  lsfile_name_db  }
                            inward_dtl.entity_gid = obj_file.entity
                            inward_dtl.employee_gid = obj_file.employee_gid
                            # print(inward_dtl.status_json)
                            out = inward_dtl.set_Invoiceheader()[0].split(',')
            return out

                    # return lsfile_name_db  ### Wip for Multiple Files
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

# def File_Upload_Barcode(file_list, dir_folder, emp_id):
#         file_list = json.loads(file_list)
#         if len(file_list) != 0:
#             lst_saved_file_list = []
#             for i in range(len(file_list)):
#                 file_json = file_list[i]
#                 file_data = file_json.get('File_Base64data')
#                 file_data = base64.b64decode(file_data)
#                 file_name = file_json.get('File_Name')
#                 file_extension = file_json.get('File_Extension')
#                 file_name_new = emp_id + '_' + str(datetime.datetime.now().strftime("%y%m%d_%H%M%S"))
#                 current_month = datetime.datetime.now().strftime('%m')
#                 current_day = datetime.datetime.now().strftime('%d')
#                 current_year_full = datetime.datetime.now().strftime('%Y')
#                 # /media/  is the MEDIA_URL
#                 lsfile_name = str((BASE_DIR + '/Bigflow' + "/media/" + dir_folder + '/'
#                                    + str(current_year_full) + '/' + str(current_month) + '/' + str(
#                             current_day) + '/' +
#                                    file_name_new + '.' + file_extension))
#                 ### Added Newly
#                 lsfile_name_db = str((MEDIA_URL + dir_folder + '/'
#                                       + str(current_year_full) + '/' + str(current_month) + '/' + str(
#                             current_day) + '/' +
#                                       file_name_new + '.' + file_extension))
#                 path = Path(lsfile_name)
#                 path.parent.mkdir(parents=True, exist_ok=True)
#                 with open(lsfile_name, 'wb') as f:
#                     f.write(file_data)
#                     ld_saved_file = {"SavedFilePath": lsfile_name_db, "File_Name": file_name}
#                     lst_saved_file_list.append(ld_saved_file)
#                     # inward_dtl = mAP.ap_model()
#                     # inward_dtl.action = 'UPDATE'
#                     # inward_dtl.type = 'FILE'
#                     # inward_dtl.header_json = {}
#                     # inward_dtl.debit_json = {}
#                     # inward_dtl.detail_json = {}
#                     # inward_dtl.status_json = {"Barcode_Name": file_name , "File_name":  lsfile_name_db  }
#                     # inward_dtl.entity_gid = 1
#                     # inward_dtl.employee_gid = 1
#                     # print(inward_dtl.status_json)
#                     # out = inward_dtl.set_Invoiceheader()[0].split(',')
#             # return Response({"MESSAGE": out})
#
#             return lsfile_name_db  ### Wip for Multiple Files

class State_Process_Set(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Action") == "insert":
                pro_exp = mMasters.Masters()
                pro_exp.Action = self.request.query_params.get('Action')
                pro_exp.City = json.dumps(self.request.data)
                pro_exp.Entity_gid = self.request.query_params.get('Entity_gid')
                pro_exp.Emp_gid = self.request.query_params.get('Emp_gid')
                pro_results = pro_exp.set_citys()
                return Response(pro_results)
            elif self.request.query_params.get("Action") == "Insert":
                pro_exp = mMasters.Masters()
                pro_exp.Action = self.request.query_params.get('Action')
                pro_exp.Type = self.request.query_params.get('Type')
                pro_exp.filter=json.dumps(self.request.data.get('filter'))
                pro_exp.classification = json.dumps(self.request.data.get('classification'))
                pro_exp.Emp_gid = self.request.query_params.get('Emp_gid')
                pro_results = pro_exp.set_state()
                pro_results=pro_results[0]
                if pro_results=="SUCCESS":
                    return Response("SUCCESS")
                else:
                    return Response("FAIL")
                return Response(pro_results)

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})