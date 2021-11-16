# django imports
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import View

# local imports
from . import forms


def signup(request):
    """ Sign a user up to grant access to his feed.

    - render the signup form
    - If the user signed up successfully, he is redirected to the feed page.
    """

    form = forms.SignupFrom()

    if request.method == 'POST':
        form = forms.SignupFrom(request.POST)

        if form.is_valid():
            user = form.save()
            # auto login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'authentication/signup.html',
                  context={'form': form})


def logout_user(request):
    """ Logout the user.

    - If the user wants to logout, he is redirected to the login page.
    """

    logout(request)
    return redirect('login')


class LoginPageView(View):
    """ Login page view.

    - get method: render the login form
    - post method: authenticate the user and redirect him to the feed page.
    """

    # set the form class and the template name
    template_name = 'authentication/login.html'
    form_class = LoginView

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name,
                      context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('feed')
        message = 'Identifiants invalides.'
        return render(request, self.template_name,
                      context={'form': form, 'message': message})
