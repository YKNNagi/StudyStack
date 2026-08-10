from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

def index(request):
    return HttpResponse("StudyStack")

def signup(request):
    if request.method == "POST":

        #登録ボタンを押した
        pass
    else:

        #最初に登録画面を開いたとき
        form = UserCreationForm()

    return render(request, "study/signup.html", {"form": form})