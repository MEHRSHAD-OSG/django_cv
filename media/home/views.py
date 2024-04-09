from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from . import models
from django.contrib import messages
from .forms import PostUpdateForms , CommentForm, ReplyCommentForm,PostSearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

class HomeView(View):
    form_class = PostSearchForm
    def get(self,req):
        posts = models.Post.objects.all()
        form = self.form_class()
        if req.GET.get('search'):
            posts=posts.filter(body__contains=req.GET['search'])

        return render(req,'home/index.html',{'posts':posts,'form':form})





class PostDetailView(View):
    form_class = CommentForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(models.Post,id=kwargs['post_id'],slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)
    
    def get(self,req, *args , **kwargs):
        comment = self.post_instance.pcomment.filter(is_reply=False)
        liked = True
        if req.user.is_authenticated and self.post_instance.user_like(req.user):
            liked = False
        form = self.form_class()
        return render(req , "home/detail.html",{'post':self.post_instance,"comment":comment,'form':form,'liked':liked})
    
    @method_decorator(login_required)
    def post(self,req,*args,**kwargs):
        form = self.form_class(req.POST)

        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.user = req.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(req,"you're comment submitted successfully",'success')
            return redirect('home:detail',self.post_instance.id,self.post_instance.slug)

class PostDeleteView(LoginRequiredMixin,View):
    def get(self,req,post_id):
        post = models.Post.objects.get(pk=post_id)
        if post.user.id==req.user.id:
            post.delete()
            messages.success(req,"deleted successfuly",'success')
        else:
            messages.error(req,"this post not yours",'danger')
        return redirect("home:home")

class PostUpdateView(LoginRequiredMixin,View):
    form_class = PostUpdateForms
    
    def setup(self, request, *args, **kwargs):

        self.post_instance = models.Post.objects.get(id=kwargs['post_id'])
        return super().setup(request,*args,**kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, 'this post is not yours', 'danger')
            return redirect("home:home")
        return super().dispatch(request,*args,**kwargs)


    def get(self,req,*args,**kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(req,'home/update.html',{'form':form})

    def post(self,req,*args,**kwargs):
        post = self.post_instance
        form = self.form_class(req.POST,instance=post)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(req,'updated successfuly','success')
            return redirect("home:detail",post.id,post.slug)




class PostCreateView(LoginRequiredMixin,View):

    form_class = PostUpdateForms
    def get(self,req):
        form = self.form_class()
        return render(req,'home/create.html',{"form":form})

    def post(self,req):
        form = self.form_class(req.POST)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:35])
            new_post.user = req.user
            new_post.save()
            messages.success(req,'created successfuly','success')
            return redirect("home:detail",new_post.id,new_post.slug)
        messages.error(req,"you can't created",'danger')
        return redirect('home:home')


class PostAddReplyView(LoginRequiredMixin,View):

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(models.Post,id=kwargs['post_id'])
        self.comment_instance = get_object_or_404(models.Comment,id=kwargs['comment_id'])
        return super().setup( request, *args, **kwargs)
    form_class = ReplyCommentForm

    def get(self,req,post_id,comment_id):

        form = self.form_class()
        return render(req,'home/reply_comment.html',{'form':form,'post':self.post_instance,'comment':self.comment_instance})
    def post(self,req,post_id,comment_id):
        form = self.form_class(req.POST)
        post = self.post_instance
        comment = self.comment_instance
        if form.is_valid():
            reply=form.save(commit=False)
            reply.user = req.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(req,'reply submitted','success')
        return redirect('home:detail', post.id,post.slug)


class PostLikeView(LoginRequiredMixin,View):
    def get(self,req,post_id):
        post = get_object_or_404(models.Post,id=post_id)
        like = models.Vote.objects.filter(post=post,user=req.user)
        
        if like.exists():
            messages.error(req,'already liked','danger')
        else:
            models.Vote.objects.create(post=post,user=req.user)
            messages.success(req,'liked','success')
        return redirect('home:detail',post.id,post.slug)


class PostDislikeView(LoginRequiredMixin,View):
    def get(self,req,post_id):
        post = get_object_or_404(models.Post,id=post_id)
        like = models.Vote.objects.filter(post=post,user=req.user)
        if like.exists():
            like.delete()
            messages.success(req,'disliked','success')
        else:
            messages.error(req,'you are not liked before','danger')
        return redirect("home:detail",post.id,post.slug)