from django.db import connection
from EshopApp.templatetags.filter_tags import get_blog_total_vote
from django.contrib import messages
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from EshopApp.models import SiteInfo
from EshopApp.views import meta_data
from .blog_form import BlogForm,BlogImageForm,BlogAudioForm, BlogOnlyFrom
new_blog_form=BlogForm()
blog_image_form=BlogImageForm()
blog_audio_form=BlogAudioForm()
site_info_data=SiteInfo.objects.last()

# Create your views here.
def blogContaint(request):
    try:
        request.GET['q']
        query=dataValidate(request.GET['q'])
        blog=Blog.objects.filter(Q(tags__contains=query) | Q(title__contains=query) | Q(discription__contains=query)).order_by("-id")
        if blog.count() == 0:
            return redirect('/empty-blog/')
        else:
            return render(request,"blogs.html",{            
                'site_info_data':site_info_data,'product_meta_data':meta_data(),
                'blogs':blog,
                'query':query
        })
    except:
        return render(request,"blogs.html",{            
            'site_info_data':site_info_data,'product_meta_data':meta_data()
        })
    
def blogDetails(request,id):
    blog = Blog.objects.get(id=id)
    return render(request,"blog-detail.html",{            
        'site_info_data':site_info_data,'product_meta_data':meta_data(),'blog_item':blog,
    })

def blogUpdate(request):
        return render(request,"blog-dashboard.html",{            
            'site_info_data':site_info_data,'product_meta_data':meta_data(),'new_blog_form':new_blog_form,'at_blog_update':'at_blog_update'
        })

from extraPackage.auth import dataValidate
from .models import Blog,Comment, CommentVote, Vote
 

def addNewBlog(request):
    if request.method == 'POST'  and request.POST['customer_user'] == str(request.user.id):
        media = dataValidate(request.POST['blog-media']).lower()
        title = dataValidate(request.POST['title'])
        tags = dataValidate(request.POST['tags'])
        discription = request.POST['discription']
        uid=request.user
        if media == 'none':
            Blog(customer_user=uid,title=title,tags=tags,discription=discription,video='',image='',audio='').save()
        elif media == 'image':
            form = BlogForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
            else:
                return HttpResponse("Invalid form")            
            # Blog(customer_user=uid,title=title,tags=tags,discription=discription).save()
        elif media == 'audio':
            form = BlogAudioForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
            else:
                return HttpResponse("Invalid form")            
            # audio=request.FILES['audio']
            # Blog(customer_user=uid,title=title,tags=tags,discription=discription,video='',image='',audio=audio).save()
        elif media == 'video':
            video=request.POST['video']
            Blog(customer_user=uid,title=title,tags=tags,discription=discription,audio='',image='',video=video).save()

        messages.success(request,'You blog has been posted. Thank you !')
        return redirect('/blogs/new-blog-post/')
    else:
        return render(request,"blog-add.html",{            
            'site_info_data':site_info_data,'product_meta_data':meta_data(),'new_blog_form':new_blog_form
        })
import os
def updateBlog(request):
    if request.method == 'POST' and request.POST['customer_user'] == str(request.user.id):
        bid = request.POST['blog-id']
        media = dataValidate(request.POST['blog-media']).lower()
        title = dataValidate(request.POST['title'])
        tags = dataValidate(request.POST['tags'])
        discription = request.POST['discription']
        uid=request.user.id
        blogs = Blog.objects.get(customer_user=uid,id=bid)
        if media == 'none':
            Blog.objects.filter(customer_user=uid,id=bid).update(title=title,tags=tags,discription=discription,image='',video='',audio='')
            # Blog(customer_user=uid,title=title,tags=tags,discription=discription).save()
        elif media == 'image':
            # print(request.POST)
            instance = get_object_or_404(Blog,id=bid)
            if(request.POST['x'] == '0' or request.POST['y'] == '0' or request.POST['height'] == '0' or request.POST['width'] == '0'):
                blg = Blog.objects.get(id=int(request.POST['blog-id']))
                try:os.remove("media/%s"%(blogs.image))
                except:a=0
                form = BlogOnlyFrom(request.POST,request.FILES,instance=instance)
            else:
                blg = Blog.objects.get(id=int(request.POST['blog-id']))
                try:os.remove("media/%s"%(blg.image))
                except:a=0
                form = BlogImageForm(request.POST,request.FILES,instance=instance)

            if form.is_valid():
                form.save()
            else:
                return HttpResponse("Invalid form")            
            # Blog(customer_user=uid,title=title,tags=tags,discription=discription).save()
        elif media == 'audio':
            instance = get_object_or_404(Blog,id=bid)
            # print(request.POST)
            # print("satya")
            blg = Blog.objects.get(id=int(request.POST['blog-id']))
            try:os.remove("media/%s"%(blg.audio))
            except:a=0
            form = BlogAudioForm(request.POST,request.FILES,instance=instance)
            if form.is_valid():
                form.save()
            else:
                return HttpResponse("Invalid form") 
            # Blog(customer_user=uid,title=title,tags=tags,discription=discription,audio=audio).save()
        elif media == 'video':
            video=request.POST['video']
            Blog.objects.filter(customer_user=uid,id=bid).update(title=title,tags=tags,discription=discription,audio='',image='',video=video)
            # Blog(customer_user=uid,title=title,tags=tags,discription=discription,video=video).save()
        

        messages.success(request,'Your blog has been updated. Thank you !')
        return redirect('/blogs/blog-update/#update-blog-section')
    else:
        return render(request,"blog-add.html",{            
            'site_info_data':site_info_data,'product_meta_data':meta_data(),'new_blog_form':new_blog_form
        })

