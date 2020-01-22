from django.urls import path
from Bigflow.Report import views as report

urlpatterns = [
    path('stocksummary/', report.StockSummaryIndex, name="stock"),
    path('FourLineMis/', report.Four_Line_Mis, name="Four_Line_Mis"),
    path('getsalesandoutstanding/', report.get_totalsales_and_totaloutstanding, name='getsalesandoutstanding'),
    path('stockgett/', report.StockSum, name="stock"),
    path('ovralreport/', report.outstandingReportIndex, name="ovralreport"),
    path('outstandingExcel/', report.outstandingExcel, name='outstanding download'),
    path('querysummary/', report.querysummaryIndex, name='querysummary'),
    path('setupdate/', report.setupdate, name='setupdate'),
    path('salecontrolsheet/', report.Controlsheet, name='Controlsheet'),
    path('Control_Sheet/', report.Control_Sheet, name='Control_Sheet'),
    path('controlsheetsummary/', report.Control_Sheet_summary, name='Control_Sheet_summary'),
    path('getControl_Sheet/', report.getControl_Sheet, name='getControl_Sheet'),
    path('getComparesale/', report.getComparesale, name='getComparesale'),
    path('outstandingcontrolsheet/', report.os_Controlsheet, name='os_Controlsheet'),
    path('stockcontrolsheet/', report.stock_controlsheet, name='stock_controlsheet'),
    path('performance_getexcel/', report.performance_excel, name='performance_getexcel'),
    path('getCompareos/', report.getCompareos, name='getCompareos'),
    path('stock_sumry_rpt/',report.stcksumry_overall_rept,name='stcksumry_overall_rept'),

]
