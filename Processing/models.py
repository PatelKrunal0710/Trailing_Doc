from django.db import models
from django.contrib.auth.models import User

class Fileinfo(models.Model):
    Upload_Date = models.DateTimeField()
    Loan_No = models.IntegerField()
    Borrower_lname = models.CharField(max_length=254)
    State = models.CharField(max_length=254)
    File_process = models.IntegerField(blank=True, null=True,default=0)
    File_note = models.CharField(max_length=254,blank=True, null=True)
    File_status = models.CharField(max_length=254, blank=True, null=True)
    Proc_userid = models.CharField(max_length=254, blank=True, null=True)
    Proc_sdate = models.DateTimeField(blank=True, null=True)
    Proc_edate = models.DateTimeField(blank=True, null=True)
    Qc_process = models.IntegerField(blank=True, null=True)
    Qc_userid = models.CharField(max_length=254, blank=True, null=True)
    Qc_sdate = models.DateTimeField(blank=True, null=True)
    Qc_edate = models.DateTimeField(blank=True, null=True)
    Checklist = models.CharField(max_length=254)

    def __str__(self):
        return str(self.Loan_No)

class Checklist_Master(models.Model):
    View_no = models.IntegerField()
    Audit_item = models.CharField(max_length=254)
    Checklist_type = models.CharField(max_length=254)

    def __str__(self):
        return self.Audit_item

class docinfo(models.Model):
    Tdfileid = models.IntegerField(null=True)
    Loan_no = models.IntegerField(null=True)
    Borrower_lname = models.CharField(max_length=254,null=True)
    State = models.CharField(max_length=254,null=True)
    View_no = models.IntegerField(null=True)
    Checklist = models.CharField(max_length=254,null=True)
    Proc_status = models.CharField(max_length=254,null=True)
    Proc_comments = models.CharField(max_length=254,null=True)
    Qc_status = models.CharField(max_length=254,null=True)
    Qc_comments = models.CharField(max_length=254,null=True)
    Checklist_type = models.CharField(max_length=254,null=True)

    def __str__(self):
        return str(self.Tdfileid)

class userprofile(models.Model):
    user = models.OneToOneField(User,on_delete='models.CASCADE')
    emp_id = models.IntegerField()
    emp_name = models.CharField(max_length = 120)
    Delete_date = models.DateTimeField(null=True, blank=True)
    Role = models.CharField(max_length=120)

    def __str__(self):
        return self.emp_name