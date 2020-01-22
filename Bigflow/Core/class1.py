from django.db import connection
from Bigflow.Master.Model import mVariable
import pandas as pd
import Bigflow

class login(mVariable.variable):
    cursor = connection.cursor()

    def setposition(self):
        cursor = connection.cursor()
        parameters = (self.action, self.latlong_gid, self.employee_gid, self.latitude, self.longitude,self.jsondata,
                      self.entity_gid, self.create_by, '')
        cursor.callproc('sp_Latlong_Set', parameters)
        cursor.execute('select @_sp_Latlong_Set_8')
        output_msg = cursor.fetchone()
        return output_msg

    def getposition(self):
        cursor = connection.cursor()
        parameters = (self.action,  self.employee_gid,self.from_date,self.to_date,self.entity_gid, '')
        cursor.callproc('sp_Latlong_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        output_msg = pd.DataFrame(rows, columns=columns)
        return output_msg


    def getcollectionperformance(self):
        cursor = connection.cursor()
        parameters = (self.action,self.type, self.from_date, self.to_date,self.customer_gid, self.entity_gid, '')
        cursor.callproc('sp_CuecardBucket_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        output_msg = pd.DataFrame(rows, columns=columns)
        return output_msg

def get_login(str1, str2):
    cursor = connection.cursor()
    cursor.callproc("sp_UMLogin_Get", (0, str1, converttoascii(str2), ''))
    columns = [d[0] for d in cursor.description]
    ldict = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.execute('select @_sp_UMLogin_Get_3')
    id = cursor.fetchone()
    ldist = [ldict, id]
    #ld_dict = {"DATA" : ldict[0],"MESSAGE" : id[0]}
    return ldist


def converttoascii(password):
    l = len(password)
    newuser = ''
    for i in range(0, l):
        tmp = ord(password[i])
        temp = tmp - l
        g = len(str(temp))
        newuser = newuser + ("0" if g < 3 else "") + str(temp)
    return newuser

    @property
    def get_employee(self):
        return "hello"


def menulist(str1,str2):
    cursor = connection.cursor()
    cursor.callproc("sp_UMEmployeevsMenu_Get", (str1, str2,''))
    columns = [d[0] for d in cursor.description]
    ldict = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.execute('select @_sp_UMEmployeevsMenu_Get_2')
    id = cursor.fetchone()
    ldist = [ldict, id]
    return ldist
