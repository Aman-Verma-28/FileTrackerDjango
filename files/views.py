
from django.http import HttpResponse
from django.shortcuts import render, redirect
from files.models import Contact
from django.contrib import messages
from files.models import User , FileHistoryModel, FileModel
from django.contrib.auth import authenticate, login, logout

from django.conf import settings
from qrcode import *
import time
from django.utils import timezone
import cv2
import webbrowser



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

def about(request,authSlug):
    if authSlug==None:
        messages.success(request,"Welcome to About")
        return render(request,"home/contact.html")
    else:
        messages.success(request,"Welcome to About")
        # authNames=User.objects.filter(email=authSlug).first()
        # print(authNames.author)
        # authDesc=Post.objects.filter(author__startswith=authNames.author).values()
        #print(authDesc[0]['authorDesc'])
        # authDesc=(authDesc[0]['authorDesc'])
        auth={"authNames":"authNames","authDesc":"authDesc"}
        return render(request,"home/about.html",auth)

# def createBlog(request):
#     try:
#         allPosts=Post.objects.all()
#         context={'allPosts':allPosts}
#         if request.method=='POST':
#             content=request.POST.get('content')
#             title=request.POST.get('title')
#             user=request.user
#             print(content)
#             now = timezone.now()
#             blog_obj= Post.objects.create(user=user,title=title,content=content,author=user.username,slug=title,timeStamp=now)
#             #print(blog_obj)
#             messages.success(request,"Your blog is successfully posted")
#             return redirect("/")
    
#     except Exception as e:
#         print(e)
#     return render(request,"blog/create-blog.html",context)
 
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
            data={
                filename:[{
                "owner":owner,
                "description":description,
                "tags":tags,
                "is_active":is_active,
                "qrimage":qrimage}]}
            file_history_obj = FileHistoryModel.objects.create(file_state=file_obj,owners=data)
            file_obj.save()
            file_history_obj.save()
            messages.success(request,"Your file is successfully created")
            return redirect("/")

    except Exception as e:
        print(e)
    return render(request,"file/create-file.html",{"hello":"hello"})



# def search(request):
#     #allpost=Post.objects.all()
#     query=request.GET['query']
#     if len(query)>78:
#         allpost=Post.objects.none()
#     else:
#         allpostTitle=Post.objects.filter(title__icontains=query)
#         allpostContent=Post.objects.filter(content__icontains=query)
#         allpost=allpostTitle.union(allpostContent)
#     if allpost.count()==0:
#         messages.warning(request,"No search results found")
#     params={'allposts':allpost,'query':query}
#     return render(request,"home/search.html",params)

#authentication apis


def handleSignup(request):
    if request.method=="POST":
        #get the post parameters
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        department=request.POST['department']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        #checks for error inputs
        # if len(username)>15:
        #     messages.error(request, "Username must be less than 15 characters")
        #     return redirect('home')
        
        # if not username.isalnum():
        #     messages.error(request, "Username can only contain letters and numbers")
        #     return redirect('home')

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

# def handlelogin(request):
#     if request.method=="POST":
#         usernamelogin=request.POST['usernamelogin']
#         loginpass=request.POST['loginpass']
#         try:
#             user=User.objects.get(email=usernamelogin)
#             print(user,"user")
#             print("this",user.check_password(loginpass))
#             if user.check_password(loginpass):

#             # user=authenticate(email=usernamelogin, password=loginpass)
#                 print("user",user)
#                 if user is not None:
#                     # login(request,user)
#                     messages.success(request," Successfully logged In")
#                     return redirect('home')
#                 else:
#                     messages.error(request,"Invalid Credentials , Please try again!")
#                     return redirect('home')
#             else:
#                 messages.error(request,"Invalid Credentials , Please try again!")
#                 return redirect('home')
#         except Exception as e:
#             messages.error(request,"Invalid Credentials , Please try again!")
#             return redirect('home')

