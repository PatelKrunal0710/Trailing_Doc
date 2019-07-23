from django.contrib import admin
from .models import Fileinfo,Checklist_Master,userprofile

# Register your models here.
admin.site.register(Fileinfo)
admin.site.register(Checklist_Master)
admin.site.register(userprofile)