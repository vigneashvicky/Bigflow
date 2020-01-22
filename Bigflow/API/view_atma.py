from rest_framework.views import APIView
from rest_framework.response import Response
import json
import Bigflow.Core.models as common

from Bigflow.ATMA.model import mATMA

### ATMA
class atmaCatalog_Setapi(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Catalog Details":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Classification'))
                out_message = obj_prodcat.atmaSet_Catalog()
                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message})

            if self.request.query_params.get("Group") == "Catalog_Details_Update":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Classification'))
                out_message = obj_prodcat.update_catalogdetails()
                if out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)

            if self.request.query_params.get("Group") == "CATALOG_ASSIGN":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Classification'))
                out_message = obj_prodcat.atmaSet_AssginCatalog()
                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message})
        except Exception as e:
            return Response({"MESSAGE": "ERROR", "DATA": str(e)})

class atmaCatalog_Getapi(APIView):
   def post(self,request):
       try:
           if self.request.query_params.get("Group") == "Catalog_Details":
               jsondata = json.loads(request.body.decode('utf-8'))
               object_query =  mATMA.ATMA_model()
               object_query.type = self.request.query_params.get("Type")
               object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
               object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
               ld_out_message = object_query.atmaget_catalog()
               if ld_out_message.get("MESSAGE") == 'FOUND':
                   ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                              "MESSAGE": 'FOUND'}
               elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                   ld_dict = {"MESSAGE": 'NOT_FOUND'}
               else:
                   ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
               return Response(ld_dict)

           if self.request.query_params.get("Group") == "partner_product":
               jsondata = json.loads(request.body.decode('utf-8'))
               object_query = mATMA.ATMA_model()
               object_query.type = self.request.query_params.get("Type")
               object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
               object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
               ld_out_message = object_query.getcatalog_partnerproduct()
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

