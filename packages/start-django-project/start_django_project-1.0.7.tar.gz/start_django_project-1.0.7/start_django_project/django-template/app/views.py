from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from .forms import CreateUserForm

class IndexView(TemplateView):
    template_name = 'app/index.html'

class AboutView(TemplateView):
    template_name = 'app/about.html'

class SignupView(TemplateView):
    template_name = 'app/signup.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, "app/index.html")
        form = CreateUserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, "app/thanks.html", {'form': form})

        return render(request, self.template_name, {'form': form})

class LoginPageView(TemplateView):
    template_name = 'app/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')

        return render(
            request,
            self.template_name,
            {
                'error_message':
                'Username or password is incorrect'
            }
        )

class LogoutView(TemplateView):
    template_name = 'app/logout.html'

    def get(self, request,  *args, **kwargs):
        logout(request)
        return redirect('index')