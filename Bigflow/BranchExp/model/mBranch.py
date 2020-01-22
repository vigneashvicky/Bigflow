from django.db import connection
import pandas as pd
import json
from Bigflow.Transaction.Model import mFET

class BranchExp_model(mFET.FET_model):

    def get_expensedetails(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_APExpense_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_dp = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_APExpense_Get_4')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_dp, "MESSAGE": sp_out_message[0]}

    def set_expensedetails(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.jsonData,'Y', self.json_classification,1, '')
        cursor.callproc('sp_APExpense_Set', parameters)
        cursor.execute('select @_sp_APExpense_Set_6')
        sp_out_message = cursor.fetchone()
        return { "MESSAGE": sp_out_message[0]}

    def property_set(self):
        cursor=connection.cursor()
        parameters=(self.type,self.sub_type,self.filters,self.classification,'')
        # cursor.callproc('sp_ap_property_Set',parameters)
        cursor.callproc('sp_APProperty_Set', parameters)
        cursor.execute('select @_sp_APProperty_Set_4')
        msg = cursor.fetchone()
        return {"MESSAGE":msg[0]}

    def get_alltablevalue(self):
        cursor = connection.cursor()
        Parameters = (self.type,self.table_values,self.entity_gid,'')
        cursor.callproc('sp_AllTableValues_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        pro_type = pd.DataFrame(rows, columns=columns)
        return pro_type

    def get_pro_details(self):
        cursor=connection.cursor()
        Parameters=(self.Type,self.Sub_Type,self.filter,self.classification,'')
        cursor.callproc('sp_APProperty_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        pro_det = pd.DataFrame(rows, columns=columns)
        return pro_det