class GET_ATMA_Data(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "ATMASUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_atma = mATMA.ATMA_model()
                obj_atma.Group = self.request.query_params.get("Group")
                obj_atma.Action = self.request.query_params.get("Action")
                obj_atma.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
                obj_atma.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                ld_out_message = obj_atma.atma_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "ATMAPAYMENTSUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                obj_prodcat.cls = json.dumps(jsondata.get('Params').get('Classification'))
                ld_out_message = obj_prodcat.atma_paymentsummary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED"+ str(e), "DATA": str(e)})

class GET_ATMA_Directors_Data(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "ATMASUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_atma = mATMA.ATMA_model()
                obj_atma.Group = self.request.query_params.get("Group")
                obj_atma.Action = self.request.query_params.get("Action")
                obj_atma.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
                obj_atma.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                ld_out_message = obj_atma.atmadirector_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED"+ str(e), "DATA": str(e)})

class atma_Activitydetails_Set_api(APIView):
   def post(self, request):
       try:
           if self.request.query_params.get("Group") == "Activity_Details":
               jsondata = json.loads(request.body.decode('utf-8'))
               obj_modname = mATMA.ATMA_model()
               obj_modname.action = self.request.query_params.get("Action")
               obj_modname.type = self.request.query_params.get("Type")
               obj_modname.jsonData = json.dumps(jsondata.get('Params'))
               obj_modname.dataw = json.dumps(jsondata.get('Classification'))
               out_message = obj_modname.Set_Activitydetails()
               if out_message[0] == "SUCCESSFULLY INSERTED":
                   return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
               else:
                   return Response({"MESSAGE": out_message})

           if self.request.query_params.get("Group") == "Activity_Details_Update":
               jsondata = json.loads(request.body.decode('utf-8'))
               obj_prodcat = mATMA.ATMA_model()
               obj_prodcat.Group = self.request.query_params.get("Group")
               obj_prodcat.action = self.request.query_params.get("Action")
               obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
               obj_prodcat.dataw = json.dumps(jsondata.get('Classification'))
               out_message = obj_prodcat.update_activitydetails()
               if out_message[0] == "SUCCESSFULLY UPDATED":
                   return Response({"SUCCESS"})

               else:
                   return Response(out_message)
       except Exception as e:
           return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class atma_Activitydetails_Get_api(APIView):
   def post(self,request):
       try:
           if self.request.query_params.get("Group") == "Activity_Details":
               jsondata = json.loads(request.body.decode('utf-8'))
               object_query =mATMA.ATMA_model()
               object_query.type = self.request.query_params.get("Type")
               object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
               object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
               ld_out_message = object_query.atma_Activitydetails_Get()
               if ld_out_message.get("MESSAGE") == 'FOUND':
                   ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                              "MESSAGE": 'FOUND'}
               elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                   ld_dict = {"MESSAGE": 'NOT_FOUND'}
               else:
                   ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
               return Response(ld_dict)
       except Exception as e:
           return Response({"MESSAGE": "ERROR_OCCURED"+ str(e), "DATA": str(e)})

class atmaPartnerPayment_Setapi(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Header Details":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Classification'))
                out_message = obj_prodcat.Set_Header()
                out_message1=common.outputReturns(out_message,1)
                out_message2 = common.outputReturns(out_message, 0)
                out_message3 = common.outputReturns(out_message, 2)
                out_message4 = common.outputReturns(out_message, 3)
                if out_message1 == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS","DATA":out_message2,"RM_GID":out_message3,"p_code":out_message4})

                else:
                    return Response({"MESSAGE": 'NOTE'+" : " + out_message2})

            if self.request.query_params.get("Group") == "MoveToRM":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Params').get('Classification'))
                out_message = obj_prodcat.Set_movetorm()
                out_message1=common.outputReturn(out_message,1)
                out_message2 = common.outputReturn(out_message, 0)
                if out_message1 == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS","DATA":out_message2})

                else:
                    return Response({ out_message1})

            if self.request.query_params.get("Group") == "PAYMODESUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Params').get('Classification'))
                out_message = obj_prodcat.set_paymode()
                if out_message[0] == "SUCCESS":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
            if self.request.query_params.get("Group") == "UPDATEPAYMODESUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Params').get('Classification'))
                out_message = obj_prodcat.update_paymode()
                if out_message[0] == "SUCCESS":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)

        except Exception as e:
            return Response({"MESSAGE": 'ERROR_OCCURED' + str(e), "DATA": str(e)})


class atma_AttachmentApi_get(APIView):
   def post(self,request):
       try:
           if self.request.query_params.get("Group") == "Document_Group":
               jsondata = json.loads(request.body.decode('utf-8'))
               object_query = mATMA.ATMA_model()
               object_query.type = self.request.query_params.get("Type")
               object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
               jsonData1=jsondata.get('Params').get('Filter')
               object_query.jsonData = json.dumps(jsonData1)

               ld_out_message = object_query.get_AttachmentSummary_model()
               if ld_out_message.get("MESSAGE") == 'FOUND':
                   ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                              "MESSAGE": 'FOUND'}
               elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                   ld_dict = {"MESSAGE": 'NOT_FOUND'}
               else:
                   ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
               return Response(ld_dict)
       except Exception as e:
           return Response({"MESSAGE": "ERROR_OCCURED"+ str(e), "DATA": str(e)})

class atma_Docgroup_Set(APIView):
   def post(self, request):
       try:
           if self.request.query_params.get("Group") == "Document_Group":
               obj_modname = mATMA.ATMA_model()
               obj_modname.action = self.request.query_params.get("Action")
               obj_modname.type = self.request.query_params.get("Type")
               jsonData1= json.loads(request.body.decode('utf-8'))
               obj_modname.jsonData = json.dumps(jsonData1)

               out_message = obj_modname.Set_Docgroup()
               if out_message == "SUCCESSFULLY INSERTED":
                   return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
               else:
                   return Response({"MESSAGE": out_message})
       except Exception as e:
           return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})



