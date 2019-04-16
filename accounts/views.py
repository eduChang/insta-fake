from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Create your views here.
def signup(request):
    raise("asdf")
    if request.method=="POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts:list")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/form.html',{'form':form})
    
def login(request):
    if request.method=="POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("posts:list")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/form.html", {"form":form})
    
def logout(request):
    auth_logout(request)
    return redirect("posts:list")
    
def user_page(request,id):
    User = get_user_model()
    user_info = User.objects.get(id=id)
    return render(request, "accounts/user_page.html", {'user_info':user_info})

@login_required    
def follow(request,id):
    User = get_user_model()
    me = request.user
    you = User.objects.get(id=id)
    
    if me != you:
        if you in me.followings.all():
            me.followings.remove(you)
        else:
            me.followings.add(you)
    
    return redirect('accounts:user_page', id)

@login_required    
def edit_profile(request, id):
    User = get_user_model()
    user = User.objects.get(id=id)
    me = request.user
    if me == user:
        if request.method=="POST":
            form = CustomUserChangeForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('accounts:user_page', id)
        else:
            form = CustomUserChangeForm(instance=user)
        return render(request, 'accounts/form.html', {'form':form})
    
    return redirect("posts:list")
    
    
    
    
    