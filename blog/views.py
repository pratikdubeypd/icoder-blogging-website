from ast import parse
from django import http
from django.shortcuts import render, HttpResponse, redirect
from .models import Blog, BlogComment
from django.contrib import messages
from blog.templatetags import extras

# Create your views here.
def blogHome(request):
    allBlogs = Blog.objects.all()
    dict = {'allBlogs':allBlogs}
    return render(request, 'blog/bloghome.html', dict)

def blogPost(request, slug):
    blogPost = Blog.objects.filter(slug=slug).first()
    blogPost.views+=1
    blogPost.save()
    comments = BlogComment.objects.filter(post=blogPost, parent = None)
    replies = BlogComment.objects.filter(post=blogPost).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    print(replyDict)
    dict = {'blogPost':blogPost, 'comments': comments, 'replyDict':replyDict, 'user':request.user}
    return render(request, 'blog/blogpost.html', dict)

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        parentSno = request.POST.get('parentSno')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Blog.objects.get(sno = postSno)
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, 'comment posted')
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, 'reply posted')
    return redirect(f"/blog/{post.slug}")