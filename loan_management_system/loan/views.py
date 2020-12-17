from datetime import datetime
from loan.models import NewLoan
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django import forms
from django.urls import reverse



def index(request):
    return render(request, "index.html")

def customer_signup(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['signupusername']
        email = request.POST['signupemail']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        try:
            validate_password(pass1)
        except:
            messages.error(request, "Minimum length of password should be 8 characters!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return redirect('home')
        
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("home")
    
        myuser = User.objects.create_user(username, email, pass1, first_name = first_name, last_name = last_name)
        myuser.save()
        messages.success(request, "Your account has been successfully created!")
        return redirect('home')


def customer_signin(request):
    if request.method == "POST":
        cust_username = request.POST['cust_username']
        cust_password = request.POST['cust_pass']
        user = authenticate(username = cust_username, password = cust_password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Successfully Logged In!")
            records = NewLoan.objects.all()
            record_list = []
            for record in records:
                if record.fname == request.user.first_name:
                    record_list.append(record)
            params = {"records": record_list}
            return render(request, "loan_request.html", params)
                
        else:
            messages.error(request, "Invalid Credentials, Please try again!")
            return redirect("home")
    else:
        return HttpResponse("<h1>Error 404 - Not Found</h1>")


def loan_request(request):
    fname = request.GET['fname']
    amount = request.GET['amount']
    tenure = request.GET['tenure']
    comments = request.GET['comments']
    
    new_user = NewLoan.objects.create(fname = fname, amount = amount, tenure = tenure, comments = comments)
    messages.success(request,"Your loan request has been successfully enqueued, we will get back to you once it has been approved!")
    return render(request, 'loan_request.html')

    # return HttpResponseRedirect(reverse('app_name:url'))
    # messages.error(request,"Fill in the required fields")
    # return HttpResponseRedirect(reverse('app_name:url'))
        

def change_password(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(username=request.user)
        check_old_password = request.user.check_password(request.POST['oldpass'])
        if not check_old_password:
            messages.error(request, "Your old password does not match!")
            return redirect("new_loan")

        new_pass = request.POST['newpass']
        confirm_pass = request.POST['confirmpass']

        if new_pass == confirm_pass:
            current_user.set_password(new_pass)
            current_user.save()
            messages.success(
                request, "Your password has been successfully changed!")
            auth_login(request, current_user)
            return redirect("new_loan")
    else:
        messages.warning(request, "You have been logged out, please login again to change password!")
        return redirect("home")

def customer_signout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out!")
    return redirect('home')

def agent_signin(request):
    return HttpResponse("agent signed in")

def agent_signout(request):
    return HttpResponse('agent signed out')


def admin_signin(request):
    return HttpResponse("admin signed in")

def admin_signout(request):
    return HttpResponse("admin signed out")