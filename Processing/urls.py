from django.urls import path
from . import views

urlpatterns = [
    path('',views.loginpage,name="loginpage"),
    path('Fileupload',views.Fileupload,name="Fileupload"),
    path('Checklist',views.Checklist,name="Checklist"),
    path('Chk_save',views.Chk_save,name="Chk_save"),
    path('faildoc',views.faildoc,name="faildoc"),
]