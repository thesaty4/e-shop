from os import truncate
from django.db.models.deletion import CASCADE
from accounts.models import User
from django.db import models
import datetime
from tinymce.models import HTMLField

# Create your models here.
class Blog(models.Model):
    customer_user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    tags = models.TextField(max_length=500)
    image = models.ImageField(upload_to='blogs/images/',null=True,blank=True)
    audio = models.FileField(upload_to='blogs/audio/',null=True,blank=True)
    video = models.URLField(null=True,blank=True)
    # discription = models.TextField(max_length=1000)
    discription = HTMLField()
    at_date_time = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.title[0:10])


# class Image(models.Model):
#     blogs = models.ForeignKey(Blog,on_delete=models.CASCADE)
#     img_path = models.ImageField(upload_to="blogs/imgs/")
#     def __str__(self):
#         return str(self.title[0:10])+"... Blog Image"

class Vote(models.Model):
    blogs = models.ForeignKey(Blog,on_delete=models.CASCADE)
    customer_user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_up_vote = models.BooleanField()
    vote_date_time = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.blogs)+"... vote"

class Comment(models.Model):
    customer_user = models.ForeignKey(User,on_delete=models.CASCADE)
    blogs = models.ForeignKey(Blog,on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)
    comment_date_time = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.blogs)+" by "+str(self.customer_user)

class CommentVote(models.Model):
    blogs = models.ForeignKey(Blog,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    customer_user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_up_vote = models.BooleanField()
    vote_date_time = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.blogs)+"... vote"

class CommentReply(models.Model):
    blogs_comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    customer_user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_reply = models.TextField(max_length=400)
    reply_date_time = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.blogs_comment)+"... vote"

# class SubCommentVote(models.Model):
#     blogs = models.ForeignKey(Blog,on_delete=models.CASCADE)
#     customer_user = models.ForeignKey(User,on_delete=models.CASCADE)
#     is_up_vote = models.BooleanField()
#     vote_date_time = models.DateTimeField(default=datetime.datetime.now())
#     def __str__(self):
#         return str(self.blogs[0:10])+"... vote"
      