class Gettaxdetails(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "GETTAXTYPE":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_atma = mATMA.ATMA_model()
                obj_atma.Group = self.request.query_params.get("Group")
                obj_atma.Action = self.request.query_params.get("Action")
                obj_atma.emptyjsonone = json.dumps({})
                obj_atma.emptyjsontwo = json.dumps({})
                ld_out_message = obj_atma.gettaxdetails()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get(
                    "Group") == "TAXINSERTSUMMARYEXEMPTEDYES" or self.request.query_params.get(
                    "Group") == "TAXINSERTSUMMARYEXEMPTEDNO":
                obj_atma = mATMA.ATMA_model()
                obj_atma.Group = self.request.query_params.get("Group")
                obj_atma.Action = self.request.query_params.get("Action")
                obj_atma.filterjson = json.loads(request.body.decode('utf-8'))
                obj_atma.clsjson2 = json.dumps(obj_atma.filterjson[0])
                obj_atma.clsjson3 = json.dumps(obj_atma.filterjson[1])
                ld_out_message = obj_atma.set_taxdetailsdata()
                if ld_out_message[0] == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response(ld_out_message)
            elif self.request.query_params.get(
                    "Group") == "TAXINSERTSUMMARYEXEMPTEDUPDATEYES" or self.request.query_params.get(
                    "Group") == "TAXINSERTSUMMARYEXEMPTEDUPDATENO" or self.request.query_params.get(
                    "Group") == "TAXINSERTSUMMARYEXEMPTEDUPDATEYESNOFILE":

                obj_atma = mATMA.ATMA_model()
                obj_atma.Group = self.request.query_params.get("Group")
                obj_atma.Action = self.request.query_params.get("Action")
                obj_atma.filterjson = json.loads(request.body.decode('utf-8'))
                obj_atma.clsjson2 = json.dumps(obj_atma.filterjson[0])
                obj_atma.clsjson3 = json.dumps(obj_atma.filterjson[1])
                ld_out_message = obj_atma.update_taxdetailsdata()
                if ld_out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})
                else:
                    return Response(ld_out_message)

            if self.request.query_params.get("Group") == "ATMATAXSUMMARY":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_atma = mATMA.ATMA_model()
                obj_atma.Group = self.request.query_params.get("Group")
                obj_atma.Action = self.request.query_params.get("Action")
                obj_atma.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                obj_atma.cls = json.dumps(jsondata.get('Params').get('Classification'))
                ld_out_message = obj_atma.get_taxsummary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)

        except Exception as e:
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class atma_Activityget(APIView):
  def post(self,request):
      try:
          if self.request.query_params.get("Group") == "Activity_Group":
              jsondata = json.loads(request.body.decode('utf-8'))
              object_query = mATMA.ATMA_model()
              object_query.type = self.request.query_params.get("Type")
              object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
              object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
              ld_out_message = object_query.atmaget_activity()
              if ld_out_message.get("MESSAGE") == 'FOUND':
                  ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                             "MESSAGE": 'FOUND'}
              elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                  ld_dict = {"MESSAGE": 'NOT_FOUND'}
              else:
                  ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
              return Response(ld_dict)
      except Exception as e:
          return Response({"MESSAGE": "ERROR_OCCURED"+ str(e), "DATA": str(e)})

class atma_ActivitySet_API(APIView):
  def post(self, request):
      try:
          if self.request.query_params.get("Group") == "Activity_ADD":
              jsondata = json.loads(request.body.decode('utf-8'))
              obj_modname =  mATMA.ATMA_model()
              obj_modname.action = self.request.query_params.get("Action")
              obj_modname.type = self.request.query_params.get("Type")
              obj_modname.jsonData = json.dumps(jsondata.get('Params'))
              obj_modname.dataw = json.dumps(jsondata.get('Classification'))
              out_message = obj_modname.atma_activityadd()
              if out_message == "SUCCESS":
                  return Response({"MESSAGE": "SUCCESS"})
              else:
                  return Response({"MESSAGE": out_message})
          if self.request.query_params.get("Group") == "Activity_UPDATE":
              jsondata = json.loads(request.body.decode('utf-8'))
              obj_modname = mATMA.ATMA_model()
              obj_modname.action = self.request.query_params.get("Action")
              obj_modname.type = self.request.query_params.get("Type")
              obj_modname.jsonData = json.dumps(jsondata.get('Params'))
              obj_modname.dataw = json.dumps(jsondata.get('Classification'))
              out_message = obj_modname.update_Actgroup()
              if out_message == "SUCCESSFULLY UPDATED":
                  return Response({"MESSAGE": "SUCCESS"})
              else:
                  return Response({"MESSAGE": out_message})
      except Exception as e:
          return Response({"MESSAGE": "ERROR " + str(e), "DATA": str(e)})
