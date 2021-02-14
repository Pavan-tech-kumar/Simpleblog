from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm,LogInForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from  blog.models import Post
from django.contrib.auth.models import Group


#Home page
def home(request):
    posts=Post.objects.all()
    return render(request,'blog/home.html',{"posts":posts})

#About
def about(request):
    return render(request,'blog/about.html')

#contact
def contact(request):
    return render(request,'blog/contact.html')

#dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        user=request.user
        full_name=user.get_full_name()
        gps=user.groups.all()
        return render(request,'blog/dashboard.html',{'posts':posts,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')
#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#sign up
def user_signup(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,' Congratulations,Your Ready To Post......')
            user=form.save()
            group=Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form=SignUpForm()
    return render(request,'blog/signup.html',{"form":form})

#login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form=LogInForm(request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Logged In Successfully")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form=LogInForm()
        return render(request,'blog/login.html',{"form":form})
    else:
        return HttpResponseRedirect('/dashboard/')

#add new post by user
def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form=PostForm(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                desc=form.cleaned_data['desc']
                pst=Post(title=title,desc=desc)
                pst.save()
                messages.success(request,"Added Post Successfully")
                form=PostForm()
        else:
            form=PostForm()
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


#update post by user
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi=Post.objects.get(pk=id)
            form=PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request,"Updated the Post successfully..")
                return HttpResponseRedirect('/dashboard')
        else:
            pi=Post.objects.get(pk=id)
            form=PostForm(instance=pi)
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

#deleting the post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pf=Post.objects.get(pk=id)
            pf.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')