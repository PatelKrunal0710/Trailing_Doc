from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import Fileinfo,Checklist_Master,docinfo
import datetime
import csv,io

def loginpage(request):
    if request.method=="POST":
        user = authenticate(username = request.POST['name'], password = request.POST['password'])
        print(user)
        if user is not None:
            ldt = user.last_login
            login(request, user)
            if ldt == None:
                return redirect('password_change')
            else:
                if request.user.userprofile.Role == 'Admin':
                    return redirect('Fileupload')
                if request.user.userprofile.Role == 'Processor':
                    return redirect('Checklist')
        else:
            return render (request,'Login.HTML', {'error':'username or password is incorrect'})
    else:
        return render(request, 'Login.html')

def Logout(request):
    request.session.flush()
    logout(request)
    return redirect('loginpage')

def Fileupload(request):
    if request.method == "POST":
        csv_file = request.FILES['file']
        print(csv_file)
        data_set = csv_file.read().decode('UTF-8')
        print(data_set)
        io_string = io.StringIO(data_set)
        print(io_string)
        next(io_string)        
        # for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        #     _, created = Fileinfo.objects.update_or_create(
        #         Loan_No=column[0],
        #         Borrower_lname=column[1],
        #         State=column[2],
        #         Checklist=column[3],
        #         Upload_Date = datetime.datetime.now(),
        #     )
        return render(request, "Fileupload.HTML")
    return render(request, "Fileupload.HTML")


def Checklist(request):
    lno = Fileinfo.objects.filter(File_process=0).first()
    # lno.File_process = 2
    # lno.Proc_userid = str(request.user)
    # lno.Proc_sdate = datetime.datetime.now()
    # lno.save()
    chk = Checklist_Master.objects.filter(Checklist_type = lno.Checklist).order_by('View_no')
    return render(request,'BCD.html',{'lno':lno,'chk':chk})

def Chk_save(request):
    d = dict(request.POST)
    fid = int(request.POST["fileid"])
    loanno = int(request.POST["loan_no"])
    bname = request.POST["Bname"]
    state = request.POST["State"]
    sr = d['Sr']
    chklist = d['list']
    status = d['ddstatus']
    cmnt = d['comment']
    for (a,b,c,d) in zip(sr,chklist,status,cmnt):
        d = docinfo.objects.create(Tdfileid=fid,Loan_no= loanno, Borrower_lname = bname,State=state,View_no=int(a),Checklist=b,Proc_status=c,Proc_comments=d)
        d.save()
    if 'Fail' in status:
        Fileinfo.objects.filter(Loan_No = loanno).update(File_status = 'Fail',Proc_edate=datetime.datetime.now())
    elif 'Suspend' in status:
        Fileinfo.objects.filter(Loan_No = loanno).update(File_status = 'Suspend',Proc_edate=datetime.datetime.now())
    else:
        Fileinfo.objects.filter(Loan_No = loanno).update(File_status = 'Pass',Proc_edate=datetime.datetime.now())
    return redirect('Checklist')

def faildoc(request):
    fdr = docinfo.objects.filter(Proc_status="Fail").order_by("Loan_no")
    pfdr = Fileinfo.objects.filter(File_status="Pass")
    sfdr = Fileinfo.objects.filter(File_status="Suspend")
    return render(request,'report.html',{'fdr':fdr,'pfdr':pfdr,'sfdr':sfdr})