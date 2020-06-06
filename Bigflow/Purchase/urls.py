from django.conf.urls import url
from django.urls import path
from Bigflow.Purchase import views
from Bigflow.Transaction import views as transaction

urlpatterns = [
    # from Bigflow.Purchase import urls as PurchaseUrl
    # path('', include(PurchaseUrl)),
    path('PO_Approval/', views.POApproval_Index, name='POApproval_index'),
    path('createpoindex/', views.createpoindex, name='createpoindex'),
    path('PurchasePlanning/', views.PurchasePlanningIndex, name='PurchasePlanning'),
    path('pr_supplier/', views.pr_supplierIndex, name='pr Supplier Allocation'),
    path('openpo/', views.open_po, name='open_po'),
    path('prheader_ccbs/', views.prheader_ccbs, name='prheader_ccbs'),
    path('openpoedit/', views.openpo_edit, name='openpo_edit'),
    path('pdfviewer/', views.pdfviewer, name='pdfviewer'),
    path('pdfviewer2/', views.pdfviewer2, name='pdfviewer2'),

    path('pdfedit/', views.pdfedit, name='pdfedit'),
    path('commosave/', views.commosave, name='commosave'),
    path('commodity_generate_code/',views.commodity_code_gen,name='commodity_code_gen'),
    path('supplierdropdown/', views.supplier_dropdown, name='supplier_dropdown'),
    path('prdetails_ccbsget/', views.prdetails_ccbs, name='prdetails_ccbs'),
    path('commodity/', views.commodity, name='commodity'),
    path('commodityadd/', views.commodityadd, name='commodityadd'),
    path('commoditydropdown/', views.commoditydropdown, name='commoditydropdown'),
    path('commo_product/', views.commo_product, name='commo_product'),
    path('commo_product_name/', views.commo_product_name, name='commo_product_name'),

    #delmat
    path('delmat/', views.delmat, name='delmat'),
    path('adddelmat/', views.adddelmat, name='adddelmat'),
    path('delmattype/', views.delmattype, name='delmattype'),
    path('delmatsavedatas/', views.delmatsavedatas, name='delmatsavedatas'),
    path('delmatget/', views.delmatget, name='delmatget'),
    path('delmatupdate/', views.delmatupdate, name='delmatupdate'),
    path('branchresult/', views.branchresult, name='branchresult'),
    path('delmatapproval/', views.delmatapproval, name='delmatapproval'),
    path('delmatapprovalsmry/', views.delmatapprovalsmry, name='delmatapprovalsmry'),
    path('tranapproval/', views.tranapproval, name='tranapproval'),
    path('alltable/', views.alltable, name='alltable'),
    path('trandatadetails1/', views.trandatadetails1, name='trandatadetails1'),
    path('reftable/', views.reftable, name='reftable'),
    # path('godownddl/', views.godownddl, name='godownddl'),


    path('pending_posummary/', views.pending_posummary, name='pending_posummary'),
    path('agentsummary/', views.agentsummary, name='agentsummary'),
    path('getfinalapproval/', views.getfinalapproval, name='getfinalapproval'),
    path('Newdelmat/', views.New_delmat_Get, name='NewdelmatGet'),
    path('Prdraftdata/', views.Prdraftdata, name='Prdraftdata'),

    path('prfinalapproval/', views.prfinalapproval, name='prfinalapproval'),
    path('openpo_getexcel/', views.openpo_getexcel, name='openpo_getexcel'),
    path('pr_maker/', views.purchasesmry, name='purchasesmry'),
    path('purchasecrte/', views.purchasecrte, name='purchasecrte'),
    path('pr_approve/', views.approvalsmry, name='approvalsmry'),
    path('po_delievery/', views.po_delievery_popup, name='po_delievery'),
    path('codegenerate/', views.codegenerationviews, name='codegenerate'),
    path('approvalview/', views.approvalview, name='approvalview'),
    path('purchase/', views.purchase ,name='purchase'),
    path('Prapproval_get/', views.Prapproval_get, name='Prapproval_get'),
    path('purchasesmryget/', views.purchasesmryget, name='purchasesmryget'),
    path('PO_Close_Maker/', views.poclosesmry, name='poclosesmry'),
    path('poclosecrte/', views.poclosecrte, name='poclosecrte'),
    path('PO_CancelMaker/', views.pocancelsmry, name='pocancelsmry'),
    path('pocancelcrte/', views.pocancelcrte, name='pocancelcrte'),
    path('PO_Reopen_Maker/', views.poreopensmry, name='poreopensmry'),
    path('poreopencrte/', views.poreopencrte, name='poreopencrte'),
    path('PO_Close_Approve/', views.poapprvlclssmry, name='poapprvlclssmry'),
    path('poapprvlclscrt/', views.poapprvlclscrt, name='poapprvlclscrt'),
    path('GRN_Maker/', views.grnsmry, name='grnsmry'),
    path('grncreate/', views.grncreate, name='grncreate'),
    path('GRN_Approver/', views.grnaprvlsmry, name='grnaprvlsmry'),
    path('grnaprvlcreate/', views.grnaprvlcreate, name='grnaprvlcreate'),
    path('PO_Cancel_Approve/', views.poapprvlcnclsmry, name='poapprvlcnclsmry'),
    path('poapprvlcnclcrt/', views.poapprvlcnclcrt, name='poapprvlcnclcrt'),
    path('Poapproval_get/', views.Poapproval_get, name='Poapproval_get'),
    path('porejectt/', views.poreject, name='porejectt', ),
    path('ponewapproval/', views.ponewapproval_set, name='ponewapproval_set'),
    path('po_maker/', views.posummary, name='posummary'),
    path('Poheader_detail/', views.Poheader_detail, name='Poheader_detail'),
    path('Getpostatus/', views.Getpostatus, name='Getpostatus'),
    path('poheader_data/', views.po_headerget_view, name='po_headerget_view'),
    path('POApproval/', views.POApproval_create, name='POApproval'),
    path('POApproval_Details/', views.POApproval_detail, name='POApproval_detail'),
    path('Approval_PODetail/', views.Approval_PODetail, name='Approval_PODetail'),
    path('PODelivery_detail/', views.PODelivery_detail, name='PODElivery  Detail'),
    path('Approval_View_Update/', views.Approval_View_Update, name='Approval_View_Update', ),
    path('Approval_Update/', views.Approval_Update, name='Approval_Update'),
    path('pur_poclosesummary/', views.pur_poclosesummary, name='pur_poclosesummary'),
    path('pur_poreopensummary/', views.pur_poreopensummary, name='pur_poreopensummary'),
    path('purcappsryget/', views.purcappsryget, name='purcappsryget'),
    path('Prdetail_get/', views.Prdetail_get, name='Prdetail_get'),
    path('pr_po_delete/', views.pr_po_delete, name='pr_po_delete'),
    path('Prapproval_set/', views.Prapproval_set, name='Prapproval_set'),
    path('Poapproval_set/', views.Poapproval_set, name='Poapproval_set'),
    path('Prheader_Set/', views.Prheader_Set, name='Prheader_Set'),
    path('Productjson/', transaction.Productjson, name='Productjson'),
    path('Prdelete_Set/', views.Prdelete_Set, name='Prdelete_Set'),
    path('Dropdown_details/', views.Dropdown_details, name='Dropdown_details'),
    path('product_name/', views.product_name, name='product_name'),
    path('POQtyList/', views.POQtyList, name='POQtyList'),
    path('deliverydetail/', views.deliverydetail, name='deliverydetail'),
    path('POheader_Set/', views.POheader_Set, name='POheader_Set'),
    path('PR_to_POheader_Set/', views.PR_to_POheader_Set, name='PR_to_POheader_Set'),

    path('Getprstatus/', views.Getprstatus, name='Getprstatus'),
    path('getpoadmentment/', views.getpoadmentment, name='getpoadmentment'),
    path('po_ammentsummry/', views.po_ammentsummry, name='po_ammentsummry'),
    path('po_ammentcreate/', views.po_ammentcreate, name='po_ammentcreate'),
    path('getpoadmentmentapp/', views.getpoadmentmentapp, name='getpoadmentmentapp'),
    path('po_ammentapprovalsummry/', views.po_ammentapprovalsummry, name='po_ammentapprovalsummry'),
    path('pur_pocloseappsummary/', views.pur_pocloseappsummary, name='pur_pocloseappsummary'),
    path('get_grnheadersumry/', views.get_grnheadersumry, name='get_grnheadersumry'),
    path('get_grndetails/', views.get_grndetails, name='get_grndetails'),
    path('set_grnheader/', views.set_grnheader, name='set_grnheader'),
    path('set_grndetails/', views.set_grndetails, name='set_grndetails'),
    path('set_grnapproval/', views.set_grnapproval, name='set_grnapproval'),
    path('get_grnapprovalget/', views.get_grnapprovalget, name='get_grnapprovalget'),
    path('get_grnpoheaderdetails/', views.get_grnpoheaderdetails, name='get_grnpoheaderdetails'),
    path('get_grnheader/', views.get_grnheader, name='get_grnheader'),
    path('vendorselection/', views.vendorselection, name='vendorselection'),
    path('supplier_details/', views.supplier_details, name='supplier_details'),
    path('purchasedata/', views.purchasedata, name='purchasedata'),
    path('sup_capacity/', views.get_supCapacity, name='supplier capacity'),
    path('po_querystring/',views.po_querystring,name='po_querystring'),
    path('get_querystring/',views.get_querystring,name='get_querystring'),
    path('get_allqueue_status/',views.get_allqueue_status,name='get_allqueue_status'),
    path('set_PRDetails/',views.set_PRDetails,name='set_PRDetails for sales planning'),
    path('set_grn/', views.set_grn, name='set_grn'),
    path('get_grnprocess_details/', views.get_grnprocess_details, name='get_grnprocessdetails'),
    path('grn_details_view/', views.grndetailsview, name='grncreate'),
    path('get_grnprocessdetails/', views.get_grnprocessdetails, name='get_grnprocessdetails'),
    #PR
    path('pr_productcategory/',views.pr_productcategory,name='pr_productcategory'),
    path('pr_category_type/',views.pr_category_type,name='pr_category_type'),
    path('pr_product/',views.pr_product,name='pr_product'),
    path('commodity_pdata/',views.commodity_pdata,name='commodity_pdata'),
    path('saveccbs/',views.saveccbs,name='saveccbs'),
    path('get_SalesCount/',views.get_SalesCount,name='get_SalesCount'),
    path('get_Saleshstry/',views.get_Saleshstry,name='get_Saleshstry')
]