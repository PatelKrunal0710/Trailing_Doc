from django.urls import path
from . import views

urlpatterns = [
    path('',views.loginpage,name="loginpage"),
    path('Fileupload',views.Fileupload,name="Fileupload"),
    path('Checklist',views.Checklist,name="Checklist"),
    path('Chk_save',views.Chk_save,name="Chk_save"),
    path('faildoc',views.faildoc,name="faildoc"),
    path('chkmaster',views.chkmaster,name="chkmaster"),
    path('Dashboard',views.pdashboard,name="Dashboard"),
    path('Qc',views.Qc,name="Qc"),
    path('qcChk_save',views.qcChk_save,name="qcChk_save"),
]