from django.urls import path
from . import views
urlpatterns = [
    path('blogContaint/',views.blogContaint,name="blogContaint"),
    path('blogDetails/<int:id>',views.blogDetails,name="blogDetails"),
    path('blog-update/',views.blogUpdate,name="Dashboard"),
    path('delete-blog/',views.deleteBlog),
    path('new-blog-post/',views.addNewBlog,name="New Blog"),
    path('get-blog/',views.getBlog,name="get blog"),
    path('blog-comment/',views.blogComment,name="blog comment"),
    path('delete-comment/',views.deleteComment,name="delete comment"),
    path('blog-comment-reply/',views.blogCommentReply,name="Blog comment reply comment"),
    path('delete-reply-comment/<int:bid>',views.deleteCommentReply,name="Delete comment reply comment"),
    path('blog-comment-vote/',views.blogCommentVoting,name="blog comments voting"),
    path('blog-voting/',views.blogVoting,name="blog voting"),
    path('get-more-blog/',views.getMoreBLog,name="blog pagination"),
    path('get-queries-blog/',views.getQueryBlog,name="blog query blog"),
    path('get-blog-details/',views.getBlogDetails,name="blog deatils"),
    path('update-blog-post/',views.updateBlog,name="blog update"),
]