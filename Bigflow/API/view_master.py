from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Bigflow.Master.Model import mMasters
from Bigflow.Transaction.Model import mFET


class Product_API(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "PRODUCT_GET":
                obj_product = mFET.FET_model()
                obj_product.type = self.request.query_params.get("Type")
                obj_product.sub_type = self.request.query_params.get("Subtype")
                obj_product.name = ''
                obj_product.limit = '100'

                out_message = obj_product.get_product()
                if len(out_message) > 0:
                    return Response({"MESSAGE": "FOUND", "DATA": json.loads(out_message)})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Campaign_API(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "CAMPAIGN_GET":
                obj_campaign = mMasters.Masters()
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_campaign.type = self.request.query_params.get("Type")
                obj_campaign.sub_type = self.request.query_params.get("Subtype")
                obj_campaign.jsonData = json.dumps(jsondata.get('Parms').get('Filter'))
                obj_campaign.json_classification = json.dumps(jsondata.get('Parms').get('Classification'))

                df_outmessage = obj_campaign.get_campaign()

                if df_outmessage.empty == False:
                    json_data = json.loads(df_outmessage.to_json(orient='records'))
                    return Response({"MESSAGE": "FOUND", "DATA": json_data})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class CCBS_MASTER(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "CCBS_MASTER":
                obj_campaign = mMasters.Masters()
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_campaign.type = self.request.query_params.get("Type")
                obj_campaign.sub_type = self.request.query_params.get("Sub_type")
                obj_campaign.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_campaign.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))

                df_outmessage = obj_campaign.get_CCBS_Master()

                if df_outmessage.empty == False:
                    json_data = json.loads(df_outmessage.to_json(orient='records'))
                    return Response({"MESSAGE": "FOUND", "DATA": json_data})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})

            if self.request.query_params. \
                    get("Group") == "SET_CATEGORY_AND_SUBCATEGORY_MASTER":
                obj_campaign = mMasters.Masters()
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_campaign.type = self.request.query_params.get("Type")
                obj_campaign.sub_type = self.request.query_params.get("Sub_type")
                obj_campaign.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_campaign.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))

                df_outmessage = obj_campaign.set_cat_subcat_Master()

                if df_outmessage[0] == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": str(df_outmessage[0])})

            if self.request.query_params.get("Group") == "SET_CCBS_MASTER":
                obj_campaign = mMasters.Masters()
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_campaign.type = self.request.query_params.get("Type")
                obj_campaign.sub_type = self.request.query_params.get("Sub_type")
                obj_campaign.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_campaign.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))

                df_outmessage = obj_campaign.set_CCBS_Master()

                if df_outmessage[0] == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": str(df_outmessage[0])})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class StatePrice_API(APIView):
    def post(self, request):
        try:
            obj_State = mMasters.Masters()
            jsondata = json.loads(request.body.decode('utf-8'))
            obj_State.type = self.request.query_params.get("Type")
            obj_State.sub_type = self.request.query_params.get("Subtype")
            obj_State.create_by = self.request.query_params.get("Emp_Gid")
            obj_State.json_classification = json.dumps(jsondata.get('Parms').get('Classification'))
            obj_State.json_filters = json.dumps(jsondata.get('Parms').get('Filter'))
            out_message = obj_State.get_StatePrice()
            if len(out_message) > 0:
                return Response({"MESSAGE": "FOUND", "DATA": out_message})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class All_Tables_Values_Get(APIView):
    def post(self, request):
        try:
            obj_values = mMasters.Masters()
            obj_values.action = ''
            obj_values.jsonData = request.body.decode('utf-8')
            obj_values.entity_gid = self.request.query_params.get("Entity_Gid")

            out_message = obj_values.get_alltablevalue()

            if out_message.empty == False:
                json_data = json.loads(out_message.to_json(orient='records'))
                return Response({"MESSAGE": "FOUND", "DATA": json_data})
            else:
                return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class All_Product_Get(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "GET_ALL_PRODUCT":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_allproduct = mMasters.Masters()
                obj_allproduct.type = self.request.query_params.get("Type")
                obj_allproduct.sub_type = self.request.query_params.get("Sub_Type")
                obj_allproduct.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_allproduct.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_allproduct.get_AllProduct()
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


class Classification_Get(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "BRANCH_SALES":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_classification = mMasters.Masters()
                obj_classification.type = self.request.query_params.get("Type")
                obj_classification.sub_type = self.request.query_params.get("Sub_Type")
                obj_classification.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_classification.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_classification.get_classification_summary()
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


class ProductCat_type_Set(APIView):
    def post(self, request):
       try:
            if self.request.query_params.get("Group") == "Product_Category" or "Product_Type" or "Product_Carton_Map" or "insert_data" or "":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_prodcat = mMasters.Masters()
                obj_prodcat.action = self.request.query_params.get("Action")
                obj_prodcat.type = self.request.query_params.get("Type")
                obj_prodcat.jsonData = json.dumps(jsondata)
                out_message = obj_prodcat.Set_Productcat()
                if out_message[0] == "SUCCESS" or "SUCCESSFULLY UPDATED":
                  return Response({"MESSAGE": "SUCCESS"})
                else:
                  return Response({"MESSAGE": "FAIL", "DATA": str(out_message[0])})
       except Exception as e:
            return Response({"MESSAGE": "ERROR", "DATA": str(e)})


class Supplier_Master(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Supplier_Get":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_supplier = mMasters.Masters()
                obj_supplier.type = self.request.query_params.get("Type")
                obj_supplier.sub_type = self.request.query_params.get("SubType")
                obj_supplier.json_supplier = json.dumps(jsondata.get('Params').get('Details'))
                obj_supplier.json_classification = json.dumps(jsondata.get('Params').get('Classification'))
                out_message = obj_supplier.get_Supplier()
                if out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}

                elif out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_message.get("MESSAGE")}
                return Response(ld_dict)
            if self.request.query_params.get("Group") == "Supplier_Set":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_supplier = mMasters.Masters()
                obj_supplier.action = self.request.query_params.get("Action")
                obj_supplier.json_supplier = json.dumps(jsondata.get('Params').get('Supplier'))
                obj_supplier.json_address = json.dumps(jsondata.get('Params').get('Address'))
                obj_supplier.json_contact = json.dumps(jsondata.get('Params').get('Contact'))
                obj_supplier.json_clasfication = json.dumps(jsondata.get('Params').get('Classification'))
                out_message = obj_supplier.set_Supplier()
                if out_message[0] == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL", "DATA": str(out_message[0])})
            elif self.request.query_params.get("Group") == "Supplier_Update":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_supplier = mMasters.Masters()
                obj_supplier.action = self.request.query_params.get("Action")
                obj_supplier.json_supplier = json.dumps(jsondata.get('Params').get('Supplier'))
                obj_supplier.json_address = json.dumps(jsondata.get('Params').get('Address'))
                obj_supplier.json_contact = json.dumps(jsondata.get('Params').get('Contact'))
                obj_supplier.json_clasfication = json.dumps(jsondata.get('Params').get('Classification'))
                out_message = obj_supplier.set_Supplier()
                if out_message[0] == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL", "DATA": str(out_message[0])})
            elif self.request.query_params.get("Group") == "Active_INactive_supplier":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_supplier = mMasters.Masters()
                obj_supplier.action = self.request.query_params.get("Action")
                obj_supplier.json_supplier = json.dumps(jsondata.get('parms').get('supplier'))
                obj_supplier.json_address ='{}'
                obj_supplier.json_contact ='{}'
                obj_supplier.json_clasfication = json.dumps(jsondata.get('parms').get('classification'))
                out_message = obj_supplier.set_Supplier()
                if out_message[0] == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({"MESSAGE": "FAIL", "DATA": str(out_message[0])})




        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class cluster_Master(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "CLUSTER_EMPMAP_FLAG":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_cluster = mMasters.Masters()
                obj_cluster.action = self.request.query_params.get("Group")
                obj_cluster.jsondata = json.dumps(jsondata.get('Classification'))
                ldf_cluster = obj_cluster.get_cluster()
                if ldf_cluster.empty == False:
                    return Response({"MESSAGE": "FOUND", "DATA": json.loads(ldf_cluster.to_json(orient='records'))})
                else:
                    return Response({"MESSAGE": "NOT_FOUND"})

        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})


class Product_Master(APIView):
    def post(self, request):
        try:
            if self.request.query_params.get("Group") == "Product_Get":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_product = mFET.FET_model()
                obj_product.type = self.request.query_params.get("Type")
                obj_product.subtype = self.request.query_params.get("SubType")
                obj_product.jsondata = json.dumps(jsondata.get('Filters'))
                out_message = obj_product.getsmry_product()
                if out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}

                elif out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_message.get("MESSAGE")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "Product_Set":
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_product_set = mMasters.Masters()
                obj_product_set.action = self.request.query_params.get("Action")
                obj_product_set.type = self.request.query_params.get("Type")
                obj_product_set.jsonData = json.dumps(jsondata.get("data"))
                out_message = obj_product_set.Set_Productcat()
                if out_message[0] == "SUCCESS":
                    return Response({"MESSAGE": "SUCCESS"})
                else:
                    return Response({ "MESSAGE": str(out_message[0])})
        except Exception as e:
            return Response({"MESSAGE": "ERROR_OCCURED", "DATA": str(e)})
