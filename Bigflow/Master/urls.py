from django.urls import path
from Bigflow.Master import views
from Bigflow.Transaction import views as transactionview

urlpatterns = [
    path('texteditor/', views.texteditor, name='texteditor'),
    path('userreport/', views.userreport, name='userreport'),
    path('trandatadetails/', views.trandatadetails, name='trandatadetails'),
    path('mailtemplate/', views.mailtemplate, name='mailtemplate'),
    path('mailtemplatesummary/',views.mailtemplatesummary, name='mailtemplatesummary'),
    path('sendmailTemplate/', views.sendmailTemplate, name='sendmailTemplate'),
    path('Templatecreation/', views.Templatecreation, name='Templatecreation'),
    path('EditTemplate/', views.EditTemplate, name='EditTemplate'),
    path('getquerydata/', views.getquerydata, name='getprocessdata'),
    path('MailTemplate_set/',views.MailTemplate_set, name='MailTemplate_set'),
    path('getTemplatedata/', views.getTemplatedata , name='getTemplatedata'),
    path('commentget/',views.commentget,name='commentget'),
    path('commentset/',views.commentset,name='commentset'),
    path('execmappingexcel/',views.execmapping_excel,name='execmapping_excel'),
    path('ddlempexec/',views.employee_executive,name='ddlempexec'),
    path('ddlempexecall/',views.employee_allexecutive,name='ddlempexecall'),
    path('supplier/',views.supplierIndex,name='supplier'),
    path('suppliersummary/',views.supplierSumryIndex,name='suppliersummary'),
    path('productadd/',views.productadd, name='productadd'),
    path('productorservice/',views.productorservice, name='productorservice'),
    path('productdetails/',views.productdetails,name='productdetails'),
    path('categoryget/', views.categoryget, name='categoryget'),
    path('typeget/', views.typeget, name='typeget'),
    path('producttypeset/', transactionview.producttypeset, name='producttypeset'),
    path('productadd/', views.productadd, name='productadd'),
    path('Productsmry/', transactionview.Productsmry, name='Productsmry'),
    path('popupcarton/', views.Product_Add_Popupcarton, name="Product_Add_Popupcarton"),
    path('suppliermaster/',views.Supplier_Master,name='Supplier_Master'),
    path('popup3/', views.Product_Type_Popup, name="Product_Type_Popup"),
    path('popup2/', views.Product_Add_Popup, name="Product_Add_Popup"),
    path('supplierdetails/',views.supplierdetails,name='supplier_details'),
    path('set_state_dist_city_pincode/',views.SetCityPincode,name='Adding_New_City_Pincode'),
    path('empactinact/', views.empactinact, name='employee_active_inactive'),


    ]
