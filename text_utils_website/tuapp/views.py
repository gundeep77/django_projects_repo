import os
import string
import smtplib
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password

my_email = os.environ.get('EMAIL_ADDRESS')
my_password = os.environ.get('EMAIL_PASSWORD')


params = {}
analyze_hasrun = False


def home(request):
    return render(request, 'tuapp/home.html')


def about(request):
    if request.method == "POST":
        return render(request, 'tuapp/about.html')
    else:
        return HttpResponse("<h1>Error 404 - Not Found</h1>")


def contacts(request):
    if request.method == "POST":
        return render(request, 'tuapp/contacts.html')
    else:
        return HttpResponse("<h1>Error 404 - Not Found</h1>")


def main(request):
    return render(request, 'tuapp/main.html')


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(my_email, my_password)
    server.sendmail(my_email, to, content)
    server.close()


def forgot_password(request):
    if request.method == "POST":
        fpass_email = request.POST['email_id']
        content = "Please click this link to proceed"
        if User.objects.filter(email = fpass_email).exists():
            sendEmail(fpass_email, content)
            return HttpResponse("Check your mail")


def signup_method(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        signupusername = request.POST['signupusername']
        signupemail = request.POST['signupemail']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        try:
            validate_password(pass1)
        except:
            messages.error(request, "Minimum length of password should be 8 characters!")
            return redirect("home")

        # Check for erroneous inputs
        if not signupusername.isalnum():
            messages.error(request, "Username must be Alphanumeric!")
            return redirect("home")

        elif pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return redirect("home")

        elif User.objects.filter(username=signupusername).exists():
            messages.error(request, "Username already exists!")
            return redirect("home")

        # Create user
        myuser = User.objects.create_user(signupusername, signupemail, pass1, first_name = first_name, last_name = last_name)
        myuser.save()
        messages.success(
            request, "Your account has been successfully created!")
        return redirect("home")

    else:
        return HttpResponse("<h1>Error 404 - Not Found</h1>")


def login_method(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        
        user = authenticate(username=loginusername, password=loginpass)
    
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in!")
            return redirect("appHome")
        elif user is not None:
            auth_login(request, user)
            messages.success(request, "Successfully Logged In!")
            return redirect("appHome")
        else:
            messages.error(request, "Invalid Credentials, Please try again!")
            return redirect("home")
    else:
        return HttpResponse("<h1>Error 404 - Not Found</h1>")

def logout_method(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You are already logged out!")
        return redirect("home")
    logout(request)
    messages.success(request, "Successfully Logged Out!")
    return redirect('home')


def change_password(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(username=request.user)
        check_old_password = request.user.check_password(request.POST['oldpass'])
        if not check_old_password:
            messages.error(request, "Your old password does not match!")
            return redirect("appHome")

        new_pass = request.POST['newpass']
        confirm_pass = request.POST['confirmpass']

        if new_pass == confirm_pass:
            current_user.set_password(new_pass)
            current_user.save()
            messages.success(
                request, "Your password has been successfully changed!")
            auth_login(request, current_user)
            return redirect("appHome")
    else:
        messages.warning(request, "You have been logged out, please login again to change password!")
        return redirect("home")


# def download(request):
#     global params
#     global analyze_hasrun

#     if analyze_hasrun:
#         file = open("analyzed_text.txt", 'w')
#         file.write(params['analyzed_text'] + "\n\n")
#         file.write(params['char_count'])
#         file.close()
#     return HttpResponse("Downloaded!")


# @login_required(redirect_field_name="next", login_url='')
def analyze(request):
    if not request.user.is_authenticated:
        messages.warning(
            request, "You have been logged out, please login again to use the utilities!")
        return redirect("home")
    global params
    global analyze_hasrun
    djtext = request.POST.get('text', 'default')
    removepunc = request.POST.get('removepunc', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    fullcaps = request.POST.get('fullcaps', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')
    charcounter = request.POST.get('charcounter', 'off')

    analyzed = ""
    extracount = 0
    djtext = djtext.strip()

    nlr = False
    esr = False
    rp = False
    fc = False

    if djtext != "" and (
            newlineremover == 'on' or extraspaceremover == 'on' or removepunc == 'on' or fullcaps == 'on' or charcounter == 'on'):
        if removepunc == "on" and djtext != "":
            for char in djtext:
                if char not in string.punctuation:
                    analyzed += char
            params = {'analyzed_text': analyzed}
            rp = True

        if newlineremover == "on" and djtext != "":
            if rp:
                djtext = params['analyzed_text']
                analyzed = ""
            for line in djtext.splitlines():
                if line == "":
                    continue
                analyzed += line + "\n"
            params = {'analyzed_text': analyzed}
            nlr = True

        if extraspaceremover == "on" and djtext != "":
            if nlr or rp:
                djtext = params['analyzed_text']
                analyzed = ""
            for i in range(len(djtext)):
                if djtext[i] == " " == djtext[i + 1]:
                    continue
                else:
                    analyzed += djtext[i]
            params = {'analyzed_text': analyzed}
            esr = True

        if fullcaps == "on" and djtext != "":
            if nlr or esr or rp:
                djtext = params['analyzed_text']
                analyzed = ""
            for char in djtext:
                analyzed += char.upper()
            params = {'analyzed_text': analyzed}
            fc = True

        if charcounter == "on" and djtext != "":
            count = 0
            if nlr:
                count -= 1
                djtext = params['analyzed_text']
            if esr or rp or fc:
                djtext = params['analyzed_text']
            for _ in djtext:
                count += 1
            if extracount != 0:
                count -= extracount
            params = {'analyzed_text': djtext,
                      'char_count': "Number of characters: " + str(count)}
        analyze_hasrun = True
        return render(request, 'tuapp/analyze.html', params)

    elif djtext == "" and (
            newlineremover == 'on' or extraspaceremover == 'on' or removepunc == 'on' or fullcaps == 'on' or charcounter == 'on'):
        return render(request, 'tuapp/warningmessage.html')
    else:
        return render(request, 'tuapp/warningmessage.html')