def getBlog(request):
    bid = request.GET['blog-id']
    label = request.GET['label']
    blogs=Blog.objects.all()
    blog_ids=[]
    for blog in blogs:
        blog_ids.append(blog.id)
    index_of_current_blog=blog_ids.index(int(bid))
    if blog_ids[0] == blog_ids.index(index_of_current_blog) or blog_ids[-1]==blog_ids.index(index_of_current_blog):
        blog_item = Blog.objects.get(id=int(bid))
    else:
        if label == 'prev':
            prev_id = blog_ids.index(index_of_current_blog)-1
            blog_item = Blog.objects.get(id=prev_id)
        elif label == 'next':
            next = blog_ids.index(index_of_current_blog)+1
            blog_item = Blog.objects.get(id=next)
    
    return render(request,'include/blog/blog-post-data.html',{'blog_item':blog_item})

from accounts.models import User
import pandas as pd
import numpy as np
import pickle

from sklearn.feature_extraction.text import CountVectorizer 
def check_spam(msg):
    with open("site-information/Machine-Learning-data/svc_algo.sav","rb") as file:
        (svc_algo,cols)=pickle.load(file)
    # print(svc_algo)
    vect=CountVectorizer()
    vect.fit([msg])
    msg_matrix=vect.transform([msg])
    msg_dense_matrix=msg_matrix.toarray()
    msg_df=pd.DataFrame(msg_dense_matrix)
    msg_deff = set(cols)-set(msg_df.columns)
    for i in msg_deff:
        msg_df[i]=0
    msg_type = svc_algo.predict(msg_df)
    return msg_type[0]

def blogComment(request):
    uid = request.user.id
    data = request.GET['comment']
    bid = request.GET['blog-id']
    if ':' in data or '/' in data or '<script>' in data:
        messages.warning(request,"Sorry, Spam Message isn't allowed !")
        return redirect("/blogs/blogDetails/"+str(bid)+"#msg")
    else:
        # CHECKING IS THIS MESSAGE SPAM?
        msg_status = check_spam(data)
        if msg_status == 'spam':
            messages.warning(request,"Sorry, Spam Message isn't allowed !")
            return redirect("/blogs/blogDetails/"+str(bid)+"#msg")
        else:
            data = dataValidate(data)
            user = User.objects.get(id=uid)
            blogs = Blog.objects.get(id=bid)
            obj=Comment(customer_user=user,blogs=blogs,comment=data)
            obj.save()
            return redirect("/blogs/blogDetails/"+str(bid))

def deleteComment(request):
    uid = request.user.id
    cid = request.GET['comment-id']
    Comment.objects.filter(customer_user=uid,id=cid).delete()
    return HttpResponse("Deleted")

from blogs.models import CommentReply
def blogCommentReply(request):
    uid = request.user.id
    cid = request.GET['comment-id']
    bid = request.GET['blog-id']
    user = User.objects.get(id=uid)
    comment = Comment.objects.get(id=cid)
    data = dataValidate(request.GET['comment'])
    CommentReply(blogs_comment=comment,customer_user=user,comment_reply=data).save()
    return redirect("/blogs/blogDetails/"+str(bid))

def deleteCommentReply(request,bid):
    uid = request.user
    cid = request.GET['comment-id']
    CommentReply(id=cid,customer_user=uid).delete()
    return redirect("/blogs/blogDetails/"+str(bid))