class atma_Updateattachment(APIView):
   def post(self,request):
       try:
           if self.request.query_params.get("Group") == "Document_Update" or self.request.query_params.get("Group") == "Document_Updatenofile":
               obj_atma = mATMA.ATMA_model()
               obj_atma.Group = self.request.query_params.get("Group")
               obj_atma.Action = self.request.query_params.get("Action")
               obj_atma.filterjson = json.loads(request.body.decode('utf-8'))
               obj_atma.filterjson1 = json.dumps(obj_atma.filterjson)
               ld_out_message = obj_atma.atmaupdateattachment()
               return Response(ld_out_message)
       except Exception as e:
           return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})
class atma_clientdetails_api(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "ClientDetails_ADD":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_modname = mATMA.ATMA_model()
                obj_modname.action = self.request.query_params.get("Action")
                obj_modname.type = self.request.query_params.get("Type")
                obj_modname.jsonData = json.dumps(jsondata.get('Params'))
                obj_modname.dataw = json.dumps(jsondata.get('Classification'))
                out_message = obj_modname.Set_clientgroup()
                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": out_message})
            if self.request.query_params.get("Group") == "ClientDetails_GET":
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mATMA.ATMA_model()
                object_query.action = self.request.query_params.get("Action")
                object_query.type = self.request.query_params.get("Type")
                object_query.json_classification = json.dumps(jsondata.get('Classification'))
                object_query.jsonData = json.dumps(jsondata.get('Params'))
                ld_out_message = object_query.get_clientgroup()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
            if self.request.query_params.get("Group") == "ClientDetails_Update":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Classification'))
                out_message = obj_prodcat.update_clientdetails()
                if out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
        except Exception as e:
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class atma_contractdetails_api(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "ContractDetails_SET":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_modname = mATMA.ATMA_model()
                obj_modname.action = self.request.query_params.get("Action")
                obj_modname.type = self.request.query_params.get("Type")
                obj_modname.jsonData = json.dumps(jsondata.get('Params'))
                obj_modname.dataw = json.dumps(jsondata.get('Classification'))
                out_message = obj_modname.Set_contractgroup()
                if out_message[0] == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": out_message})
            if self.request.query_params.get("Group") == "ContractDetails_GET":
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mATMA.ATMA_model()
                object_query.action = self.request.query_params.get("Action")
                object_query.type = self.request.query_params.get("Type")
                object_query.json_classification = json.dumps(jsondata.get('Classification'))
                object_query.jsonData = json.dumps(jsondata.get('Params'))
                ld_out_message = object_query.get_contractgroup()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)

            if self.request.query_params.get("Group") == "ContractDetails_Update":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Classification'))
                out_message = obj_prodcat.update_contractdetails()
                if out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
        except Exception as e:
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class atma_branchdetails_api(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "BranchDetails_Set":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_modname = mATMA.ATMA_model()
                obj_modname.action = self.request.query_params.get("Action")
                obj_modname.type = self.request.query_params.get("Type")
                obj_modname.jsonData = json.dumps(jsondata.get('Params'))
                obj_modname.dataw = json.dumps(jsondata.get('Classification'))
                out_message = obj_modname.Set_branchgroup()
                if out_message[0] == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": out_message})
            if self.request.query_params.get("Group") == "BranchDetails_GET":
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mATMA.ATMA_model()
                object_query.action = self.request.query_params.get("Action")
                object_query.type = self.request.query_params.get("Type")
                object_query.json_classification = json.dumps(jsondata.get('Classification'))
                object_query.jsonData = json.dumps(jsondata.get('Params'))
                ld_out_message = object_query.get_branchgroup()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)

            if self.request.query_params.get("Group") == "BranchDetails_Update":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Classification'))
                out_message = obj_prodcat.update_branchdetails()
                if out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
        except Exception as e:
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})


