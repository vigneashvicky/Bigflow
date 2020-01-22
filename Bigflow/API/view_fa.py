from rest_framework.views import APIView
from rest_framework.views import Response
import json
from Bigflow.API import views as commonview
from Bigflow.FA.model import mFA
from Bigflow.Transaction.Model import mSales


class FAApi(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "FA_ASSERT_MAKER_SUMMARY":
                # Get The Data And Shown in Assert Maker Summary :: Pending Data.
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_fa.get_fa_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "FA_INVOICE_DETAILS":
                # Get The Data And Shown in Invoice Details Summary :: Asset Maker.
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_fa.get_fa_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "FA_ASSET_CHECKER_SUMMARY":
                # Get The Data And Shown in Asset Checker Summary. - using Group
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_fa.get_fa_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "FA_ASSET_TRAN_SUMMARY":
                # Get The Data And Shown in Asset ALL  Summary. -
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_fa.get_fa_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class FA_Asset_Make(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "FA_ASSET_MAKE":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_fa.json_file = json.dumps(jsondata.get('Params').get('File'))
                base64data = json.loads(obj_fa.json_file)
                ## Validate file Null
                if base64data[0] != []:
                    saved_filepath = commonview.File_Upload(obj_fa.json_file, 'FA', obj_fa.employee_gid)
                    obj_fa.json_file = json.dumps(saved_filepath)
                else:
                    obj_fa.json_file = '{}'
                obj_fa.jsonData = json.dumps(jsondata.get('Params').get('CHANGE'))
                obj_fa.jsonData_sec = json.dumps(jsondata.get('Params').get('STATUS'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_fa.set_fa_make()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "FA_ASSET_CHECKER":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_fa.jsonData = json.dumps(jsondata.get('Params').get('CHANGE'))
                obj_fa.jsonData_sec = json.dumps(jsondata.get('Params').get('STATUS'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_fa.set_fa_make()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class FA_Tran(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "FA_ASSET_TRAN":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_fa.jsonData = json.dumps(jsondata.get('Params').get('CHANGE'))
                obj_fa.jsonData_sec = json.dumps(jsondata.get('Params').get('STATUS'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_fa.set_fa_make()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "FA_ASSET_DEPRECIATION":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DEPRECIATION'))
                obj_fa.jsonData = json.dumps(jsondata.get('Params').get('CHANGE'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_fa.set_fa_depreciation()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class FA_Location(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "FA_LOCATION_GET":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_fa.get_fa_location()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "FA_LOCATION_SET":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_fa.set_fa_location()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class FA_Category(APIView):
    def post(self, request):
        try:
         if self.request.query_params.get("Group") == "FA_CATEGORY_SET":
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_fa = mFA.FaModel()
            obj_fa.action = self.request.query_params.get("Action")
            obj_fa.type = self.request.query_params.get("Type")
            obj_fa.sub_type = self.request.query_params.get("Sub_Type")
            obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
            obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
            obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
            ld_out_message = obj_fa.set_fa_category()
            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS"}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL"}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
         elif self.request.query_params.get("Group") == "FA_ASSET_CATEGORY":
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_fa = mFA.FaModel()
            obj_fa.type = self.request.query_params.get("Type")
            obj_fa.sub_type = self.request.query_params.get("Sub_Type")
            obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
            obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
            ld_out_message = obj_fa.get_fa_category()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                           "MESSAGE": 'FOUND'}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND'}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class FA_Sale(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "FA_SALE_SET":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.create_by = self.request.query_params.get("Employee_Gid")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.customer_gid = json.dumps(jsondata.get('Params').get('custid'))
                obj_fa.Channel = self.request.query_params.get('Channel')
                obj_fa.So_Header_date = self.request.query_params.get('So_Header_date')
                obj_fa.sodetails = json.dumps(jsondata.get('Params').get('SOdetails'))
                obj_fa.entity_gid = json.dumps(jsondata.get('Params').get('CLASSIFICATION').get('Entity_Gid'))
                ld_out_message = obj_fa.set_sales_order()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class FA_Depreciation(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "FA_ASSET_DEPRECIATION":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_fa = mFA.FaModel()
                obj_fa.action = self.request.query_params.get("Action")
                obj_fa.type = self.request.query_params.get("Type")
                obj_fa.sub_type = self.request.query_params.get("Sub_Type")
                obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
                obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DEPRECIATION'))
                obj_fa.jsonData = json.dumps(jsondata.get('Params').get('CHANGE'))
                obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_fa.set_fa_depreciation()
                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": "FAIL"}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class FinYear(APIView):
    def post(self, request):
        try:
         if self.request.query_params.get("Group") == "FIN_YEAR_SET":
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_fa = mFA.FaModel()
            obj_fa.action = self.request.query_params.get("Action")
            obj_fa.type = self.request.query_params.get("Type")
            obj_fa.sub_type = self.request.query_params.get("Sub_Type")
            obj_fa.employee_gid = self.request.query_params.get("Employee_Gid")
            obj_fa.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
            obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
            ld_out_message = obj_fa.set_fin_year()
            if ld_out_message.get("MESSAGE") == 'SUCCESS':
                ld_dict = {"MESSAGE": "SUCCESS"}
            elif ld_out_message.get("MESSAGE") == 'FAIL':
                ld_dict = {"MESSAGE": "FAIL"}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
         elif self.request.query_params.get("Group") == "FIN_YEAR_GET":
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_fa = mFA.FaModel()
            obj_fa.type = self.request.query_params.get("Type")
            obj_fa.sub_type = self.request.query_params.get("Sub_Type")
            obj_fa.filter_json = json.dumps(jsondata.get('Params').get('FILTER'))
            obj_fa.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
            ld_out_message = obj_fa.get_fin_year()
            if ld_out_message.get("MESSAGE") == 'FOUND':
                ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                           "MESSAGE": 'FOUND'}
            elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                ld_dict = {"MESSAGE": 'NOT_FOUND'}
            else:
                ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
            return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})