from rest_framework.views import APIView
from rest_framework.response import Response
import json
from Bigflow.API import views as commonview
from Bigflow.Report.Model import mControlSheet

class Control_Sheet(APIView):
    def post(self,request):
        try:
            if self.request.query_params.get("Group") == "INITIAL_SUMMARY":
                # The First Page Summary Data
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mControlSheet.CtrlModel()
                obj_ctrl.group = self.request.query_params.get("Group")
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = self.request.query_params.get("SubType")
                obj_ctrl.create_by = self.request.query_params.get("Employee_Gid")
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_ctrl.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_ctrl.get_ctrl_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "CONTROL_SALES":
                #### Upload the Sale Data and save Excel
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mControlSheet.CtrlModel()
                obj_ctrl.action = self.request.query_params.get("Action")
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = 'TALLY'
                obj_ctrl.create_by = self.request.query_params.get("Create_by")
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_ctrl.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ###
                # Here To Save The File In a Directory
                obj_ctrl.json_file = json.dumps(jsondata.get('Params').get('File'))
                lst_saved_filepath = commonview.File_Upload(obj_ctrl.json_file, 'CONTROL_SHEETS',obj_ctrl.create_by)
                obj_ctrl.jsondata = json.dumps(lst_saved_filepath)
                ###
                out_msg = obj_ctrl.set_ctrl_dump()
                if out_msg.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif out_msg.get("MESSAGE") == 'PROCESS_DATA':
                    ld_dict = {"MESSAGE":"SUCCESS","DATA":json.loads(out_msg.get("DATA").to_json(orient='records'))}
                elif out_msg.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": out_msg.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_msg.get("DATA")}
                return Response(ld_dict)

            elif self.request.query_params.get("Group") == "CONTROL_OUTSTANDING":
                #### Upload the Outstanding Data and save Excel
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mControlSheet.CtrlModel()
                obj_ctrl.action = self.request.query_params.get("Action")
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = 'TALLY'
                obj_ctrl.create_by = '1'
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_ctrl.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ###
                # Here To Save The File In a Directory
                obj_ctrl.json_file = json.dumps(jsondata.get('Params').get('File'))
                lst_saved_filepath = commonview.File_Upload(obj_ctrl.json_file, 'CONTROL_SHEETS',obj_ctrl.create_by)
                obj_ctrl.jsondata = json.dumps(lst_saved_filepath)
                ###
                out_msg = obj_ctrl.set_ctrl_dump()
                if out_msg.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif out_msg.get("MESSAGE") == 'PROCESS_DATA':
                    ld_dict = {"MESSAGE":"SUCCESS","DATA":json.loads(out_msg.get("DATA").to_json(orient='records'))}
                elif out_msg.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": out_msg.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_msg.get("DATA")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "CONTROL_STOCK":
                #### Upload the Stock [2 - Godown and Tallly Source] Data and save Excel
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mControlSheet.CtrlModel()
                obj_ctrl.action = self.request.query_params.get("Action")
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = self.request.query_params.get("SubType")
                obj_ctrl.create_by = self.request.query_params.get("Create_by")
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('DETAILS'))
                obj_ctrl.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ###
                # Here To Save The File In a Directory
                if obj_ctrl.sub_type == 'TALLY':
                    obj_ctrl.json_file = json.dumps(jsondata.get('Params').get('File'))
                    lst_saved_filepath = commonview.File_Upload(obj_ctrl.json_file, 'CONTROL_SHEETS',obj_ctrl.create_by)
                    obj_ctrl.jsondata = json.dumps(lst_saved_filepath)
                else:
                    obj_ctrl.jsondata = '{}'
                ###
                out_msg = obj_ctrl.set_ctrl_dump()
                if out_msg.get("MESSAGE") == 'SUCCESS':
                    ld_dict = {"MESSAGE": "SUCCESS"}
                elif out_msg.get("MESSAGE") == 'PROCESS_DATA':
                    ld_dict = {"MESSAGE":"SUCCESS","DATA":json.loads(out_msg.get("DATA").to_json(orient='records'))}
                elif out_msg.get("MESSAGE") == 'FAIL':
                    ld_dict = {"MESSAGE": out_msg.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + out_msg.get("DATA")}
                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "SALES_COMPARE":
                ### Compare the Sales Data
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mControlSheet.CtrlModel()
                obj_ctrl.group = self.request.query_params.get("Group")
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = self.request.query_params.get("SubType")
                obj_ctrl.create_by = self.request.query_params.get("Employee_Gid")
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_ctrl.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_ctrl.get_ctrl_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "STOCK_COMPARE":
                ### Compare the Sales Data
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mControlSheet.CtrlModel()
                obj_ctrl.group = self.request.query_params.get("Group")
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = self.request.query_params.get("SubType")
                obj_ctrl.create_by = self.request.query_params.get("Employee_Gid")
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_ctrl.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_ctrl.get_ctrl_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
            elif self.request.query_params.get("Group") == "OUTSTANDING_COMPARE":
                ### Compare the Sales Data
                jsondata = json.loads(request.body.decode('utf-8'))
                obj_ctrl = mControlSheet.CtrlModel()
                obj_ctrl.group = self.request.query_params.get("Group")
                obj_ctrl.type = self.request.query_params.get("Type")
                obj_ctrl.sub_type = self.request.query_params.get("SubType")
                obj_ctrl.create_by = self.request.query_params.get("Employee_Gid")
                obj_ctrl.jsonData = json.dumps(jsondata.get('Params').get('FILTER'))
                obj_ctrl.json_classification = json.dumps(jsondata.get('Params').get('CLASSIFICATION'))
                ld_out_message = obj_ctrl.get_ctrl_summary()
                if ld_out_message.get("MESSAGE") == 'FOUND':
                    ld_dict = {"DATA": json.loads(ld_out_message.get("DATA").to_json(orient='records')),
                               "MESSAGE": "FOUND"}
                elif ld_out_message.get("MESSAGE") == 'NOT_FOUND':
                    ld_dict = {"MESSAGE": ld_out_message.get("MESSAGE")}
                else:
                    ld_dict = {"MESSAGE": 'ERROR_OCCURED.' + ld_out_message.get("MESSAGE")}

                return Response(ld_dict)
        except Exception as e:
            return Response({"MESSAGE":"ERROR_OCCURED","DATA":str(e)})