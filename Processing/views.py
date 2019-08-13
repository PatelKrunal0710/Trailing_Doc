from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import Fileinfo,Checklist_Master,docinfo
import csv,io,random,datetime
from datetime import timedelta

def loginpage(request):
    if request.method=="POST":
        user = authenticate(username = request.POST['name'], password = request.POST['password'])
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
        return render(request, "Fileupload.HTML",{"smesg":"File has been uploaded successfully."})
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
    lno = Fileinfo.objects.get(File_process=2,Proc_userid=request.user)          
    if not lno:
        print(lno,"inside if condition")
        lno = Fileinfo.objects.filter(File_process=0).order_by('-Priority').first()    
        lno.File_process = 2
        lno.Proc_userid = str(request.user)
        lno.Proc_sdate = datetime.datetime.now()
        lno.save()    
    chk = Checklist_Master.objects.filter(Checklist_type = lno.Checklist).order_by('View_no')
    return render(request,'BCD.html',{'lno':lno,'chk':chk})

def Chk_save(request):
    loan = docinfo.objects.filter(Loan_no = request.POST["loan_no"])
    print(loan)
    if not loan:
        d = dict(request.POST)
        fid = int(request.POST["fileid"])
        loanno = int(request.POST["loan_no"])
        bname = request.POST["Bname"]
        state = request.POST["State"]
        Sr_No = request.POST['Sr#']
        Filename =request.POST['File_name']
        sr = d['Sr']
        chklist = d['list']
        status = d['ddstatus']
        cmnt = d['comment']
        for (a,b,c,d) in zip(sr,chklist,status,cmnt):
            d = docinfo.objects.create(Tdfileid=fid,Loan_no= loanno, Borrower_lname = bname,State=state,View_no=int(a),Checklist=b,Proc_status=c,Proc_comments=d,Sr_No = Sr_No,File_name=Filename)
            d.save()
        if 'Fail' in status:
            Fileinfo.objects.filter(Loan_No = loanno).update(File_status = 'Fail',Proc_edate=datetime.datetime.now(),File_process=1)
        elif 'Suspend' in status:
            Fileinfo.objects.filter(Loan_No = loanno).update(File_status = 'Suspend',Proc_edate=datetime.datetime.now(),File_process=1)
        else:
            Fileinfo.objects.filter(Loan_No = loanno).update(File_status = 'Pass',Proc_edate=datetime.datetime.now(),File_process=1)
        if request.user.userprofile.Sample_QC == 100:
            Fileinfo.objects.filter(Loan_No = loanno).update(Qc_process=0)
        else:
            completed_loans = Fileinfo.objects.filter(File_process=1,Proc_edate__date=datetime.date.today(),Proc_userid=request.user)
            print(completed_loans, completed_loans.count())
            prcent = completed_loans.count()*request.user.userprofile.Sample_QC/100
            if prcent % 1 == 0:
                rendomloans = Fileinfo.objects.filter(File_process=1,Proc_edate__date=datetime.date.today(),Proc_userid=request.user).exclude(Qc_process=0)
                if request.user.userprofile.Sample_QC == 15:                    
                    sqc = random.choices(rendomloans, k=3)                                        
                    for i in sqc:
                        Fileinfo.objects.filter(Loan_No = str(i)).update(Qc_process=0)
                else:
                    sqc = random.choice(rendomloans)        
                    Fileinfo.objects.filter(Loan_No = str(sqc)).update(Qc_process=0)
        return redirect('Dashboard')
    else:
        return redirect('Dashboard')

def faildoc(request):
    filename =Fileinfo.objects.values('File_name').distinct()
    fdr = docinfo.objects.filter(Proc_status="Fail").order_by("id")
    pfdr = Fileinfo.objects.filter(File_status="Pass").order_by("Sr_No")
    sfdr = Fileinfo.objects.filter(File_status="Suspend").order_by("Sr_No")
    return render(request,'report.html',{'fdr':fdr,'pfdr':pfdr,'sfdr':sfdr,'filename':filename})

def pdashboard(request):    
    tcount = Fileinfo.objects.filter(File_process=0).count()
    tqcount = Fileinfo.objects.filter(Qc_process=0).count()
    pcount = Fileinfo.objects.filter(File_process=1,Proc_edate__date=datetime.date.today(),Proc_userid=request.user).count()
    qcount = Fileinfo.objects.filter(File_process=1,Qc_edate__date=datetime.date.today(),Qc_userid=request.user).count()
    return render(request, 'Dashboard.html',{'tcount':tcount,'tqcount':tqcount,'pcount':pcount,'qcount':qcount})

def Qc(request):
    q = Fileinfo.objects.filter(Qc_process=0).order_by('Proc_edate').exclude(Proc_userid=request.user).first()
    if not q:
        return redirect("404.html")
    q.Qc_process=2
    q.Qc_userid = str(request.user)
    q.Qc_sdate = datetime.datetime.now()
    q.save()
    qcdoc = docinfo.objects.filter(Tdfileid=q.id).order_by("id")
    return render(request,'QC.html',{'qcdoc':qcdoc,'q':q})
    
def qcChk_save(request):
    d = dict(request.POST)
    fid = int(request.POST["fileid"])
    loanno = int(request.POST["loan_no"])
    bname = request.POST["Bname"]
    print(fid,loanno,bname)
    sr = d['Sr']
    chklist = d['list']
    status = d['ddstatus']
    cmnt = d['comment']
    for (a,b,c,d) in zip(sr,chklist,status,cmnt):
        d = docinfo.objects.filter(Tdfileid=fid).update(Qc_status=c,Proc_comments=d)
        if 'Fail' in status:
            Fileinfo.objects.filter(Loan_No = loanno).update(File_status = 'Fail',Qc_edate=datetime.datetime.now(),Qc_process=1)
        elif 'Suspend' in status:
            Fileinfo.objects.filter(Loan_No = loanno).update(File_status = 'Suspend',Qc_edate=datetime.datetime.now(),Qc_process=1)
        else:
            Fileinfo.objects.filter(Loan_No = loanno).update(File_status = 'Pass',Qc_edate=datetime.datetime.now(),Qc_process=1)
    return redirect('Dashboard')