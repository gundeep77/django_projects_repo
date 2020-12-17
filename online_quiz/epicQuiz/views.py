import random
import smtplib
import json
from epicQuiz.models import ComputerQuiz, UserTestData, ScienceQuiz, GKQuiz
from django.shortcuts import HttpResponse, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from email.message import EmailMessage
from online_quiz import settings


my_email = settings.EMAIL_HOST_USER
my_password = settings.EMAIL_HOST_PASSWORD


def home(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def user_page(request):
    return render(request, 'user_page.html')


@login_required(login_url='login')
def computer_quiz(request):
    user_computer_quiz_status = UserTestData.objects.get(user = request.user)
    if not user_computer_quiz_status.computer_status:
        user_computer_quiz_status.computer_status = True
        user_computer_quiz_status.save()
        quiz = ComputerQuiz.objects.all()
        return render(request, 'computer_quiz.html', {'quiz': quiz})
    else:
        messages.error(request, "You have already taken this quiz!")
        return redirect('user_page')


@login_required(login_url='login')
def science_quiz(request):
    user_science_quiz_status = UserTestData.objects.get(user = request.user)
    if not user_science_quiz_status.science_status:
        user_science_quiz_status.science_status = True
        user_science_quiz_status.save()
        quiz = ScienceQuiz.objects.all()
        return render(request, 'science_quiz.html', {'quiz': quiz})
    else:
        messages.error(request, "You have already taken this quiz!")
        return redirect('user_page')


@login_required(login_url='login')
def gk_quiz(request):
    user_gk_quiz_status = UserTestData.objects.get(user = request.user)
    if not user_gk_quiz_status.gk_status:
        user_gk_quiz_status.gk_status = True
        user_gk_quiz_status.save()
        quiz = GKQuiz.objects.all()
        return render(request, 'gk_quiz.html', {'quiz': quiz})
    else:
        messages.error(request, "You have already taken this quiz!")
        return redirect('user_page')


@login_required(login_url='login')
def computer_result(request):
    if request.method == "POST":        
        user_data = UserTestData.objects.get(user = request.user)
        user_data.computer_status = True
        user_data.save()
        response = {}
        count = 0
        remark = ''
        quiz = ComputerQuiz.objects.all()
        for ques in quiz:
            if request.POST.get(str(ques.id)) == ques.correct_ans:
                count += 1
            response[str(ques.id)] = request.POST.get(str(ques.id))
        data = json.dumps(response, indent = 4)
        user_data.computer_responses += data
        user_data.save()
        if count < 4:
            remark = 'POOR'
        elif count >= 4 and count < 8:
            remark = 'AVERAGE'
        elif count >= 8 and count < 10:
            remark = 'EXCELLENT'
        else:
            remark = 'OUTSTANDING'
        
        final = []
        for ques in quiz:
            temp = []
            temp.append(ques.question)
            temp.append(request.POST.get(str(ques.id)))
            temp.append(ques.correct_ans)
            final.append((temp))
        return render(request, 'result.html', {"count": count, 'remark': remark, 'final': final})
    else:
        return redirect('user_page')


@login_required(login_url='login')
def science_result(request):
    if request.method == "POST":
        user_data = UserTestData.objects.get(user = request.user)
        user_data.science_status = True
        user_data.save()
        response = {}
        count = 0
        remark = ''
        quiz = ScienceQuiz.objects.all()
        for ques in quiz:
            if request.POST.get(str(ques.id)) == ques.correct_ans:
                count += 1
            response[str(ques.id)] = request.POST.get(str(ques.id))
        data = json.dumps(response, indent = 4)
        user_data.science_responses += data
        user_data.save()
        if count < 4:
            remark = 'POOR'
        elif count >= 4 and count < 8:
            remark = 'AVERAGE'
        elif count >= 8 and count < 10:
            remark = 'EXCELLENT'
        else:
            remark = 'OUTSTANDING'
        final = []
        for ques in quiz:
            temp = []
            temp.append(ques.question)
            temp.append(request.POST.get(str(ques.id)))
            temp.append(ques.correct_ans)
            final.append((temp))
        return render(request, 'result.html', {"count": count, 'remark': remark, 'final': final})
    else:
        return redirect('user_page')


@login_required(login_url='login')
def gk_result(request):
    if request.method == "POST":
        user_data = UserTestData.objects.get(user = request.user)
        user_data.gk_status = True
        user_data.save()
        response = {}
        count = 0
        remark = ''
        quiz = GKQuiz.objects.all()
        for ques in quiz:
            if request.POST.get(str(ques.id)) == ques.correct_ans:
                count += 1
            response[str(ques.id)] = request.POST.get(str(ques.id))
        data = json.dumps(response, indent = 4)
        user_data.gk_responses += data
        user_data.save()
        if count < 4:
            remark = 'POOR'
        elif count >= 4 and count < 8:
            remark = 'AVERAGE'
        elif count >= 8 and count < 10:
            remark = 'EXCELLENT'
        else:
            remark = 'OUTSTANDING'
        final = []
        for ques in quiz:
            temp = []
            temp.append(ques.question)
            temp.append(request.POST.get(str(ques.id)))
            temp.append(ques.correct_ans)
            final.append((temp))
        return render(request, 'result.html', {"count": count, 'remark': remark, 'final': final})
    else:
        return redirect('user_page')


def signup_method(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        signupemail = request.POST['signupemail']
        signupusername = request.POST['signupusername']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        try:
            validate_password(pass1)
        except:
            messages.error(request, "Minimum length of password should be 8 characters!")
            return redirect("home")

        if not signupusername.isalnum():
            messages.error(request, "Username must be alphanumeric!")
            return redirect("home")
        elif pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return redirect("home")
        elif User.objects.filter(username=signupusername).exists():
            messages.error(request, "Username already exists!")
            return redirect("home")

        myuser = User.objects.create_user(signupusername, signupemail, pass1, first_name = fname, last_name = lname)
        myuser.save()
        userdata = UserTestData.objects.create(user = myuser)
        userdata.save()
        messages.success(request, "Your account has been successfully created!")
        return redirect('home')
    else:
        return HttpResponse("<h1>Error 404 - Not Found</h1>")


def login_method(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username = loginusername, password = loginpass)
        
        if user is not None:
            auth_login(request, user)
            return redirect('user_page')
        else:
            messages.error(request, "Invalid credentials, please try again!")
            return redirect('home')
        
    else:
        return redirect('home')


def change_password(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(username=request.user)
        check_old_password = request.user.check_password(request.POST['oldpass'])
        if not check_old_password:
            messages.error(request, "Your old password does not match!")
            return redirect("user_page")

        new_pass = request.POST['newpass']
        confirm_pass = request.POST['confirmpass']

        if new_pass == confirm_pass:
            current_user.set_password(new_pass)
            current_user.save()
            messages.success(
                request, "Your password has been successfully changed!")
            auth_login(request, current_user)
            return redirect("user_page")


def logout_method(request):
    logout(request)
    return redirect('home')


def send_mail(msg):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(my_email, my_password)
    server.send_message(msg)
    server.close()


def generate_password():
    import string
    alphas = string.ascii_letters
    digits = string.digits
    special = string.punctuation
    special = special.replace(',','').replace('.','').replace(';','').replace('"','').replace("'",'')

    string1 = ''.join(random.choice(alphas) for i in range(3))
    digit_set = ''.join(random.choice(digits) for i in range(3))
    special_set = ''.join(random.choice(special) for i in range(3))
    
    new_string =  string1 + digit_set + special_set
    lst = []
    for letter in new_string:
        lst.append(letter)
    random.shuffle(lst)
    password = ''
    for letter in lst:
        password += letter
    return password


def forgot_password(request):
    if request.method == "POST":
        fpass_email = request.POST['email_id']
        if User.objects.filter(email = fpass_email).exists():
            new_password = "YOUR NEW PASSWORD: " + generate_password() + "\n" + "Login with this password, then you can set a new password.\n\nThanks and Regards!\nEpic Quiz"
            msg = EmailMessage()
            msg['Subject'] = "Password Reset Notification"
            msg['From'] = "EpicQuiz" + my_email
            msg['To'] = fpass_email
            msg.set_content(new_password)
            send_mail(msg)
            messages.success(request, "Please check your mail!")
            return redirect('home')
        else:
            messages.error(request, "Provided email address is not associated with your account")
            return redirect('home')