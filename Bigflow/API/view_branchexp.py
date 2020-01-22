from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Bigflow.BranchExp.model import mBranch


class Expense_Process(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group")== "EXPENSE_DATA":
                jsondata = json.loads(request.body.decode('utf-8'))
                exp_process= mBranch.BranchExp_model()
                exp_process.type=self.request.query_params.get("Type")
                exp_process.sub_type=self.request.query_params.get("SubType")
                exp_process.jsonData=json.dumps(jsondata.get('Params').get('FILTER'))
                exp_process.json_classification='{}'#json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                #exp_process.create_by=self.request.query_params.get("Create_by")
                #exp_process.is_commit = self.request.query_params.get("Is_Commit")
                inv_out_message=exp_process.get_expensedetails()
                if inv_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"MESSAGE": 'SUCCESS' ,"DATA":json.loads(inv_out_message.get("DATA").to_json(orient='records'))}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "INV_Process_Single_GET" :
                jsondata = json.loads(request.body.decode('utf-8'))
                exp_process = mBranch.BranchExp_model()
                exp_process.action = self.request.query_params.get("Action")
                exp_process.type = self.request.query_params.get("Type")
                exp_process.jsonData = json.dumps(jsondata.get('Params').get('HEADER'))
                exp_process.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                exp_process.json_rate = json.dumps(jsondata.get('Params').get('RATE'))
                exp_process.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                exp_process.create_by = self.request.query_params.get("Create_by")
                exp_process.is_commit = self.request.query_params.get("Is_Commit")
                inv_out_message = exp_process.get_expensedetails()
                if inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Expense_Process_Set(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group")== "EXPENSE_DATA":
                jsondata = json.loads(request.body.decode('utf-8'))
                exp_process= mBranch.BranchExp_model()
                exp_process.action=self.request.query_params.get("Action")
                exp_process.type=self.request.query_params.get("Type")
                exp_process.create_by=self.request.query_params.get("create_by")
                exp_process.jsonData=json.dumps(jsondata.get('Params').get('FILTER'))
                exp_process.json_classification=json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                #exp_process.create_by=self.request.query_params.get("Create_by")
                #exp_process.is_commit = self.request.query_params.get("Is_Commit")
                inv_out_message=exp_process.set_expensedetails()
                if inv_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"MESSAGE": 'SUCCESS' ,"DATA":json.loads(inv_out_message.get("DATA").to_json(orient='records'))}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "INV_Process_Single_GET" :
                jsondata = json.loads(request.body.decode('utf-8'))
                exp_process = mBranch.BranchExp_model()
                exp_process.action = self.request.query_params.get("Action")
                exp_process.type = self.request.query_params.get("Type")
                exp_process.jsonData = json.dumps(jsondata.get('Params').get('HEADER'))
                exp_process.jsondata = json.dumps(jsondata.get('Params').get('DETAILS'))
                exp_process.json_rate = json.dumps(jsondata.get('Params').get('RATE'))
                exp_process.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                exp_process.create_by = self.request.query_params.get("Create_by")
                exp_process.is_commit = self.request.query_params.get("Is_Commit")
                inv_out_message = exp_process.set_expensedetails()
                if inv_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif inv_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": inv_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + inv_out_message.get("MESSAGE")}
                return Response(ld_dict)

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Property_Process(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Type")=="PRODUCT":
                property_types=mBranch.BranchExp_model()
                property_types.type=self.request.query_params.get("Type")
                property_types.entity_gid=self.request.query_params.get("entity_gid")
                property_types.table_values=json.dumps(self.request.data)
                result =property_types.get_alltablevalue()
                json_data = json.loads(result.to_json(orient='records'))
                return Response(json_data)
            elif self.request.query_params.get("Type")=="PROPERTY":
                if self.request.query_params.get("Sub_Type")=="SUMMARY":
                    pro_det=mBranch.BranchExp_model()
                    pro_det.Type=self.request.query_params.get('Type')
                    pro_det.Sub_Type=self.request.query_params.get('Sub_Type')
                    pro_det.filter=json.dumps(self.request.data.get('filters'))
                    pro_det.classification=json.dumps(self.request.data.get('classification'))
                    pro_result=pro_det.get_pro_details()
                    if pro_result.empty== False:
                        json_data = json.loads(pro_result.to_json(orient='records'))
                        return Response({"MESSAGE": "FOUND", "DATA": json_data})
                    else:
                        return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Property_Process_Set(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Type") == "INSERT":
                if self.request.query_params.get("Sub_Type") == "property":
                    exp_process = mBranch.BranchExp_model()
                    exp_process.type = self.request.query_params.get("Type")
                    exp_process.sub_type = self.request.query_params.get("Sub_Type")
                    exp_process.filters = json.dumps(self.request.data.get("params").get("filters"))
                    exp_process.classification = json.dumps(self.request.data.get("params").get("classification"))
                    result = exp_process.property_set()
                    if result.get("MESSAGE") == "SUCCESS":
                        return Response("SUCCESS")
                    else:
                        return Response("FAIL")
            if self.request.query_params.get("Type") == "update":
                if self.request.query_params.get("Sub_Type") == "property":
                    exp_process = mBranch.BranchExp_model()
                    exp_process.type = self.request.query_params.get("Type")
                    exp_process.sub_type = self.request.query_params.get("Sub_Type")
                    exp_process.filters = json.dumps(self.request.data.get("params").get("filters"))
                    exp_process.classification = json.dumps(self.request.data.get("params").get("classification"))
                    result = exp_process.property_set()
                    if result.get("MESSAGE") == "SUCCESS":
                        return Response("SUCCESS")
                    else:
                        return Response("FAIL")

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})