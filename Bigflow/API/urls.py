from django.urls import path
from Bigflow.API import views as view, view_atma
from Bigflow.API import view_service as view_service
from Bigflow.API import view_master as view_master
from Bigflow.API import view_sales as view_sales
from Bigflow.API import view_report as view_report
from Bigflow.Report import views_API as view_stock
from Bigflow.API import view_Claim as view_Claim
from django.conf.urls import url, include
from Bigflow.API import view_purchase as view_purchase
from Bigflow.API import view_fa as view_fa
from Bigflow.API import  view_branchexp as view_branchexp

from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('login/', view.login.as_view()),
    path('Change_Password', view.Change_Password.as_view()),
    path('user_rights', view.UM_RightsMenu.as_view()),
    path('FET_Schedule', view.FET_Schedule.as_view()),
    path('FET_ScheduleHistory', view.FET_ScheduleHistory().as_view()),
    path('TEST', view.TEST.as_view()),
    path('CustomerFilter', view.FET_Customer_Filter.as_view()),
    path('Customer_Mapped', view.Customer_Mapped.as_view()),
    path('FET_Schedule_Set', view.FET_Schedule_Set.as_view()),
    path('FET_SalesOrder', view.FET_SalesOrder.as_view()),  ## To Save the Sales
    path('FET_SalesOrder_Get', view.FET_SalesOrder_Get.as_view()),
    path('FETScheduleCustomer', view.ScheduleCustomerFET.as_view()),
    path('FET_Schedule_Update', view.FET_Schedule_Update.as_view()),
    path('Direct_Outcome_Summary', view.Direct_Outcome_Summary.as_view()),
    ##FET Review.
    path('FET_Review', view.FET_Review.as_view()),
    path('FET_ReviewApprove_set', view.FET_ReviewApprove.as_view()),
    path('FET_ReviewProcess', view.FET_ReviewProcess.as_view()),
    ## APPROVE
    path('FET_Approve', view.FET_Approve.as_view()),
    # Master
    path('Schedule_Master', view.Schedule_Master.as_view()),
    path('Product_Sales', view.Product_Sales.as_view()),
    path('Product_SalesFav', view.Product_Sales_Favourite.as_view()),
    path('Employee_Profile', view.Employee_Profile.as_view()),
    path('Customerview_get', view.Customer_view_get.as_view()),
    path('Release_Version_Get', view.FET_Version.as_view()),
    path('Campaign_API_Get', view_master.Campaign_API.as_view()),
    path('All_Tables_Values_Get', view_master.All_Tables_Values_Get.as_view()),
    path('StatePrice_API_Get', view_master.StatePrice_API.as_view()),
    path('ccbsapi', view_master.CCBS_MASTER.as_view()),
    path('ProductCat_type_Set', view_master.ProductCat_type_Set.as_view()),
    path('Supplier_Mast', view_master.Supplier_Master.as_view()),
    path('Product_Master', view_master.Product_Master.as_view()),

    ### Sales Master
    path('Dealer_Price_API', view_sales.Dealer_Price_API.as_view()),
    path('Rate_Card_API', view_sales.Rate_Card_API.as_view()),

    ##Location
    path('LatLong_Set', view.LatLong.as_view()),
    ### Files
    path('FileUpload', view.FileUpload.as_view()),
    path('LatLongFET', view.Get_position.as_view()),
    ### Service,
    path('Service_SetAPI', view_service.Service_SetAPI.as_view()),
    path('Service_SummaryGetAPI', view_service.Service_SummaryGetAPI.as_view()),
    path('CourierName_get', view_service.CourierName_get.as_view()),
    path('Dispatch_set_API', view_service.Dispatch_set.as_view()),
    path('Sales_Dispatch', view_service.Dispatch_set.as_view()),

    ### Stock
    path('Stock_GetAPI', view.Stock_GetAPI.as_view()),
    path('Stock_SetAPI', view.Stock_SetAPI.as_view()),
    ### Common.
    path('Comment', view.Comment.as_view()),
    path('DeviceDetails', view.DeviceDetails.as_view()),
    path('LoginDetails', view.Login_Get.as_view()),
    path('DispatchProcess_Get', view_sales.Dispatch_Process.as_view()),
    path('DispatchProcess_Set', view_sales.Dispatch_Process.as_view()),

    # sales
    path('Salesplanset', view.sales_planning_Set.as_view()),
    path('Salesplanget', view.sales_planning_Get.as_view()),
    path('Salesplan_misget', view.sales_planningMIS.as_view()),
    path('Salesplan_History', view.sales_planning_history.as_view()),
    path('Salesplan_Report', view.sales_planning_Report.as_view()),

    path('SalesOrder_APIGet', view_sales.SalesOrder_Register.as_view()),
    path('SalesInv_Process_set', view_sales.Sales_Invoice_Process.as_view()),
    path('apiurl_Query_SummarySales', view_sales.Query_Summary.as_view()),
    path('apiurl_Query_SummarySalesProduct', view_sales.Query_SummaryProduct.as_view()),
    path('apiurl_Query_SummaryCollection', view_sales.Query_SummaryCollection.as_view()),
    path('apiurl_Query_SummaryOutstanding', view_sales.Query_SummaryOutstanding.as_view()),
    path('apiurl_query_summary_getcollectionstatus', view_sales.Query_Summarygetcollectionstatus.as_view()),

    # purchase
    path('PurchaseRequest_Set', view.Purchase_request_API.as_view()),
    # path('Alltable_ccbs', view.Purchase_request_API.as_view()),

    ### Report_Customer_Performance
    path('Report_Total_Sales', view_sales.Customer_Performance_Report.as_view()),

    # check_in check_out
    path('Check_In_Check_Out', view.Check_In_Check_Out.as_view()),

    # Dispatch
    path('Invoice_Dispatch_API', view_sales.Invoice_Dispatch.as_view()),
    # Stock
    path('Stock_Summary_API', view_stock.StockAPI.as_view()),

    # Carton
    path('All_product_get', view_master.All_Product_Get.as_view()),
    path('Delmat_set', view_purchase.Delmat.as_view()),
    path('Alltable_ccbs', view_purchase.Alltable_ccbs.as_view()),

    ## TA - claim
    path('Claim_Initial', view_Claim.TA_Initial.as_view()),
    path('Scanning', view_Claim.ScanModule.as_view()),
    # Classification
    path('Classification_Get', view_master.Classification_Get.as_view()),

    ### Control Sheet
    path('Control_Sheet', view_report.Control_Sheet.as_view()),

    #### Cluster
    path('cluster_Master', view_master.cluster_Master.as_view()),
    #### Scan Barcode
    path('File_Upload_Barcode', view.File_Save.as_view()),



    ## FA
    # path('FA_Summary', view_fa.FAApi.as_view()),
    # path('FA_MAKER', view_fa.FA_Asset_Make.as_view()),
    # path('FA_TRAN', view_fa.FA_Tran.as_view()),
    # path('FA_LOCATION', view_fa.FA_Location.as_view()),
    # path('FA_CATEGORY', view_fa.FA_Category.as_view()),


    ##Atma
    path('GET_ATMA_Data', view_atma.GET_ATMA_Data.as_view()),
    path('GET_ATMA_Directors_Data', view_atma.GET_ATMA_Directors_Data.as_view()),
    path('atmaPartnerPayment_Setapi', view_atma.atmaPartnerPayment_Setapi.as_view()),
    path('atmaAttachment_apiurl', view_atma.atma_AttachmentApi_get.as_view()),
    path('atma_Docgroup_Setapi', view_atma.atma_Docgroup_Set.as_view()),
    path('atma_Updateattachment', view_atma.atma_Updateattachment.as_view()),
    path('atma_Activitydetails_Set', view_atma.atma_Activitydetails_Set_api.as_view()),
    path('atma_Activitydetails_Get', view_atma.atma_Activitydetails_Get_api.as_view()),
    path('Gettaxdetails', view_atma.Gettaxdetails.as_view()),
    path('atma_Activityget', view_atma.atma_Activityget.as_view()),
    path('atma_ActivitySet_APIurl', view_atma.atma_ActivitySet_API.as_view()),
    path('atma_clientdetails_api', view_atma.atma_clientdetails_api.as_view()),
    path('atma_contractdetails_api', view_atma.atma_contractdetails_api.as_view()),
    path('atma_branchdetails_api', view_atma.atma_branchdetails_api.as_view()),
    path('atma_basicprofiledetails_api', view_atma.atma_basicprofiledetails_api.as_view()),
    path('atma_getcheckerdetails_api', view_atma.atma_getcheckerdetails_api.as_view()),
    path('atmaCatalog_Setapi', view_atma.atmaCatalog_Setapi.as_view()),
    path('atmaCatalog_Getapi', view_atma.atmaCatalog_Getapi.as_view()),
    path('Prmaker_Setapi', view_atma.Prmaker_Set.as_view()),
    path('PRMAKERapi',view_atma.PRMAKER.as_view()),
    path('atma_profileproduct_getapi', view_atma.Partnerproductapi_get.as_view()),
    path('atma_profileproduct_setapi', view_atma.Partnerproductapi_set.as_view()),
    path('PartnerdeactivateSet_api', view_atma.Partnerdeactivateapi_Set.as_view()),
    path('approval_stagesapi', view_atma.approval_stagesapi.as_view()),
    path('approval_paartnergetapi', view_atma.approval_paartnergetapi.as_view()),
    path('Partnerapproval',view_atma.Partnerapproval.as_view()),
    path('Partnerdisapproval',view_atma.Partnerdisapproval.as_view()),
    path('Update_changerequest_API',view_atma.Update_changerequest_API.as_view()),


#BranchExp

    # path('Br_Property_Proccess_Get', view_branchexp.Property_Process.as_view()),
    # path('Br_Property_Proccess_Set',view_branchexp.Property_Process_Set.as_view()),
    # path('Br_property_Details',view_branchexp.Property_Process.as_view()),
    # path('Expense_Process',view_branchexp.Expense_Process.as_view()),
    # path('Expense_ProcessSet',view_branchexp.Expense_Process_Set.as_view()),

    #Master
    # path('Master_State_Details',view.State_Process_Set.as_view())
]
