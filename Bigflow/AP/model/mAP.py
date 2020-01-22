from django.db import connection
import pandas as pd
import json
from Bigflow.Transaction.Model import mFET

class ap_model(mFET.FET_model):


    def get_grn(self):
        cursor = connection.cursor()
        parameters = (self.action, self.POnumber,self.supplier_gid, self.entity_gid,'')
        cursor.callproc('sp_APInvoiceGRN_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def get_inwarddtl(self):
        cursor = connection.cursor()
        jsondata = self.FILTER_JSON
        FILTER_JSON = json.dumps(jsondata)
        parameters = (self.action,self.type, FILTER_JSON, self.entity_gid, '')
        cursor.callproc('sp_InwardOffice_Get', parameters)
        cursor.execute('select @_sp_InwardOffice_Get_4')
        output_msg = cursor.fetchone()
        return output_msg


    def set_Invoice(self):
        cursor = connection.cursor()
        headjsondata = self.header_json
        deatailjson = self.detail_json
        invoicejson = self.invoice_json
        debitjson = self.debit_json
        creditjson = self.credit_json
        statusjson = self.status_json
        header_json = json.dumps(headjsondata)
        detail_json = json.dumps(deatailjson)
        invoice_json = json.dumps(invoicejson)
        debit_json = json.dumps(debitjson)
        credit_json = json.dumps(creditjson)
        status_json = json.dumps(statusjson)
        parameters = (self.action, self.type, invoice_json,detail_json,header_json,debit_json,credit_json,status_json,self.entity_gid,self.employee_gid,'')
        cursor.callproc('sp_APInvoiceSPS_Set', parameters)
        cursor.execute('select @_sp_APInvoiceSPS_Set_10')
        output_msg = cursor.fetchone()
        return output_msg

    def Invoice_get(self):
        cursor = connection.cursor()
        parameters = (self.action, self.ponumber,self.supplier_gid,self.inwardheader_gid,self.inwarddetail_gid ,self.status,self.state_gid,self.entity_gid,1, '')
      #  parameters = (self.action, self.ponumber,self.supplier_gid,self.inwardheader_gid,self.inwarddetail_gid ,self.status,self.state_gid,self.entity_gid, '')
        cursor.callproc('sp_APInvoice_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def credit_get(self):
        cursor = connection.cursor()
        parameters = (self.type, self.supplier_gid,self.entity_gid, '')
        cursor.callproc('sp_APSupplierCredit_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def set_Invoiceheader(self):
        cursor = connection.cursor()
        headjsondata = self.header_json
        debitjson = self.debit_json
        deatailjson = self.detail_json
        statusjson = self.status_json
        header_json = json.dumps(headjsondata)
        debit_json = json.dumps(debitjson)
        detail_json = json.dumps(deatailjson)
        status_json = json.dumps(statusjson)
        parameters = (self.action, self.type, header_json,detail_json,debit_json,status_json,self.employee_gid,self.entity_gid,'')
        cursor.callproc('sp_APInvoice_Set', parameters)
        cursor.execute('select @_sp_APInvoice_Set_8')
        output_msg = cursor.fetchone()
        return output_msg

    def hsn_get(self):
        cursor = connection.cursor()
        parameters = (self.type, self.group,'{}',self.entity_gid, '')
        cursor.callproc('sp_HSN_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def hsn_taxget(self):
        cursor = connection.cursor()
        hsndtl = self.hsndtl
        hsndtl_json = json.dumps(hsndtl)
        parameters = (self.group,'AMOUNT_DISCOUNT',hsndtl_json,1,'')
        cursor.callproc('sp_TAXcalculate_Get', parameters)
        columns = [x[0] for x in cursor.description]
        # rows = cursor.fetchall()
        # rows = list(rows)
        # while (cursor.nextset()):
        #     try:
        #      columns = [x[0] for x in cursor.description]
        #      rows = cursor.fetchall()
        #      # columns.append([x[0] for x in cursor.description]).replace('[','').replace(']','')
        #      # rows.append(cursor.fetchall())
        #     except:
        #         print("")
        #
        # grn_dtl = pd.DataFrame(rows, columns=columns)
        # return grn_dtl
        rows = cursor.fetchall()
        rows = list(rows)
        tax_dtl = pd.DataFrame(rows, columns=columns)
        cursor.nextset()
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        tax_dtl2 = pd.DataFrame(rows, columns=columns)
        cursor.nextset()
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        tax_dtl3 = pd.DataFrame(rows, columns=columns)
        cursor.close()
        data = [tax_dtl,tax_dtl2,tax_dtl3]
        return data

    def hsn_Credittaxget(self):
        cursor = connection.cursor()
        hsndtl = self.hsndtl
        hsndtl_json = json.dumps(hsndtl)
        parameters = (self.group,'',hsndtl_json,1,'')
        cursor.callproc('sp_TAXcalculate_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def tablevalue_get(self):
        cursor = connection.cursor()
        tablevalue = self.tablevalue
        tablevalue_json = json.dumps(tablevalue)
        parameters = (self.type, tablevalue_json,self.entity_gid, '')
        cursor.callproc('sp_AllTableValues_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def History_get(self):
        cursor = connection.cursor()
        refvalue = self.refvalue
        refvalue_json = json.dumps(refvalue)
        parameters = (self.group, self.type,refvalue_json,self.entity_gid, '')
        cursor.callproc('sp_APHistory_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def set_payment(self):
        cursor = connection.cursor()
        headjsondata = self.header_json
        detailjson = self.detail_json
        otherjson = self.other_json
        statusjson = self.status_json
        header_json = json.dumps(headjsondata)
        detail_json = json.dumps(detailjson)
        other_json = json.dumps(otherjson)
        status_json = json.dumps(statusjson)
        parameters = (self.action, self.type, header_json,detail_json,other_json,status_json,self.employee_gid,self.entity_gid,'')
        cursor.callproc('sp_APPayment_Set', parameters)
        cursor.execute('select @_sp_APPayment_Set_8')
        output_msg = cursor.fetchone()
        return output_msg

    def rejectdata_get(self):
        cursor = connection.cursor()
        reject_json = json.dumps(self.reject_json)
        parameters = (self.group,self.type,reject_json,self.entity_gid,'')
        cursor.callproc('sp_APInvoiceReject_Get',parameters)
        columns = [x[0] for x  in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        reject_dtl = pd.DataFrame(rows, columns=columns)
        return reject_dtl

    def getreasondata(self):
        cursor = connection.cursor()
        reason_json = json.dumps(self.reason_json)
        parameters = (self.type, reason_json, self.entity_gid, '')
        cursor.callproc('sp_AllTableValues_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        reject_dtl = pd.DataFrame(rows, columns=columns)
        return reject_dtl

    def set_Invoicereject(self):
        cursor = connection.cursor()
        reject_json = self.reject_json
        reject_json = json.dumps(reject_json)
        parameters = (self.action, self.type, reject_json,self.entity_gid,self.employee_gid,'')
        cursor.callproc('sp_APInvoiceReject_Set', parameters)
        cursor.execute('select @_sp_APInvoiceReject_Set_5')
        output_msg = cursor.fetchone()
        return output_msg

    def getpaymentdtl(self):
        cursor = connection.cursor()
        pay_json = self.pay_json
        pay_json = json.dumps(pay_json)
        parameters = (self.group,self.type, pay_json, self.entity_gid, '')
        cursor.callproc('sp_APPayment_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        out = pd.DataFrame(rows, columns=columns)
        return out

    def get_dropdown_detail(self):
        cursor = connection.cursor()
        parameters = (self.tablename, self.gid, self.name,self.entity_gid,'')
        cursor.callproc('sp_Dropdown_Common_active_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        dropdown = pd.DataFrame(rows, columns=columns)
        return dropdown

    def get_ppxdetails(self):
        cursor = connection.cursor()
        parameters = (self.group, self.type, json.dumps(self.filter),self.entity_gid,'')
        cursor.callproc('sp_APPPX_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        result = pd.DataFrame(rows, columns=columns)
        result.insert(4, "Liquidate", 0)
        return result

    def set_ppxdetails(self):
        cursor = connection.cursor()
        detail_json = self.detail_json
        detail_json = json.dumps(detail_json)
        parameters = (self.action, self.type, json.dumps(self.header_json),detail_json, '{}','{"Entity_Gid":['+str(self.entity_gid) +']}',self.employee_gid,'','')
        cursor.callproc('sp_Ap_ppx_Set', parameters)
        cursor.execute('select @_sp_Ap_ppx_Set_8')
        output_msg = cursor.fetchone()
        return output_msg

    def set_Dispatchpayment(self):
        cursor = connection.cursor()
        jsondata = self.PAYMENT_JSON
        PAYMENT_JSON = json.dumps(jsondata)
        parameters = (self.action, self.type, self.in_out, self.courier_gid, self.Dispatch_date, self.send_by,
                      self.awbno, self.dispatch_mode, self.dispatch_type, self.packets, self.weight,
                      self.dispatch_to, self.address, self.city, self.state, self.pincode, self.remark,
                      self.returned, self.returned_on, self.returned_remark, self.pod,
                      self.pod_image, self.isactive, self.isremoved, self.dispatch_gid,
                      PAYMENT_JSON, self.status, self.entity_gid, self.employee_gid, '')
        cursor.callproc('sp_DispatchSPs_Set', parameters)
        cursor.execute('select @_sp_DispatchSPs_Set_29')
        output_msg = cursor.fetchone()
        return output_msg

    def get_auditchklist(self):
        cursor = connection.cursor()
        parameters = ( self.type, self.chk_type,self.header_gid, self.entity_gid, '')
        cursor.callproc('sp_APauditchklist_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        result = pd.DataFrame(rows, columns=columns)
        return result

    def auditchklist(self):
        cursor = connection.cursor()
        chklist_json = self.chklist_json
        chklist_json = json.dumps(chklist_json)
        parameters = (self.action, self.type, chklist_json,'{"Entity_Gid":['+str(self.entity_gid) +']}',self.employee_gid,'')
        cursor.callproc('sp_APauditchklist_Set', parameters)
        cursor.execute('select @_sp_APauditchklist_Set_5')
        output_msg = cursor.fetchone()
        return output_msg

    def Address_Get(self):
        cursor = connection.cursor()
        parameters = (self.location_gid,self.entity_gid,'')
        cursor.callproc('sp_Address_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        service_out = pd.DataFrame(rows,columns=columns)
        return service_out

    def set_PODDispatch_ap(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.courier_gid,self.Dispatch_date,self.send_by,
                      self.awbno,self.dispatch_mode,self.dispatch_type,self.packets,self.weight,
                      self.dispatch_to,self.address,self.city,self.state,self.pincode,self.remark,
                      self.returned,self.returned_on,self.returned_remark,self.pod,
                      self.pod_image,self.isactive,self.isremoved,self.dispatch_gid,"DISPATCHED",
                      self.entity_gid,self.employee_gid,'')
        cursor.callproc('sp_Dispatch_Set',parameters)
        cursor.execute('select @_sp_Dispatch_Set_27')
        output_msg = cursor.fetchone()
        return output_msg

    def set_APstale(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, json.dumps(self.header_json),'{"Entity_Gid":['+str(self.entity_gid) +']}',self.employee_gid,'')
        cursor.callproc('sp_APStale_Set', parameters)
        cursor.execute('select @_sp_APStale_Set_5')
        output_msg = cursor.fetchone()
        return output_msg

    def get_stale(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type,
                        self.filter_json,
                        '{"Entity_Gid":['+str(self.entity_gid) +']}',self.employee_gid,'')
        cursor.callproc('sp_APStale_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        service_out = pd.DataFrame(rows,columns=columns)
        return service_out

    def get_classification_summary(self):
        cursor = connection.cursor()
        parameters = (self.type,self.sub_type,self.jsonData,json.dumps(self.json_classification),'')
        cursor.callproc('sp_Classification_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Classification_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_ta = pd.DataFrame(rows,columns=columns)
        return {"DATA":df_ta,"MESSAGE":outmsg_sp[0]}

    def get_supplier_data(self):
        cursor = connection.cursor()
        parameters = (self.type,self.sub_type,self.jsonData,json.dumps(self.json_classification),'')
        cursor.callproc('sp_SupplierDetails_Get',parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_SupplierDetails_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_ta = pd.DataFrame(rows,columns=columns)
        return {"DATA":df_ta,"MESSAGE":outmsg_sp[0]}

    def set_ECFInvoiceheader(self):
        cursor = connection.cursor()
        headjsondata = self.header_json
        debitjson = self.debit_json
        deatailjson = self.detail_json
        statusjson = self.status_json
        header_json = json.dumps(headjsondata)
        debit_json = json.dumps(debitjson)
        detail_json = json.dumps(deatailjson)
        status_json = json.dumps(statusjson)
        parameters = (self.action, self.type, header_json,detail_json,debit_json,status_json,self.employee_gid,self.entity_gid,'')
        cursor.callproc('sp_ECFInvoice_Set', parameters)
        cursor.execute('select @_sp_ECFInvoice_Set_8')
        output_msg = cursor.fetchone()
        return output_msg

    def ECFInvoice_get(self):
        cursor = connection.cursor()
        parameters = (self.action, self.ecfnumber,self.supplier_gid,self.inwardheader_gid,self.inwarddetail_gid ,self.status,self.state_gid,self.entity_gid, '')
        cursor.callproc('sp_ECFInvoice_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        grn_dtl = pd.DataFrame(rows, columns=columns)
        return grn_dtl

    def ECFset_Invoice(self):
        cursor = connection.cursor()
        headjsondata = self.header_json
        deatailjson = self.detail_json
        invoicejson = self.invoice_json
        debitjson = self.debit_json
        creditjson = self.credit_json
        statusjson = self.status_json
        header_json = json.dumps(headjsondata)
        detail_json = json.dumps(deatailjson)
        invoice_json = json.dumps(invoicejson)
        debit_json = json.dumps(debitjson)
        credit_json = json.dumps(creditjson)
        status_json = json.dumps(statusjson)
        parameters = (
        self.action, self.type, invoice_json, detail_json, header_json, debit_json, credit_json, status_json,
        self.entity_gid, self.employee_gid, '')
        cursor.callproc('sp_ECFInvoiceSPS_Set', parameters)
        cursor.execute('select @_sp_ECFInvoiceSPS_Set_10')
        output_msg = cursor.fetchone()
        return output_msg