from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("StudyStack")

def signup(request):
    if request.method == "POST":

        #登録ボタンを押した
        form =UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

        else:
            print(form.errors)
        
    else:

        #最初に登録画面を開いたとき
        form = UserCreationForm()

    return render(request, "study/signup.html", {"form": form})



def login_view(request):
    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("dashboard")
      
    else:
        form = AuthenticationForm()

    return render(request, "study/login.html", {"form": form})

@login_required(login_url="/login/")
def dashboard(request):
    return render(request, "study/dashboard.html")