class atma_basicprofiledetails_api(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "BasicProfile_Set":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_modname = mATMA.ATMA_model()
                obj_modname.action = self.request.query_params.get("Action")
                obj_modname.type = self.request.query_params.get("Type")
                obj_modname.jsonData = json.dumps(jsondata.get('Params'))
                obj_modname.dataw = json.dumps(jsondata.get('Classification'))
                out_message = obj_modname.Set_basicprofilegroup()
                if out_message[0] == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": out_message})
            if self.request.query_params.get("Group") == "Partnerprofile_Get":
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mATMA.ATMA_model()
                object_query.action = self.request.query_params.get("Action")
                object_query.type = self.request.query_params.get("Type")
                object_query.json_classification = json.dumps(jsondata.get('Classification'))
                object_query.jsonData = json.dumps(jsondata.get('Params'))
                ld_out_message = object_query.get_basicprofiledetailsgroup()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class atma_getcheckerdetails_api(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Checker_Get":
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mATMA.ATMA_model()
                object_query.action = self.request.query_params.get("Action")
                object_query.type = self.request.query_params.get("Type")
                object_query.json_classification = json.dumps(jsondata.get('Classification'))
                object_query.jsonData = json.dumps(jsondata.get('Params'))
                ld_out_message = object_query.get_checker_detailsgroup()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)

            if self.request.query_params.get("Group") == "Checker_Status":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Classification'))
                out_message = obj_prodcat.update_productstatusdetails()
                if out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
        except Exception as e:
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class Prmaker_Set(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "PRMAKER Details":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Classification'))
                out_message = obj_prodcat.Set_Prmaker()
                if out_message == "SUCCESSFULLY INSERTED":
                    return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
                else:
                    return Response({"MESSAGE": out_message})
        except Exception as e:
            return Response({"MESSAGE": "ERROR", "DATA": str(e)})

class PRMAKER(APIView):
   def post(self,request):
       try:
           if self.request.query_params.get("Group") == "PRMAKER Details":
               jsondata = json.loads(request.body.decode('utf-8'))
               object_query = mATMA.ATMA_model()
               object_query.type = self.request.query_params.get("Type")
               object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
               object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
               ld_out_message = object_query.get_prmaker()
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

class Partnerproductapi_get(APIView):
   def post(self,request):
       try:
           if self.request.query_params.get("Group") == "Partner Product":
               jsondata = json.loads(request.body.decode('utf-8'))
               object_query = mATMA.ATMA_model()
               object_query.type = self.request.query_params.get("Type")
               object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
               object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
               ld_out_message = object_query.get_profileProduct()
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

class Partnerproductapi_set(APIView):
   def post(self, request):
       try:
           if self.request.query_params.get("Group") == "Partner Product":
               jsondata = json.loads(request.body.decode('utf-8'))
               obj_modname =  mATMA.ATMA_model()
               obj_modname.action = self.request.query_params.get("Action")
               obj_modname.type = self.request.query_params.get("Type")
               obj_modname.jsonData = json.dumps(jsondata.get('Params'))
               obj_modname.dataw = json.dumps(jsondata.get('Classification'))
               out_message = obj_modname.Set_Partnerproduct()
               if out_message[0] == "SUCCESSFULLY INSERTED":
                   return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
               else:
                   return Response({"MESSAGE": out_message})
       except Exception as e:
           return Response({"MESSAGE": "ERROR", "DATA": str(e)})

class Partnerdeactivateapi_Set(APIView):
   def post(self, request):
       try:
           if self.request.query_params.get("Group") == "Partner Inactive":
               jsondata = json.loads(request.body.decode('utf-8'))
               obj_modname = mATMA.ATMA_model()
               obj_modname.action = self.request.query_params.get("Action")
               obj_modname.type = self.request.query_params.get("Type")
               obj_modname.jsonData = json.dumps(jsondata.get('Params'))
               obj_modname.dataw = json.dumps(jsondata.get('Classification'))
               out_message = obj_modname.Set_Partnerdeactivate()
               if out_message[0] == "SUCCESSFULLY INSERTED":
                   return Response({"MESSAGE": "SUCCESSFULLY INSERTED"})
               else:
                   return Response({"MESSAGE": out_message})
       except Exception as e:
           return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})


