from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    body = models.TextField()
    slug = models.SlugField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created','-updated']

    def get_absolute_url(self):
        return reverse('home:detail',args=[self.id , self.slug])

    def like_count(self):
        return self.pvotes.count()

    def user_like(self,user):
        user_like = user.uvotes.filter(post=self)
        if user_like.exists():
            return True
        return False

    def __str__(self):
        return f'{self.user} {self.slug}'


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ucomment')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='pcomment')
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name='rcomment',blank=True,null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.post}"


class Vote(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='uvotes')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='pvotes')

    def __str__(self):
        return f"{self.user} {self.post.slug}"