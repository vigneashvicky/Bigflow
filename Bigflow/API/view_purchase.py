from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Bigflow.API import views as commonview
from Bigflow.Purchase.Model import mPurchase

class Delmat(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Type") == "pr_multi":
                # The First Page Summary Data
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mPurchase.Purchase_model()
                obj_ctrl.action = self.request.query_params.get("Action")
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.enty = self.request.query_params.get("Entity_Gid")
                obj_ctrl.crtby = self.request.query_params.get("Employee_Gid")
                obj_ctrl.array = json.dumps(jsondata)

                ld_out_message = obj_ctrl.set_delmatsave()

                if ld_out_message.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
            elif self.request.query_params.get("Action") == "get" or self.request.query_params.get(
                    "Action") == "get_po":
                # The First Page Summary Data
                obj_ctrl = mPurchase.Purchase_model()
                obj_ctrl.action = self.request.query_params.get("Action")
                obj_ctrl.enty = self.request.query_params.get("Entity_Gid")
                ld_out_message = obj_ctrl.set_delmatget()
                ld_dict = {"DATA": json.loads(ld_out_message.to_json(orient='records'))}
                return Response(ld_dict)
            elif self.request.query_params.get("Type") == "pr_update":
                # The First Page Summary Data
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mPurchase.Purchase_model()
                obj_ctrl.action = self.request.query_params.get("Action")
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.enty = self.request.query_params.get("Entity_Gid")
                obj_ctrl.crtby = self.request.query_params.get("Employee_Gid")
                obj_ctrl.array = json.dumps(jsondata)

                ld_out_message = obj_ctrl.set_delmatupdate()

                if ld_out_message.get("MESSAGE") == 'SUCCESSFULLY UPDATED':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif ld_out_message.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    dal=ld_out_message.get("MESSAGE")
                    dal=dal[14:].split('by')
                    status=dal[0]
                    emp=int(dal[1])

                    ld_dict = {"MESSAGE": 'Alredy Exist',"Status" :status,"Emp":emp}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE":"ERROR_OCCURED","DATA":str(e)})



class Alltable_ccbs(APIView):
    def post(self,request):
        try:
            if(request.method=='POST'):

                object_query = mPurchase.Purchase_model()
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query.action = self.request.query_params.get("Action")
                object_query.enty = self.request.query_params.get("Entity_Gid")
                # object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
                object_query.jdata = json.dumps(jsondata)
                ld_out_message = object_query.alltable_data()
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

class Agaentsmry(APIView):
    def post(self,request):
        try:
            if(request.method=='POST'):

                object_query = mPurchase.Purchase_model()
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query.action = self.request.query_params.get("Action")
                object_query.type = self.request.query_params.get("Type")
                # object_query.action = self.request.query_params.get("Action")
                object_query.enty = self.request.query_params.get("classification")
                # object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
                object_query.main = json.dumps(jsondata)
                ld_out_message = object_query.Agentsummary_Get()
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

class Grn_Details(APIView):
   def post(self,request):
       try:
           if(request.method=='POST'):
               object_query = mPurchase.Purchase_model()
               if(self.request.query_params.get("type") == 'GRN'):
                   object_query.type=self.request.query_params.get('type')
                   object_query.sub_type=self.request.query_params.get('sub_type')
                   object_query.filter_json=self.request.data
                   result=object_query.grndetails_get_()
                   json_data = json.loads(result.to_json(orient='records'))
                   return Response(json_data)
       except Exception as e:
           return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})