class approval_stagesapi(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "RM_To_VMU_Update":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Classification'))
                out_message = obj_prodcat.update_aproval_stagesdetails()
                if out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
            if self.request.query_params.get("Group") == "APPROVED_GROUP":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Classification'))
                out_message = obj_prodcat.update_headaproval_stagesdetails()
                if out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
        except Exception as e:
            return Response({"MESSAGE": "ERROR" + str(e), "DATA": str(e)})

class Partnerapproval(APIView):
  def post(self,request):
      try:
          if self.request.query_params.get("Group") == "Partner Activate":
              jsondata = json.loads(request.body.decode('utf-8'))
              object_query = mATMA.ATMA_model()
              object_query.type = self.request.query_params.get("Type")
              object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
              object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
              ld_out_message = object_query.get_partapproval()
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

class Partnerdisapproval(APIView):
  def post(self,request):
      try:
          if self.request.query_params.get("Group") == "Partner Inactivate":
              jsondata = json.loads(request.body.decode('utf-8'))
              object_query = mATMA.ATMA_model()
              object_query.type = self.request.query_params.get("Type")
              object_query.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
              object_query.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
              ld_out_message = object_query.get_partdisapproval()
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


class approval_paartnergetapi(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Partner_Approval_Get":
                jsondata = json.loads(request.body.decode('utf-8'))
                object_query = mATMA.ATMA_model()
                object_query.type = self.request.query_params.get("Type")
                object_query.json_classification = json.dumps(jsondata.get('Params'))
                object_query.jsonData = json.dumps(jsondata.get('Classification'))
                ld_out_message = object_query.get_approvalpartner()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": 'FOUND'}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": 'NOT_FOUND'}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}
                return Response(ld_dict)

            if self.request.query_params.get("Group") == "Partner_ChangeRequest":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Classification'))
                out_message = obj_prodcat.updateapprovalrequest()
                if out_message[0] == "SUCCESS":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)

            if self.request.query_params.get("Group") == "APPROVER_TO_REQUEST":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Params').get('Classification'))
                out_message = obj_prodcat.change_request_page()
                out_message1 = common.outputReturn(out_message, 1)
                out_message2 = common.outputReturn(out_message, 0)
                if out_message1 == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS", "DATA": out_message2})

                else:
                    return Response({out_message1})

            if self.request.query_params.get("Group") == "VIEW_TO_CANCEL":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Params').get('Classification'))
                out_message = obj_prodcat.change_request_page()
                out_message1 = common.outputReturn(out_message, 1)
                out_message2 = common.outputReturn(out_message, 0)
                if out_message1 == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS", "DATA": out_message2})

                else:
                    return Response({out_message1})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})

class Update_changerequest_API(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Activation_Request":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mATMA.ATMA_model()
                obj_prodcat.Group = self.request.query_params.get("Group")
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.jsonData = json.dumps(jsondata.get('Params').get('Filter'))
                obj_prodcat.dataw = json.dumps(jsondata.get('Params').get('Classification'))
                out_message = obj_prodcat.activation_request()
                if out_message[0] == "SUCCESSFULLY UPDATED":
                    return Response({"SUCCESS"})

                else:
                    return Response(out_message)
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})