#     else:
#         return HttpResponse("404! NOT FOUND")

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

# def handleSignup(request):
#     if request.method=="POST":
#         #get the post parameters
#         # username=request.POST['username']
#         fname=request.POST['fname']
#         lname=request.POST['lname']
#         email=request.POST['email']
#         department=request.POST['department']
#         pass1=request.POST['pass1']
#         pass2=request.POST['pass2']

#         #checks for error inputs
#         # if len(username)>15:
#         #     messages.error(request, "Username must be less than 15 characters")
#         #     return redirect('home')
        
#         # if not username.isalnum():
#         #     messages.error(request, "Username can only contain letters and numbers")
#         #     return redirect('home')

#         if pass1!=pass2:
#             messages.error(request, "Passwords do not match")
#             return redirect('home')
#         email=User.objects.filter(email=email)
#         if email is not None:
#             messages.error(request, "The email already exists")
#             return redirect('home')
#         #creating the user
#         myuser=User.objects.create(email=email,password=pass1,department=department)
#         myuser.first_name=fname
#         myuser.last_name=lname
#         myuser.save()
#         messages.success(request, "Your ICoder account has been succesfully created")
#         return redirect('home')

#     else:
#         return HttpResponse("404: NOT ALLOWED")

# def handlelogin(request):
#     if request.method=="POST":
#         usernamelogin=request.POST['usernamelogin']
#         loginpass=request.POST['loginpass']
#         print("this",usernamelogin,loginpass)
#         try:
#             user=User.objects.get(email=usernamelogin, password=loginpass)
#             if user is not None:
#             # user=authenticate(email=usernamelogin, password=loginpass)
#                 print("user",user)
#             # if user is not None:
#                 login(request,user)
#                 messages.success(request," Successfully logged In")
#                 return redirect('home')
#         except Exception as e:
#             messages.error(request,"Invalid Credentials , Please try again!")
#             return redirect('home')
    # else:
    #     return HttpResponse("404! NOT FOUND")

def handlelogout(request):
    logout(request)
    messages.success(request,"Successfully logged Out")
    return redirect('home')


    # return img_name
    #     return render(request, 'index.html', {'img_name': img_name})
    # return render(request, 'index.html')



def GetAllFiles(request):
    if request.method=="GET":
        print(request.user)
        owner = User.objects.get(email=str(request.user))
        print(owner)
        # all_files=list(FileModel.objects.all().values("filename"))
        all_files = FileModel.objects.filter(owner=owner).values()
        print(all_files)
        context={'all_files':all_files}
        return render(request,"file/blogHome.html",context)


def GetFile(request,slug):
    if request.method=="GET":
        try:
            print(slug)
            print(type(slug))
            filename = str(slug)
            print(FileModel.objects.all().values().first())
            cur_file = FileModel.objects.get(filename=filename)
            print("all_files_new", cur_file)
            context={"filename":cur_file.filename,"description":cur_file.description,"owner":cur_file.owner,"tags":cur_file.tags,"is_active":cur_file.is_active,"qr":cur_file.qrimage}
            # context={'all_files':all_files}
            return render(request,"file/blogPost.html",context)
            #         return Response(
        #             {"all_files": all_files.filename}, status=status.HTTP_200_OK
        #         )
        #     else:
        #         return Response({"msg": "No Such file present"})
        except Exception as e:
            return render(request,"file/blogPost.html",context)
            # return Response({"msg": "No Such file present"})


def GetFileHistory(request,slug):


    # def get(self, request, format=None):
        # data = request.GET
        # print(data)
        # filename = data.get("filename")
            try:
                filehistory_obj=FileHistoryModel.objects.get(file_state__filename=slug)
                print("slug",slug)
                # print("filename", filename)
                # all_files = FileHistoryModel.objects.get(file_state__filename=filename)
                # if all_files:
                    # return render(request,"file/history.html")
                    # pass
                context={"obj":filehistory_obj}
                return render(request,"file/history.html",context)
            #         return Response({"all_files": "done"}, status=status.HTTP_200_OK)
            #     else:
            #         return Response({"msg": "No files present"})
            except Exception as e:
                pass
                return render(request,"file/history.html")
            #     return Response({"msg": "No file history present"})

