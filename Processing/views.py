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
        io_string = io.StringIO(data_set)        
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = Fileinfo.objects.update_or_create(
                Upload_Date = datetime.datetime.now(),
                Sr_No = column[0],
                Loan_No =column[1],
                MM_Loan = column[2],
                Borrower_lname=column[3],
                Process_Type = column[4],
                Checklist=column[5],
                File_name = csv_file,
                Priority = column[6],
            )
        return render(request, "Fileupload.HTML")
    return render(request, "Fileupload.HTML")

def chkmaster(request):
    if request.method == "POST":
        csv_file = request.FILES['file']
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)        
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = Checklist_Master.objects.update_or_create(
                View_no = column[0],
                Audit_item = column[1],
                Checklist_type = column[2],
            )
        return render(request, "chkmsterupload.HTML")
    return render(request, "chkmsterupload.HTML")

def Checklist(request):
    lno = Fileinfo.objects.filter(File_process=0).order_by('-Priority').first()
    lno.File_process = 2
    lno.Proc_userid = str(request.user)
    lno.Proc_sdate = datetime.datetime.now()
    lno.save()
    chk = Checklist_Master.objects.filter(Checklist_type = lno.Checklist).order_by('View_no')
    print(chk)
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
        Fileinfo.objects.filter(Loan_No = loanno).update(File_status = 'Pass',Proc_edate=datetime.datetime.now(),File_process=1)
    return redirect('Dashboard')

def faildoc(request):
    fdr = docinfo.objects.filter(Proc_status="Fail").order_by("Loan_no")
    pfdr = Fileinfo.objects.filter(File_status="Pass")
    sfdr = Fileinfo.objects.filter(File_status="Suspend")
    return render(request,'report.html',{'fdr':fdr,'pfdr':pfdr,'sfdr':sfdr})

def pdashboard(request):
    tcount = Fileinfo.objects.filter(File_process=0).count()
    pcount = Fileinfo.objects.filter(File_process=1,Proc_edate__date=datetime.date.today(),Proc_userid=request.user).count()
    qcount = Fileinfo.objects.filter(File_process=1,Qc_edate__date=datetime.date.today(),Qc_userid=request.user).count()
    return render(request, 'Dashboard.html',{'tcount':tcount,'pcount':pcount,'qcount':qcount})