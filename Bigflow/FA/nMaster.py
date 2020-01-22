from django.db import connection
import json

class Masters():
    def __init__(self):
        self.action = ''
        self.type = ''
        self.jsonData = {}
        self.entity_gid = {}
        self.create_by = ''

    def set_checkin_date(self):
        cursor = connection.cursor()
        jsondata = self.jsonData
        ckin = json.dumps(jsondata)
        entity_gid = self.entity_Gid
        ckentity = json.dumps(entity_gid)
        parameters = (self.action,self.type,ckin, ckentity, self.create_by,'')
        cursor.callproc('sp_CheckinCheckout_Set', parameters)
        cursor.execute('select @_sp_CheckinCheckout_Set_5')
        output_msg = cursor.fetchone()
        return output_msg