def OwnFileHistory(request,slug):

    # print(request.data)

    print(request.body)
    # print(request.META)
    owner=str(request.user)
    filehistory_obj=FileHistoryModel.objects.get(file_state__filename=slug)
    # list_of_owners.append(filehistory_obj.file_state.owner)

    filehistory_obj.file_state.owner=request.user
    # print("filehistoryobj",filehistory_obj)
    # print("filehistoryobj.file_state.filename",filehistory_obj.file_state.filename)
    data={filehistory_obj.file_state.filename:
          [{
            "owner":owner,
            "description":filehistory_obj.file_state.description,
            "tags":filehistory_obj.file_state.tags,
            "is_active":filehistory_obj.file_state.is_active,
            # "qrimage":filehistory_obj.file_state.qrimage
            }]}
    print("filehistory_obj.owners",filehistory_obj.owners)
    print("data[filehistory_obj.file_state.filename]",data[filehistory_obj.file_state.filename])
    filehistory_obj.owners[filehistory_obj.file_state.filename].append(data[filehistory_obj.file_state.filename])
    filehistory_obj.save()
    context={"data":filehistory_obj}
    return render(request,"file/update-file.html",context)
    # return HttpResponse("hello")
    # def get(self, request, format=None):
        # data = request.GET
        # print(data)
        # filename = data.get("filename")
            # try:
            #     filehistory_obj=FileHistoryModel.objects.get(file_state__filename=slug)
            #     print("slug",slug)
            #     # print("filename", filename)
            #     # all_files = FileHistoryModel.objects.get(file_state__filename=filename)
            #     # if all_files:
            #         # return render(request,"file/history.html")
            #         # pass
            #     context={"obj":filehistory_obj}
            #     return render(request,"file/history.html",context)
            # #         return Response({"all_files": "done"}, status=status.HTTP_200_OK)
            # #     else:
            # #         return Response({"msg": "No files present"})
            # except Exception as e:
            #     pass
            #     return render(request,"file/history.html")
            # #     return Response({"msg": "No file history present"})


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


# #Every time you call the phone and laptop camera method gets frame
# #More info found in camera.py
# def gen(camera):
# 	while True:
# 		frame = camera.get_frame()
# 		yield (b'--frame\r\n'
# 				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# from django.http import StreamingHttpResponse
# #Method for laptop camera
# def video_feed(request):
# 	return StreamingHttpResponse(gen(VideoCamera()),
#                     #video type
# 					content_type='multipart/x-mixed-replace; boundary=frame')


# from imutils.video import VideoStream
# import imutils
# import cv2
# import os
# import urllib.request
# import numpy as np
# from django.conf import settings





# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)

#     def __del__(self):
#         self.video.release()


#     #This function is used in views
#     def get_frame(self):

#         success, image = self.video.read()
#         frame_flip = cv2.flip(image, 1)
#         ret, jpeg = cv2.imencode('.jpg', frame_flip)
#         return jpeg.tobytes()



# class IPWebCam(object):
#     def __init__(self):
#         self.url = "http://192.168.1.178:8080/shot.jpg"


#     def __del__(self):
#         cv2.destroyAllWindows()

#     def get_frame(self):
#         imgResp = urllib.request.urlopen(self.url)
#         imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
#         img = cv2.imdecode(imgNp, -1)
#         img =cv2.resize(img, (640, 480))
#         frame_flip = cv2.flip(img, 1)
#         ret, jpeg = cv2.imencode('.jpg', frame_flip)
#         return jpeg.tobytes()

