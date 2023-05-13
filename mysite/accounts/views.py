from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
    get_user_model,
)
from django.views.generic import View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SignUpForm

User = get_user_model()

# def login(request):
#   next = request.GET.get('next')
#   if request.user.is_authenticated:
#     if request.GET.get('next') != None:
#       return redirect(request.GET.get('next'))
#     messages.warning(request, 'you are in your account!')
#     return redirect('/')
#   elif request.method == 'POST':
#       user_input = request.POST.get('email')
#       try:
#         username = User.objects.get(email=user_input).username
#       except User.DoesNotExist:
#         username = user_input
#       password = request.POST.get('password')
#       user = authenticate(request, username=username, password=password)
#       if user is not None:
#         auth_login(request, user)
#         if request.GET.get('next') != None:
#           return redirect(request.GET.get('next'))
#         return redirect('/')
#   return render(request, 'accounts/login.html', {'next': next})


class LoginView(View):
    template_name = "accounts/login.html"
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                if next := request.POST.get("next"):
                    url = next
                else:
                    url = "/"
                return redirect(url)
            else:
                messages.error(request, "Inactive user.")
                return redirect(reverse("accounts:login"))
        else:
            messages.error(request, "Invalid input.")
            return redirect(reverse("accounts:login"))

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(self.request, "you already logged in!")
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)


# @login_required
# def logout(request):
#   auth_logout(request)
#   return redirect('/')


class LogoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect("/")


# def signup(request):
#   if request.user.is_authenticated:
#     messages.warning(request, 'you are in your account!')
#     return redirect('/')
#   elif request.method == 'POST':
#     form = UserCreationForm(request.POST)
#     if form.is_valid():
#       form.save()
#       messages.success(request, 'User created.')
#       return redirect('/accounts/login')
#     else:
#       messages.error(request, 'User didnt created.')
#   else:
#     form = UserCreationForm()
#   return render(request, 'accounts/signup.html', {'form': form})


class SignupView(SuccessMessageMixin, CreateView):
    template_name = "accounts/signup.html"
    form_class = SignUpForm
    success_url = "/"
    success_message = "User created."

    def get(self, request, *args: str, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return redirect(reverse("accounts:signup"))

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, "you are in your account!")
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)
