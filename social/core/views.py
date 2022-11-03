from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, authenticate, logout
from .models import Profile, Dweet
from .forms import DweetForm
# Create your views here.

def index(request):
  if request.user.is_authenticated:
    # return render(request, "dwitter/index.html")
    form = DweetForm(request.POST or None, request.FILES)

    if request.method == "POST":
      if form.is_valid():
        dweet = form.save(commit=False)
        dweet.user = request.user
        dweet.save()
        return redirect("index")  

    followed_dweets = Dweet.objects.filter(
        user__profile__in=request.user.profile.follows.all()
    ).order_by("-created_at")

    return render(
        request,
        "dwitter/index.html",
        {"form": form, "dweets": followed_dweets},
      )

  return redirect("/login")

def register(request):
  if request.method=='GET':
    return render(request,"dwitter/register.html",{"form":UserCreationForm})

  if request.method=='POST':
    form = UserCreationForm(request.POST)
    if form.is_valid(): 
      user=form.save()
      Profile.objects.create(user=user,bio="")
      return redirect("/")
    else:
      return render(request,"dwitter/register.html",{"form":form})

def signin(request):
  if request.method=='GET':
    return render(request,"dwitter/login.html",{"form":AuthenticationForm})

  if request.method=='POST':
    form = AuthenticationForm(request=request,data=request.POST)
    if form.is_valid():
      username=form.cleaned_data.get('username')
      password=form.cleaned_data.get('password')
      user=authenticate(username=username,password=password)
      if user is not None:
        login(request, user)
        return redirect("/")
    else:
      return render(request,"dwitter/login.html",{"form":form})

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return render(request,"dwitter/login.html",{"form":AuthenticationForm})

def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})

def profile(request, pk):
  if not hasattr(request.user, 'profile'):
    missing_profile = Profile(user=request.user)
    missing_profile.save()

  profile = Profile.objects.get(pk=pk)
  if request.method == "POST":
    current_user_profile = request.user.profile
    data = request.POST
    action = data.get("follow")
    if action == "follow":
      current_user_profile.follows.add(profile)
    elif action == "unfollow":
      current_user_profile.follows.remove(profile)
    current_user_profile.save()
  return render(request, "dwitter/profile.html", {"profile": profile})