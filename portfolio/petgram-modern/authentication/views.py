from django.shortcuts import redirect, render, reverse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from user_profile.models import CustomUser
from authentication.forms import SignUpForm, LoginForm
from django.contrib import messages

class SignUpView(View):
    def get(self, request):
        template_name = 'generic_form.html'
        form = SignUpForm()
        return render(request, template_name, {'form':form, 'headertwo':'Sign Up'})
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = CustomUser.objects.create_user(
                display_name=data.get('display_name'),
                username=data.get('username'),
                bio=data.get('bio'),
                email=data.get('email'),
                password=data.get('password'),
                pet_type=data.get('pet_type'),
            )
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next', reverse('homepage')))
        else:
            messages.error(request,'Username already taken')
            print('Username already taken')
            return redirect('signup')
           
class LoginView(View):
    template_name = 'generic_form.html'

    def get(self, request):
        
        form = LoginForm()
        return render(request, self.template_name, {'form':form, 'headerone':'Login'})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            print('Form is valid')
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data.get('username'),
                password=data.get('password')
            )
            if user:
                login(request, user)
                print('You are in!')
            else:
                messages.error(request,'username or password is invalid')
                print("Please signup")
        return HttpResponseRedirect(request.GET.get('next', reverse('homepage')))

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('homepage'))

def error_404_view(request,):
    return render(request, '404.html', status=404)

def error_500_view(request):
    return render(request, '500.html', status=500)        