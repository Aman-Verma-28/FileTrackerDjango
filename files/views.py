
from django.http import HttpResponse
from django.shortcuts import render, redirect
from files.models import Contact
from django.contrib import messages
from files.models import User , FileHistoryModel, FileModel
from django.contrib.auth import authenticate, login, logout

from django.conf import settings
from qrcode import make
import time
from django.utils import timezone
import cv2
import webbrowser
from datetime import datetime


from django.http import HttpResponse
# Create your views here.
def home(request):
    context={"home":"hello home"}
    return render(request,"home/home.html",context)

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']

        if (len(name)<2 or len(email)<2 or len(phone)<10 or len(content)<2 ):
            messages.error(request,"Please fill the correct details")
        else:
            contact=Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,"Your message has been sent successfully")
        #print("We are using post request")
    return render(request,"home/contact.html")

def about(request):
    # if authSlug==None:
    messages.success(request,"Welcome to About")
    return render(request,"home/about.html")
    # else:
        # messages.success(request,"Welcome to About")
        # auth={"authNames":"authNames","authDesc":"authDesc"}
        # return render(request,"home/about.html",auth)


 
def qr_gen(filename):
    print(filename)
    img = make(filename)
    print("img", img)
    img_name = "qr" + str(time.time()) + ".png"
    img.save(str(settings.MEDIA_ROOT) + "/" + img_name)

    return img_name

def CreateFileView(request):
    try:
        if request.method=="POST":
            description=request.POST.get('content')
            print(description)
            filename=request.POST.get('title')
            print(filename)
            owner = str(request.user)
            print(owner)
            print(type(owner))
            print(str(owner))
            tags = request.POST.get('tags')
            print(tags)
            is_active = request.POST.get("is_active", False)

            qrimage = qr_gen(filename)
            # try:
            file_obj = FileModel.objects.create(
                filename=filename,
                owner=owner,
                description=description,
                tags=tags,
                is_active=is_active,
                qrimage=qrimage,
            )
            file_obj.save()
            created_on_obj=FileModel.objects.get(filename=filename)
            # print(created_on_obj.created_on,"created_on")
            data={
                filename:[[{
                "owner":owner,
                "description":description,
                "tags":tags,
                "is_active":is_active,
                "qrimage":qrimage,
                "created_on":str(created_on_obj.created_on)}]]}
            file_history_obj = FileHistoryModel.objects.create(file_state=file_obj,owners=data)
            file_history_obj.save()
            messages.success(request,"Your file is successfully created")
            return redirect("/")

    except Exception as e:
        print(e)
    return render(request,"file/create-file.html",{"hello":"hello"})


def handleSignup(request):
    if request.method=="POST":
        #get the post parameters
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        department=request.POST['department']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']



        if pass1!=pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')

        #creating the user
        myuser=User.objects.create_user(email=email,password=pass1,department=department,fname=fname,lname=lname)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request, "Your ICoder account has been succesfully created")
        return redirect('home')

    else:
        return HttpResponse("404: NOT ALLOWED")


def handlelogin(request):
    if request.method=="POST":
        usernamelogin=request.POST['usernamelogin']
        loginpass=request.POST['loginpass']
        print(usernamelogin,loginpass)
        user=authenticate(request,email=usernamelogin, password=loginpass)
        print("user",user)
        if user is not None:
            login(request,user)
            messages.success(request," Successfully logged In")
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials , Please try again!")
            return redirect('home')
    else:
        return HttpResponse("404! NOT FOUND")



def handlelogout(request):
    logout(request)
    messages.success(request,"Successfully logged Out")
    return redirect('home')



def GetAllFiles(request):
    if request.method=="GET":
        print(request.user)
        owner = User.objects.get(email=str(request.user))
        print(owner)
        # all_files=list(FileModel.objects.all().values("filename"))
        all_files = FileModel.objects.filter(owner=owner).values()
        print(all_files)
        context={'all_files':all_files}
        return render(request,"file/allFiles.html",context)


def GetFile(request,slug):
    if request.method=="GET":
        try:
            print(slug)
            print(type(slug))
            filename = str(slug)
            # print(FileModel.objects.all().values().first())
            cur_file = FileModel.objects.get(filename=filename)
            file_history = FileHistoryModel.objects.get(file_state__filename=filename)
            # print("all_files_new", cur_file)
            # print("file_hostroy", file_history)
            print("file_hostroy", file_history.owners[filename])
            history=file_history.owners
            data={"data":cur_file,"history":history[filename],"status":"File History"}
            
            return render(request,"file/file.html",data)
        except Exception as e:
            # msg = {""}
            print(e)
            return render(request,"home/home.html")
            # return Response({"msg": "No Such file present"})


def GetFileHistory(request,slug):

        try:
            cur_file = FileModel.objects.get(filename=slug)
            file_history=FileHistoryModel.objects.get(file_state__filename=slug)
            print("file_hostroy", file_history.owners[slug])
            history=file_history.owners
            data={"data":cur_file,"history":history[slug]}
            return render(request,"file/file.html",data)
 
        except Exception as e:
            pass
            return render(request,"file/file.html")


def OwnFileHistory(request,slug):

    # print(request.data)

    print(request.body)
    # print(request.META)
    owner=str(request.user)
    filehistory_obj=FileHistoryModel.objects.get(file_state__filename=slug)

    filehistory_obj.file_state.owner=request.user

    data={filehistory_obj.file_state.filename:
          [{
            "owner":owner,
            "description":filehistory_obj.file_state.description,
            "tags":filehistory_obj.file_state.tags,
            "is_active":filehistory_obj.file_state.is_active,
            "created_on":str(datetime.now())
            # "qrimage":filehistory_obj.file_state.qrimage
            }]}
    print("filehistory_obj.owners",filehistory_obj.owners)
    print("data[filehistory_obj.file_state.filename]",data[filehistory_obj.file_state.filename])
    filehistory_obj.owners[filehistory_obj.file_state.filename].append(data[filehistory_obj.file_state.filename])
    filehistory_obj.save()
    filename=slug
    cur_file = FileModel.objects.get(filename=filename)
    file_history = FileHistoryModel.objects.get(file_state__filename=filename)
    # print("all_files_new", cur_file)
    # print("file_hostroy", file_history)
    print("file_hostroy", file_history.owners[filename])
    history=file_history.owners
    data={"data":cur_file,"history":history[filename],"status":"File Status Updated"}

    result={"msg":"File Owner Updated","slug":slug}
    return render(request,"file/update-file.html",result)



def TrackFileView(request):
    if request.method=="GET":

        cap = cv2.VideoCapture(0)
        # initialize the cv2 QRCode detector
        detector = cv2.QRCodeDetector()
        
        while True:
            _, img = cap.read()
            data, bbox, _ = detector.detectAndDecode(img)
        # check if there is a QRCode in the image
            if data:
                a=data
                break
                print(data)
            cv2.imshow("QRCODEscanner", img)   
            if cv2.waitKey(1) == ord("q"):
                    break
        
        # b=webbrowser.open(str(a))
        # cap.release()
        cv2.destroyAllWindows()
        context={"data":data}
        return render(request,"file/track.html",context)
