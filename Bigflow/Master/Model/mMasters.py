from django.db import connection
import pandas as pd
import json
import requests
from Bigflow.Master.Model import mVariable


class Masters(mVariable.variable):

    # def __init__(self):
    #     self.filter_json = {}
    #     self.Classification = {}

    def get_Masters(self):
        cursor = connection.cursor()
        Parameters = (self.table_name, self.gid, self.name,self.entity_gid,'')
        cursor.callproc('sp_Dropdown_Common_active_Get', Parameters)
        # cursor.execute('select @_sp_Dropdown_Common_pro_Get_2')
        # Out_SP_msg = cursor.fetchone()
        columns = [d[0] for d in cursor.description]
        ldict = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return ldict

    def get_main_category(self):
        cursor = connection.cursor()
        i = 0;
        while i < 3:
            if (i == 0):
                # cursor.execute('select category_gid,category_code,category_name,category_no from  ap_mst_tcategory')
                Parameters = ('', '{"Table_name": "ap_mst_tcategory","Column_1": "category_gid, category_code, category_name, category_no","Column_2": "","Where_Common": "category","Where_Primary": "","Primary_Value": "","Order_by": "gid"}', self.entity_gid, '')
                cursor.callproc('sp_AllTableValues_Get', Parameters)
                columns = [d[0] for d in cursor.description]
                rows = cursor.fetchall()
                rows = list(rows)
                df_courier = pd.DataFrame(rows, columns=columns)
            elif (i == 1):
                # cursor.execute(' select tcc_gid,tcc_code,tcc_name,cc_no from  ap_mst_tcc '
                #                'where tcc_isactive= "Y" and tcc_isremoved= "N" ')
                Parameters = ('', '{"Table_name": "ap_mst_tcc","Column_1": "tcc_gid, tcc_code, tcc_name, cc_no","Column_2": "","Where_Common": "tcc","Where_Primary": "","Primary_Value": "","Order_by": "gid"}', self.entity_gid, '')
                cursor.callproc('sp_AllTableValues_Get', Parameters)
                columns = [d[0] for d in cursor.description]
                rows = cursor.fetchall()
                rows = list(rows)
                df_courier1 = pd.DataFrame(rows, columns=columns)
            elif (i == 2):
                # cursor.execute('select tbs_gid,tbs_code,tbs_name,bs_no from  ap_mst_tbs  '
                #                'where tbs_isactive="Y" and tbs_isremoved="N"  ')
                Parameters = ('', '{"Table_name": "ap_mst_tbs","Column_1": "tbs_gid, tbs_code, tbs_name, bs_no","Column_2": "","Where_Common": "tbs","Where_Primary": "","Primary_Value": "","Order_by": "gid"}', self.entity_gid, '')
                cursor.callproc('sp_AllTableValues_Get', Parameters)
                columns = [d[0] for d in cursor.description]
                rows = cursor.fetchall()
                rows = list(rows)
                df_courier2 = pd.DataFrame(rows, columns=columns)
            i = i + 1;
        return df_courier, df_courier1, df_courier2

    def get_employee(self):
        cursor = connection.cursor()
        Parameters = (self.employee_gid,self.employee_name,self.cluster_gid,self.cluster, '',self.jsonData,'')
        cursor.callproc('`sp_Employee_Get`', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_courier = pd.DataFrame(rows, columns=columns)
        return df_courier

    def get_department(self):
        cursor = connection.cursor()
        Parameters = (0, '', '', self.entity_gid)
        cursor.callproc('sp_Department_Get', Parameters)
        columns = [d[0] for d in cursor.description]
        ldict = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return ldict

    def set_department(self):
        cursor = connection.cursor()
        parameters = (self.action, self.department_gid, self.department_code, self.department_name, self.entity_gid,
                      self.Employee_gid, '')
        cursor.callproc('sp_Department_Set', parameters)
        cursor.execute('select @_sp_Department_Set_6')
        output_msg = cursor.fetchone()
        return output_msg

    def get_departedit(self):
        cursor = connection.cursor()
        Parameters = (self.dept_gid, '',self.entity_gid, '')
        cursor.callproc('sp_Department_Get', Parameters)
        columns = [d[0] for d in cursor.description]
        ldict = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return ldict

    def get_departdelete(dept_gid):
        cursor = connection.cursor()
        Parameters = ('delete', dept_gid, '', '', 0, 0, '')
        cursor.callproc('sp_Department_Set', Parameters)
        cursor.execute('select @_sp_Department_Set_6')
        id = cursor.fetchone()
        return id

    def get_departactive(dept_gid):
        cursor = connection.cursor()
        Parameters = ('active', dept_gid, '', '', 0, 0, '')
        cursor.callproc('sp_Department_Set', Parameters)
        cursor.execute('select @_sp_Department_Set_6')
        id = cursor.fetchone()
        return id

    def get_departinactive(dept_gid):
        cursor = connection.cursor()
        Parameters = ('inactive', dept_gid, '', '', 0, 0, '')
        cursor.callproc('sp_Department_Set', Parameters)
        cursor.execute('select @_sp_Department_Set_6')
        id = cursor.fetchone()
        return id

    def get_courier_summary(self):
        cursor = connection.cursor()
        Parameters = (0, '',self.entity_gid)
        cursor.callproc('sp_Courier_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_courier = pd.DataFrame(rows, columns=columns)
        return df_courier

    def get_cluster(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.cluster_parent_gid, self.hierarchy_gid, self.employee_gid, self.jsonData,self.jsondata, '')
        cursor.callproc('sp_Cluster_Get', Parameters)
        # columns = [d[0] for d in cursor.description]
        # ldict = [dict(zip(columns, row)) for row in cursor.fetchall()]

        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_cluster = pd.DataFrame(rows, columns=columns)
        return df_cluster

    def set_customer(self):
        cursor = connection.cursor()
        Parameters = (
        self.action, self.customer_gid, self.customer_code, self.customer_name, self.cust_type, self.cust_subtype,
        self.custgrp_gid, self.custcate_gid, self.location_gid, self.address_gid, self.constitution_gid, self.salemode_gid,
        self.size_gid,self.landmark,self.cust_billingname, self.entity_gid, self.create_by, '')
        cursor.callproc('sp_Customer_Set', Parameters)
        cursor.execute('select @_sp_Customer_Set_17')
        df_custset = cursor.fetchone()
        return df_custset

    def get_custgrp(self):
        cursor = connection.cursor()
        Parameters = (self.custgrp_gid, self.custgrp_code, self.custgrp_name, self.entity_gid,self.mysql_limit,'')
        cursor.callproc('sp_Customergroup_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_custgrp = pd.DataFrame(rows, columns=columns)
        return df_custgrp

    def set_emp_customer_map(self):
        cursor = connection.cursor()
        parameters = (self.Employee_gid)
        cursor.callproc('sp_Custemp_Set', parameters)
        cursor.execute('select @sp_Custemp_Set_00')
        output_msg = cursor.fetchone()
        return output_msg

    def get_customer(self):
        cursor = connection.cursor()
        jsondata = self.jsonData
        Parameters = (self.customer_gid, self.customer_code, self.customer_name,jsondata,self.entity_gid,'')
        cursor.callproc('sp_Customer_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_customer = pd.DataFrame(rows, columns=columns)
        return df_customer
#Prakash
    def get_AllCustomer(self):
        cursor = connection.cursor()
        jsondata = self.jsonData
        parameters = (self.type, self.sub_type, jsondata, self.limit,self.json_classification, '')
        cursor.callproc('sp_CustomerFull_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_dp = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_CustomerFull_Get_5')
        sp_out_message = cursor.fetchone()
        return {"DATA":df_dp,"MESSAGE":sp_out_message[0]}



    def get_pincust(self):
        cursor = connection.cursor()
        Parameters = ()
        cursor.callproc('sp_Loctionpincode_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_customer = pd.DataFrame(rows, columns=columns)
        return df_customer

    def get_Location(self):
        cursor = connection.cursor()
        Parameters = (self.location_gid,self.entity_gid, '')
        cursor.callproc('sp_Location_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_location = pd.DataFrame(rows, columns=columns)
        return df_location

    def get_state(self):
        cursor = connection.cursor()
        Parameters = (self.state_gid, self.state_name)
        cursor.callproc('sp_State_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_state = pd.DataFrame(rows, columns=columns)
        return df_state

    def get_district(self):
        cursor = connection.cursor()
        Parameters = (self.district_gid, self.district_name, self.state_gid, self.entity_gid)
        cursor.callproc('sp_District_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_district = pd.DataFrame(rows, columns=columns)
        return df_district

    def get_city(self):
        cursor = connection.cursor()
        Parameters = (self.city_gid, self.city_name, self.district_gid,self.entity_gid)
        cursor.callproc('sp_City_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_city = pd.DataFrame(rows, columns=columns)
        return df_city

    def get_pincode(self):
        cursor = connection.cursor()
        Parameters = (self.pincode_gid, self.pincode_no, self.city_gid, self.district_gid, self.entity_gid,'')
        cursor.callproc('sp_Pincode_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_pin = pd.DataFrame(rows, columns=columns)
        return df_pin

    def get_ddl(self):
        cursor = connection.cursor()
        Parameters = (self.table_name, self.gid, self.name,self.entity_gid,'')
        cursor.callproc('sp_Dropdown_Common_Get', Parameters)
        columns = [d[0] for d in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        ldict1 = pd.DataFrame(rows, columns=columns)
        return ldict1


    def get_alltablevalue(self):
        cursor = connection.cursor()
        jsondt = self.jsonData
        # jsondata = json.dumps(jsondt)
        Parameters = (self.action, jsondt,self.entity_gid,'')
        cursor.callproc('sp_AllTableValues_Get', Parameters)
        columns = [d[0] for d in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        ldict1 = pd.DataFrame(rows, columns=columns)
        return ldict1

    def set_address(self):
        cursor = connection.cursor()
        Parameters = (
        self.action, self.address_gid, self.add_refcode, self.address1, self.address2, self.address3, self.pincode_no,
        self.district_gid, self.city_gid, self.state_gid, self.entity_gid, self.create_by, '')
        cursor.callproc('sp_Address_Set', Parameters)
        cursor.execute('select @_sp_Address_Set_12')
        df_addset = cursor.fetchone()
        return df_addset

    def set_Location(self):
         cursor = connection.cursor()
         Parameters = (self.action,self.location_gid,self.location_code,self.cluster_gid,self.pincode_gid,self.location_name,self.entity_gid
             ,self.create_by,'' )
         cursor.callproc('sp_Location_Set', Parameters)
         cursor.execute('select @_sp_Location_Set_8')
         df_location = cursor.fetchone()
         return df_location


    def get_address(self):
        cursor = connection.cursor()
        Parameters = (self.address_gid,self.entity_gid, '')
        cursor.callproc('sp_Address_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_add = pd.DataFrame(rows, columns=columns)
        return df_add

    def setRouteDtl(self):
        cursor = connection.cursor()
        parameters = (self.action,self.json_employee_gid, self.routeHead_gid, self.route_code,self.route_name,self.remark,self.jsonData
                      ,self.entity_gid,self.create_by,'')
        cursor.callproc('sp_Route_Set', parameters)
        cursor.execute('select @_sp_Route_Set_9')
        output_msg = cursor.fetchone()
        return output_msg

    def getRouteDtl(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.routeHead_gid, self.route_name, self.route_code, self.json_employee_gid,
                      self.json_cluster_gid,self.entity_gid, '')
        cursor.callproc('sp_Route_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_add = pd.DataFrame(rows, columns=columns)
        return df_add

    def getHierarchy(self):
        cursor = connection.cursor()
        Parameters = (self.action,self.entity_gid,'')
        cursor.callproc('sp_Hierarchy_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_hier = pd.DataFrame(rows, columns=columns)
        return df_hier

    def setCluster(self):
        cursor = connection.cursor()
        parameters = (
            self.action, self.cluster_gid, self.cluster_name, self.cluster_parent_gid, self.hierarchy_gid,
            self.entity_gid,
            self.Employee_gid, '')
        cursor.callproc('sp_Cluster_Set', parameters)
        cursor.execute('select @_sp_Cluster_Set_7')
        output_msg = cursor.fetchone()
        return output_msg

    def get_designation(self):
        cursor = connection.cursor()
        Parameters = (0, '', '',self.entity_gid)
        cursor.callproc('sp_Designation_Get', Parameters)
        columns = [d[0] for d in cursor.description]
        ldict = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return ldict

    def set_courier(self):
        cursor = connection.cursor()
        parameters = ()
        cursor.callproc('sp_Courier_Set', parameters)
        cursor.execute('seelct @_sp_Courier_Set_123')
        output_msg = cursor.fetchone()
        return output_msg

    def set_contact(self):
        cursor = connection.cursor()
        Parameters = (
        self.action, self.contact_gid, self.cont_refcode, self.cont_refgid, self.contacttype_gid, self.conper1,
        self.designation_gid, self.landline_no,
        self.landline_no1, self.mobile_no, self.mobile_no1, self.email, self.cont_dob, self.wedding_day,
        self.entity_gid, self.create_by, '')
        cursor.callproc('sp_Contact_Set', Parameters)
        cursor.execute('select @_sp_Contact_Set_16')
        df_contset = cursor.fetchone()
        return df_contset

    def set_employee(self):
        cursor = connection.cursor()
        Parameters = (
        self.action, self.employee_gid, self.employee_code, self.employee_name, self.gender, self.emp_dob,
        self.emp_doj, self.department_gid,
        self.designation_gid, self.emp_sup_name, self.emp_sup_gid, self.address_gid, self.emp_mobileno, self.email,
        self.hierarchy_gid,self.jsonData, self.entity_gid, self.create_by, '')
        cursor.callproc('sp_Employee_Set', Parameters)
        cursor.execute('select @_sp_Employee_Set_18')
        df_empset = cursor.fetchone()
        return df_empset

        # Product

    def get_category(self):
        cursor = connection.cursor()
        Parameters = (0, '')
        cursor.callproc('sp_ProductCategory_Get', Parameters)
        columns = [d[0] for d in cursor.description]
        ldict = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return ldict

    def getproduct_types(self):
        cursor = connection.cursor()
        Parameters = (self.prodcat_gid)
        cursor.callproc('sp_Prodcat_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_add = pd.DataFrame(rows, columns=columns)
        return df_add

    def getmetadata(self):
        cursor = connection.cursor()
        Parameters = (self.table_name, self.column_name, self.entity_gid,'')
        cursor.callproc('sp_Metadata_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_metadata = pd.DataFrame(rows, columns=columns)
        return df_metadata

    def set_customergroup(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.custgrp_gid, self.custgrp_code, self.custgrp_name, self.address_gid, self.conper1,
                      self.desig1, self.mobile_no, self.landline_no, self.conper2, self.desig2, self.mobile_no1,
                      self.landline_no1,self.client_gid,
                      self.entity_gid, self.create_by, '')
        cursor.callproc('sp_Customergroup_Set', Parameters)
        cursor.execute('select @_sp_Customergroup_Set_16')
        df_custset = cursor.fetchone()
        return df_custset

    def set_ip(self):
        cursor = connection.cursor()
        jsn = json.dumps(self.jsonData)
        Parameters = (self.action,jsn,
                      self.entity_gid, self.create_by, '')
        cursor.callproc('sp_Login_Set', Parameters)
        cursor.execute('select @_sp_Login_Set_4')
        df_custset = cursor.fetchone()
        return df_custset



    def suppliercode(self):
        cursor = connection.cursor()
        Parameters = ('WITHOUT_DATE',self.array,'00','2', '')
        cursor.callproc('sp_Generatecode_Get', Parameters)
        cursor.execute('select @_sp_Generatecode_Get_4')
        df_custset = cursor.fetchone()
        return df_custset

    def getexecmapping(self):
        cursor = connection.cursor()
        Parameters = (self.action,self.employee_gid,self.entity_gid,'')
        cursor.callproc('sp_ExecutiveMapping_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_add = pd.DataFrame(rows, columns=columns)
        return df_add

    def set_exemapping(self):
        cursor=connection.cursor()
        jsondata=self.exemapjson
        exemapjson=json.dumps(jsondata)
        Parameters=(self.action,exemapjson,self.from_date,self.to_date,self.entity_gid,self.employee_gid,'')
        cursor.callproc('sp_ExecutiveMapping_Set',Parameters)
        cursor.execute('select @_sp_ExecutiveMapping_Set_6')
        df_exemap=cursor.fetchone()
        return df_exemap

    def getcustomersales(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.name, self.jsonData, self.entity_gid,'')
        cursor.callproc('sp_CustomerSales_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_custset = pd.DataFrame(rows, columns=columns)
        return df_custset

    def getentity(self):
        cursor = connection.cursor()
        parameters = (self.action, self.type, self.jsonData, self.entity_gid,'')
        cursor.callproc('sp_EntityOutcome_Get', parameters)
        column_names = [col[0] for col in cursor.description]  # Get column names from MySQL
        rows = cursor.fetchall()
        rows = list(rows)
        df1_data = pd.DataFrame(rows, columns=column_names)
        cursor.nextset()
        column_names = [col[0] for col in cursor.description]  # Get column names from MySQL
        rows = cursor.fetchall()
        rows = list(rows)
        df2_data = pd.DataFrame(rows, columns=column_names)
        cursor.nextset()
        column_names = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df3_data = pd.DataFrame(rows, columns=column_names)
        cursor.close()
        df4_data = [df1_data, df2_data, df3_data]
        return df4_data

    def getcreditapprv(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.name, self.jsonData, self.entity_gid, '')
        cursor.callproc('sp_Creditapproval_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_custset = pd.DataFrame(rows, columns=columns)
        return df_custset

        # def get_pendingsummary_get(self):
        #     api_url_base = 'http://192.168.1.10/sally_api/api/Purchase/Getpendingsmry'
        #     api_url = api_url_base
        #     parameters = {'li_cust_gid': self.customer_gid}
        #     response = requests.get(api_url, params=parameters)
        #     if response.status_code == 200:
        #         return json.loads(response.content.decode('utf-8'))
        #     else:
        #         return None

    def get_pendingsummary_get(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.customer_gid, '')
        cursor.callproc('sp_FETPaymentQueue_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_custset = pd.DataFrame(rows, columns=columns)
        return df_custset

    def getactivitytrend(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.jsonData, self.entity_gid, '')
        cursor.callproc('sp_ActivityTrend_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_custset = pd.DataFrame(rows, columns=columns)
        return df_custset

    def mailquery_get(self):
        cursor = connection.cursor()
        parameters = (self.mail_headergid,self.mail_headername,self.mail_detailgid)
        cursor.callproc('sp_Mailquery_get',parameters)
        columns =  [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows =  list(rows)
        querydata = pd.DataFrame(rows,columns=columns)
        return querydata

    def set_MailTemplte(self):
        cursor = connection.cursor()
        Template_json = json.dumps(self.Template_json)
        parameters = (
        self.action, self.type, Template_json, self.employee_gid, self.entity_gid,
        '')
        cursor.callproc('sp_Mailtemplate_set', parameters)
        cursor.execute('select @_sp_Mailtemplate_set_5')
        output_msg = cursor.fetchone()
        return output_msg

    def mailtemplate_get(self):
        cursor = connection.cursor()
        parameters = (self.mail_templategid,self.mail_templatename,self.mail_templatecode)
        cursor.callproc('sp_Mailtemplate_get',parameters)
        columns =  [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows =  list(rows)
        tempdata = pd.DataFrame(rows,columns=columns)
        return tempdata

    def set_taxdetails(self):
        cursor = connection.cursor()
        Parameters = (self.action,self.taxdtl_gid,self.tax_code,self.subtax_name,self.ref_name,self.tax_type,self.reftbl_code,self.gstno,self.entity_gid,self.create_by,'')
        cursor.callproc('sp_Taxdetails_Set',Parameters)
        cursor.execute('select @_sp_Taxdetails_Set_10')
        df_taxdtl=cursor.fetchone()
        return df_taxdtl

    def get_unique(self):
        cursor = connection.cursor()
        Parameters = (self.action,self.type,self.json_unique,self.entity_gid,'')
        cursor.callproc('sp_UniqueCode_Get',Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_unique = pd.DataFrame(rows,columns=columns)
        return df_unique

    def get_taxdetails(self):
        cursor = connection.cursor()
        Parameters = (self.type,self.group,self.json_unique,self.entity_gid,'')
        cursor.callproc('sp_Taxdetails_Get',Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_taxdetl = pd.DataFrame(rows,columns=columns)
        return df_taxdetl

    def set_cmddetails(self):
        cursor = connection.cursor()
        jsondata = self.jsonData
        CMD_JSON = json.dumps(jsondata)
        Parameters = (self.action,self.type,CMD_JSON,self.entity_gid,self.create_by,'')
        cursor.callproc('sp_Comments_Set',Parameters)
        cursor.execute('select @_sp_Comments_Set_5')
        df_taxdtl=cursor.fetchone()
        return df_taxdtl

    def get_cmddetails(self):
        cursor = connection.cursor()
        jsondata = self.jsonData
        CMD_JSON = json.dumps(jsondata)
        Parameters = (self.action,self.type,CMD_JSON,self.entity_gid,'')
        cursor.callproc('sp_Comments_Get',Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_cmddtel = pd.DataFrame(rows,columns=columns)
        return df_cmddtel

    def set_city(self):
        cursor = connection.cursor()
        jsondata = self.jsonData
        cityjson = json.dumps(jsondata)
        Parameters = (self.action, cityjson, self.entity_gid, self.create_by, '')
        cursor.callproc('sp_City_Set', Parameters)
        cursor.execute('select @_sp_City_Set_4')
        df_cityset = cursor.fetchone()
        return df_cityset

    def dayrouteset(self):
        cursor = connection.cursor()
        parameters = (self.action, json.dumps(self.jsonData),
                      self.entity_gid, self.create_by, '')
        cursor.callproc('sp_Dayvisit_Set', parameters)
        cursor.execute('select @_sp_Dayvisit_Set_4')
        output_msg = cursor.fetchone()
        return output_msg

    def dayrouteget(self):
        cursor = connection.cursor()
        parameters = (self.action, self.employee_gid, self.from_date, self.to_date, self.entity_gid, '')
        cursor.callproc('sp_Dayvisit_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        output_msg = pd.DataFrame(rows, columns=columns)
        return output_msg

    def set_supplierproductmap(self):
        cursor = connection.cursor()
        jsondata = self.jsonData
        supplierratejson = json.dumps(jsondata)
        Parameters = (self.action, supplierratejson, self.entity_gid, self.create_by, '')
        cursor.callproc('sp_SupplierProductMap_Set', Parameters)
        cursor.execute('select @_sp_SupplierProductMap_Set_4')
        df_supplierproductmap = cursor.fetchone()
        return df_supplierproductmap

    def get_productnames(self):
        cursor = connection.cursor()
        parameters = (self.action,self.date, self.supplier_gid, self.product_gid, self.char_active, '')
        cursor.callproc('sp_SupplierProductMap_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        data = pd.DataFrame(rows, columns=columns)
        return data

# client
    def get_client(self):
        cursor = connection.cursor()
        Parameters = (self.client_gid, self.client_name, self.client_code, self.entity_gid)
        cursor.callproc('sp_Client_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_customer = pd.DataFrame(rows, columns=columns)
        return df_customer

    def set_client(self):
        cursor = connection.cursor()
        jsondata = self.jsonData
        clientjson = json.dumps(jsondata)
        Parameters = (self.action, self.type, clientjson, self.entity_gid, self.create_by, '')
        cursor.callproc('sp_Client_Set', Parameters)
        cursor.execute('select @_sp_Client_Set_5')
        df_cityset = cursor.fetchone()
        return df_cityset

    def set_courierdetails(self):
        cursor = connection.cursor()
        Parameters = (
        self.action, self.jsondata, self.cust_courier_gid, self.customer_gid, self.courier_gid, self.remark, self.from_date,
        self.to_date, self.entity_gid, self.create_by, '')
        cursor.callproc('sp_CustcourierMap_set', Parameters)
        cursor.execute('select @_sp_CustcourierMap_set_10')
        df_courierdtl = cursor.fetchone()
        return df_courierdtl

    def get_Version(self):
        cursor=connection.cursor()
        Parameters=(self.action,self.version_flag,self.entity_gid,'')
        cursor.callproc('sp_Version_Get',Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_version = pd.DataFrame(rows, columns=columns)
        return df_version

    def get_campaign(self):
        cursor = connection.cursor()
        Parameters = (self.type, self.sub_type, self.jsonData,self.json_classification, '')
        cursor.callproc('sp_Campaign_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_campaign = pd.DataFrame(rows, columns=columns)
        return df_campaign

    def get_CCBS_Master(self):
        cursor = connection.cursor()
        Parameters = (self.type, self.sub_type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_CCBS_Master_Get', Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_cam = pd.DataFrame(rows, columns=columns)
        return df_cam

    def set_cat_subcat_Master(self):
        cursor = connection.cursor()
        Parameters = (self.type, self.sub_type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Cat_Subcat_Master_set', Parameters)
        cursor.execute('select @_sp_Cat_Subcat_Master_set_4')
        dff = cursor.fetchone()
        return dff

    def set_CCBS_Master(self):
        cursor = connection.cursor()
        Parameters = (self.type, self.sub_type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_CCBS_Master_Set', Parameters)
        cursor.execute('select @_sp_CCBS_Master_Set_4')
        df_CCBS = cursor.fetchone()
        return df_CCBS

    def get_Logindetail(self):
        cursor=connection.cursor()
        jsondata=json.dumps(self.jsondata)
        Parameters=(self.action,self.type,jsondata,self.entity_gid,'')
        cursor.callproc('sp_Logindetails_Get',Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_logindetails = pd.DataFrame(rows, columns=columns)
        return df_logindetails

    def get_StatePrice(self):
        cursor=connection.cursor()
        jsondata = self.json_filters
        Parameters=(self.type,self.sub_type,jsondata,self.json_classification,self.create_by,'')
        cursor.callproc('sp_StatePrice_get',Parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_States = pd.DataFrame(rows, columns=columns) 
        json_data = {}
        cursor.execute('select @_sp_StatePrice_get_5')
        out_put = cursor.fetchone()
        if out_put[0] == 'FOUND':
            json_data = json.loads(df_States.to_json(orient='records'))
        return json_data


    def get_AllProduct(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.jsonData,self.json_classification, '')
        cursor.callproc('sp_ProductALL_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_dp = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_ProductALL_Get_4')
        sp_out_message = cursor.fetchone()
        return {"DATA":df_dp,"MESSAGE":sp_out_message[0]}

    def get_classification_summary(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.jsonData, self.json_classification, '')
        cursor.callproc('sp_Classification_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        cursor.execute('select @_sp_Classification_Get_4')
        outmsg_sp = cursor.fetchone()
        rows = list(rows)
        df_ta = pd.DataFrame(rows, columns=columns)
        return {"DATA": df_ta, "MESSAGE": outmsg_sp[0]}

    def get_Supplier(self):
        cursor = connection.cursor()
        parameters = (self.type, self.sub_type, self.json_supplier, self.json_classification, '')
        cursor.callproc('sp_Supplier_Get', parameters)
        columns = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        rows = list(rows)
        df_supp = pd.DataFrame(rows, columns=columns)
        cursor.execute('select @_sp_Supplier_Get_4')
        sp_out_message = cursor.fetchone()
        return {"DATA": df_supp, "MESSAGE": sp_out_message[0]}

    def set_Supplier(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.json_supplier, self.json_address, self.json_contact, self.json_clasfication,'')
        cursor.callproc('sp_SupplierSPS_Set', Parameters)
        cursor.execute('select @_sp_SupplierSPS_Set_5')
        df_supplier = cursor.fetchone()
        return df_supplier

    def Set_Productcat(self):
        cursor = connection.cursor()
        Parameters = (self.action, self.type, self.jsonData, '')
        cursor.callproc('sp_ProductNew_Set', Parameters)
        cursor.execute('select @_sp_ProductNew_Set_3')
        df_productcat = cursor.fetchone()
        return df_productcat

    def set_citys(self):
        cursor = connection.cursor()
        parameters = (self.Action, self.City, self.Entity_gid, self.Emp_gid, '')
        cursor.callproc('sp_City_Set', parameters)
        cursor.execute('select @_sp_City_Set_4')
        msg = cursor.fetchone()
        return msg

    def set_state(self):
        cursor = connection.cursor()
        parameters = (self.Action, self.Type, self.filter, self.classification, self.Emp_gid, '')
        cursor.callproc('sp_State_Set', parameters)
        cursor.execute('select @_sp_State_Set_5')
        msg = cursor.fetchone()
        return msg