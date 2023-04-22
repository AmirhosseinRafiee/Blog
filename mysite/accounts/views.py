from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

def login(request):
  next = request.GET.get('next')
  if request.user.is_authenticated:
    if request.GET.get('next') != None:
      return redirect(request.GET.get('next'))
    messages.warning(request, 'you are in your account!')
    return redirect('/')  
  elif request.method == 'POST':
      userinput = request.POST.get('username')
      try:
        username = User.objects.get(email=userinput).username
      except User.DoesNotExist:
        username = userinput
      password = request.POST.get('password')
      user = authenticate(request, username=username, password=password)
      if user is not None:
        auth_login(request, user)
        if request.GET.get('next') != None:
          return redirect(request.GET.get('next')) 
        return redirect('/') 
  return render(request, 'accounts/login.html', {'next': next})
  

@login_required
def logout(request):
  auth_logout(request)
  return redirect('/')

def signup(request):
  if request.user.is_authenticated:
    messages.warning(request, 'you are in your account!')
    return redirect('/')
  elif request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'User created.')
      return redirect('/accounts/login')
    else:
      messages.error(request, 'User didnt created.')
  else:
    form = UserCreationForm()
  return render(request, 'accounts/signup.html', {'form': form})