from django.shortcuts import render ,redirect ,get_object_or_404
from django.views import View
from .forms import UserRegisterationForm ,UserLoginForm,EditUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy
from .models import Relation,Profile



# Create your views here.

class RegisterView(View):

    form_class = UserRegisterationForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)
    
    def get(self,req):
        form = self.form_class()
        return render(req, self.template_name,{'form':form})

    def post(self,req):
        form = self.form_class(req.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'],cd['email'],cd['password'])
            messages.success(req,'you register succfessfuly','success')
            return redirect('home:home')
        return render(req,self.template_name,{"form":form})


class UserLoginView(View):
    from_class = UserLoginForm
    template_name = "accounts/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)
    
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request,*args,**kwargs)
    
    def get(self,req):
        form = self.from_class()
        return render(req,self.template_name , {"form":form})
    
    def post(self,req):
        form = self.from_class(req.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(req , username=cd['username'],password=cd['password'])
            if user is not None:
                login(req,user)
                messages.success(req,"logged in successfuly","success")
                if self.next:
                    return redirect(self.next)
                return redirect("home:home")
            messages.error(req,"username or password is incorrect")

        return render(req,self.template_name,{"form":form})

class UserLogoutView(LoginRequiredMixin,View):
    login_url = '/accounts/login'
    def get(self,req):
        logout(req)
        messages.success(req,"logged out",'success')
        return redirect("home:home")


class UserProfileView(LoginRequiredMixin,View):
    
    def get(self, req, user_id):
        is_following = False
        profile = Profile.objects.filter(user=user_id)
        username = get_object_or_404(User,pk=user_id)
        posts = Post.objects.filter(user=username)
        relation = Relation.objects.filter(from_user=req.user,to_user=username)
        if relation.exists():
            is_following=True

        return render(req,'accounts/profile.html',{'user':username,"is_following":is_following,'profile_bio':profile,'posts':posts})



class UserPasswordResetView(auth_views.PasswordResetView):

    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy("accounts:password_reset_complete")

class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin,View):
    
    def get(self,req,user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=req.user , to_user=user)
        if relation.exists():
            messages.error(req,"you're already followed",'danger')
        else:
            Relation(from_user=req.user , to_user=user).save()
            messages.success(req,'followed','success')
        return redirect('accounts:user_profile',user.id)

class UserUnfollowView(LoginRequiredMixin,View):
    
    def get(self,req,user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=req.user , to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(req,"unfollowed",'success')
        else:
            messages.error(req,"you're not followed before","danger")
        return redirect('accounts:user_profile',user.id)


class EditUserView(LoginRequiredMixin,View):
    
    form_class = EditUserForm
    
    def get(self,req):
        form = self.form_class(instance=req.user.profile,initial={'email':req.user.email})
        return render(req,'accounts/edit_profile.html',{"form":form})

    def post(self,req):
        form = EditUserForm(req.POST,instance=req.user.profile)
        if form.is_valid():
            cd_email = form.cleaned_data['email']
            form.save()
            req.user.email = cd_email
            req.user.save()
            messages.success(req,'Edited','success')

        return redirect('accounts:user_profile',req.user.id)