from EshopApp.templatetags.filter_tags import get_comment_total_upvote,get_comment_total_downvote
def blogCommentVoting(request):
    uid = request.user.id
    bid = request.GET['bid']
    cid = request.GET['cid']
    type = request.GET['vote-type']
    action = request.GET['action']
    def get_data(bid,uid,cid):
        blog=Blog.objects.get(id=bid)
        user=User.objects.get(id=uid)
        comment=Comment.objects.get(id=cid)
        return [blog,user,comment]

    if type == 'upvote' and action == 'remove':
        CommentVote.objects.filter(blogs=bid,customer_user=uid,comment=cid,is_up_vote=True).delete()
    elif type == 'downvote' and action == 'remove':
        CommentVote.objects.filter(blogs=bid,customer_user=uid,comment=cid,is_up_vote=False).delete()
    elif type == 'upvote' and action == 'add':
        data = get_data(bid,uid,cid)
        CommentVote.objects.filter(blogs=bid,customer_user=uid,comment=cid,is_up_vote=False).delete()
        CommentVote(blogs=data[0],customer_user=data[1],comment=data[2],is_up_vote=True).save()
    elif type == 'downvote' and action == 'add':
        data = get_data(bid,uid,cid)
        CommentVote.objects.filter(blogs=bid,customer_user=uid,comment=cid,is_up_vote=True).delete()
        CommentVote(blogs=data[0],customer_user=data[1],comment=data[2],is_up_vote=False).save()

    return HttpResponse(str(get_comment_total_upvote(bid,cid).count())+","+str(get_comment_total_downvote(bid,cid).count()))

def blogVoting(request):
    uid = request.user.id
    bid = request.GET['blog-id']
    type = request.GET['vote-type']
    action = request.GET['action']
    def get_data(bid,uid):
        blog=Blog.objects.get(id=bid)
        user=User.objects.get(id=uid)
        return [blog,user]

    if type == 'upvote' and action == 'remove':
        Vote.objects.filter(blogs=bid,customer_user=uid,is_up_vote=True).delete()
    elif type == 'downvote' and action == 'remove':
        Vote.objects.filter(blogs=bid,customer_user=uid,is_up_vote=False).delete()
    elif type == 'upvote' and action == 'add':
        data = get_data(bid,uid)
        Vote.objects.filter(blogs=bid,customer_user=uid,is_up_vote=False).delete()
        Vote(blogs=data[0],customer_user=data[1],is_up_vote=True).save()
    elif type == 'downvote' and action == 'add':
        data = get_data(bid,uid)
        Vote.objects.filter(blogs=bid,customer_user=uid,is_up_vote=True).delete()
        Vote(blogs=data[0],customer_user=data[1],is_up_vote=False).save()

    return HttpResponse(str(get_blog_total_vote(bid,'upvote').count())+","+str(get_blog_total_vote(bid,'downvote').count()))


def getMoreBLog(request):
    user=request.user
    start=request.GET['start']
    end=request.GET['end']
    order_by=request.GET['order-by']
    # print(request.GET['query'])
    query=dataValidate(request.GET['query'])
    if query == '' or query == None:
        blog=Blog.objects.all().order_by(order_by)[int(start):int(end)]
        return render(request,'request_data/blog-containt.html',{'blogs':blog,'user':user})
    else:
        blog=Blog.objects.filter(Q(tags__contains=query) | Q(title__contains=query) | Q(discription__contains=query)).order_by("-id")[int(start):int(end)]
        return render(request,'request_data/blog-containt.html',{'blogs':blog,'user':user})
        

from django.db.models import Q
def getQueryBlog(request):
    user=request.user.id
    query=dataValidate(request.GET['q'])
    blog=Blog.objects.filter(Q(tags__contains=query) | Q(title__contains=query) | Q(discription__contains=query)).order_by("-id")
    return render(request,'request_data/blog-containt.html',{'blogs':blog,'user':user})

def getBlogDetails(request):
    user=request.user.id
    blog_id = request.GET['blog-id']
    blog=Blog.objects.get(id=blog_id,customer_user=user)
    if blog.image == None: image=""
    else: image=blog.image

    if blog.audio == None: audio=""
    else: audio=blog.audio

    if blog.video == None: video=""
    else:video=blog.video
    return HttpResponse(str(blog.id)+"::"+blog.title+"::"+blog.tags+"::"+blog.discription+"::"+str(image)+"::"+str(audio)+"::"+str(video))
import os

def deleteBlog(request):
    usr = request.user.id
    bid = request.GET['blog-id']
    blog = Blog.objects.get(id=bid,customer_user=usr)
    try:os.remove("media/%s"%(blog.image))
    except:
        try:os.remove("media/%s"%(blog.audio))
        except: a=0
    Blog.objects.filter(customer_user=usr,id=bid).delete()
    return HttpResponse("Blog Has been deleted !")