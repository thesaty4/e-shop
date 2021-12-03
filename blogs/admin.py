from django.contrib import admin
from .models import Blog, Comment, CommentReply, CommentVote, Vote
# Register your models here.
admin.site.register((Vote,CommentVote,CommentReply))

class CustBlog(admin.ModelAdmin):
    # fields = ('title','tags',)
    list_display = ('title','tags',)
    # list_filter=("tags",)
    # list_editable = ("tags",)

class CustComment(admin.ModelAdmin):
    list_display = ('blogs','customer_user',"comment_date_time")
    list_filter=("customer_user",)



admin.site.register(Blog,CustBlog)
admin.site.register(Comment,CustComment)