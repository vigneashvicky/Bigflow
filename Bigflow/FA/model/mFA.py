from django.db import connection
import pandas as pd
import json
from Bigflow.Master.Model import mVariable


class FaModel(mVariable.variable):

    def get_fa_summary(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter_json, self.json_classification, '')
        cursor.callproc('sp_FAAssetProcess_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_FAAssetProcess_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_fa = pd.DataFrame(rows, columns=columns)
        if self.type == 'INVOICE_DETAILS' and self.sub_type == 'DETAILS':
            df_fa['debit_data'] = df_fa['debit_data'].apply(json.loads)
            return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}
        elif self.type == 'CLUB_DETAILS' and self.sub_type == 'CHECKER_SUMMARY':
            df_fa['lj_child_data'] = df_fa['lj_child_data'].apply(json.loads)
            return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}
        elif self.type == 'MERGE_DETAILS' and self.sub_type == 'CHECKER_SUMMARY' and 'lj_default_details' in df_fa.columns:
            df_fa['lj_default_details'] = df_fa['lj_default_details'].apply(json.loads)
            print(df_fa)
            return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}
        elif 'lj_default_details' in df_fa.columns:
            df_fa['lj_default_details'] = df_fa['lj_default_details'].apply(json.loads)
            if self.type == 'SPLIT_DETAILS' and self.sub_type == 'CHECKER_SUMMARY' and 'lj_split_values' in df_fa.columns:
                df_fa['lj_split_values'] = df_fa['lj_split_values'].apply(json.loads)
                return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}
            return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}
        elif self.type == 'SPLIT_DETAILS' and self.sub_type == 'CHECKER_SUMMARY' and 'lj_split_values' in df_fa.columns:
            df_fa['lj_split_values'] = df_fa['lj_split_values'].apply(json.loads)
            df_fa['lj_default_details'] = df_fa['lj_default_details'].apply(json.loads)
            return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}
        return {"DATA": df_fa, "MESSAGE": outmsg_sp[0]}

    def set_fa_make(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.sub_type,self.jsondata,self.jsonData,self.json_file,self.jsonData_sec,self.json_classification,self.employee_gid,'')
        cursor.callproc('sp_FAAssetProcess_Set', parameters)
        cursor.execute('select @_sp_FAAssetProcess_Set_9')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def get_fa_location(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter_json, self.json_classification, '')
        cursor.callproc('sp_FALocation_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_FALocation_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_location = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}

    def set_fa_location(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.sub_type,self.jsondata,self.json_classification,self.employee_gid,'')
        cursor.callproc('sp_FALocation_Set', parameters)
        cursor.execute('select @_sp_FALocation_Set_6')

        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def set_fa_category(self):
        cursor = connection.cursor()
        parameters = ( self.action, self.type, self.sub_type, self.jsondata, self.json_classification, self.employee_gid, '')
        cursor.callproc('sp_FAAssetCategory_Set', parameters)
        cursor.execute('select @_sp_FAAssetCategory_Set_6')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def get_fa_category(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter_json, self.json_classification, '')
        cursor.callproc('sp_FA_Category_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_FA_Category_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_asset_cat = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_asset_cat, "MESSAGE": outmsg_sp[0]}

    def set_sales_order(self):
        cursor = connection.cursor()
        parameters = (self.action, self.soheader_gid, self.detail_gid, self.customer_gid, self.So_Header_date, self.employee_gid, self.Channel, '', 0, 0, self.sodetails,
                      self.entity_gid,self.create_by,'')
        cursor.callproc('sp_SalesOrder_Set',parameters)
        cursor.execute('select @_sp_SalesOrder_Set_13')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def set_fa_depreciation(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.sub_type,self.jsondata,self.jsonData,self.json_classification,self.employee_gid,'')
        cursor.callproc('sp_FADepreciation_Set', parameters)
        cursor.execute('select @_sp_FADepreciation_Set_7')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}

    def get_fin_year(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.filter_json, self.json_classification, '')
        cursor.callproc('sp_Finace_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Finace_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_location = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_location, "MESSAGE": outmsg_sp[0]}

    def set_fin_year(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type,self.sub_type,self.jsondata,self.json_classification,self.employee_gid,'')
        cursor.callproc('sp_Finace_Set', parameters)
        cursor.execute('select @_sp_Finace_Set_6')
        out_message = cursor.fetchone()
        return {"MESSAGE": out_message[0]}