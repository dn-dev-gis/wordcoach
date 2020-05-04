from django.shortcuts import render, redirect
from .forms import AddForm, CheckForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Word

def home(request):
    return render(request, 'home.html')

def learn(request):
    if request.user.is_authenticated:
        wordrandom = Word.objects.filter(translatedyes__lte=50).order_by('?').first()
        eng = wordrandom.english
        kis = wordrandom.kiswahili

        if request.method == 'GET':
            return render(request, 'checkwords.html', {'form':CheckForm(), 'eng':eng, 'kis':kis})
        else:
            form = CheckForm(request.POST)
            if form.is_valid():
                newword = form.cleaned_data['inputword'].lower()
                clue2 = request.POST.get("clueword", "")
                checkword = Word.objects.filter(english=clue2).first()
                checkworddetail = checkword.kiswahili.lower()
                if newword == checkworddetail:
                    checkword.translatedyes = checkword.translatedyes + 1
                    checkword.save()
                    return redirect('checkcorrect')
                else:
                    return render(request, 'checknotcorrect.html', {'eng':eng, 'kis':kis})
            else:
                return redirect('checknotcorrect')
    else:
        return redirect('loginuser')

def add(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'addwords.html', {'form':AddForm()})
        else:
            form = AddForm(request.POST)
            if form.is_valid():
                eng = form.cleaned_data['english']
                kis = form.cleaned_data['kiswahili']
                if Word.objects.filter(kiswahili=kis):
                    if Word.objects.filter(kiswahili=kis).filter(english__contains=eng):
                        return render(request, 'addwords.html', {'form':AddForm(), 'error':'Word combination already exists'})
                    elif Word.objects.filter(english__contains=eng):
                        return render(request, 'addwords.html', {'form':AddForm(), 'error':'English word already exists'})
                    else:
                        combine = Word.objects.filter(kiswahili=kis).first()
                        combine.english = combine.english + ', ' + eng
                        combine.save()
                        return render(request, 'addwordscombinedone.html', {'eng':combine.english, 'kis':kis})
                else:
                    newword = form.save(commit=False)
                    newword.save()
                    return redirect('adddone')
    else:
        return redirect('loginuser')

def adddone(request):
    totalrecords = Word.objects.count()
    return render(request, 'addwordsdone.html',{'totalrecords':totalrecords})

def addcombinedone(request):
    return render(request, 'addwordscombinedone.html')

def checkcorrect(request):
    totalrecords = Word.objects.count()
    correctrecords = Word.objects.filter(translatedyes__gte=51).count()
    return render(request, 'checkcorrect.html',{'totalrecords':totalrecords, 'correctrecords':correctrecords})

def checknotcorrect(request):
    return render(request, 'checknotcorrect.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password do not match'})
        else:
            login(request, user)
            return redirect('home')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
