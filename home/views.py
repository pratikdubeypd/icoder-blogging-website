from django.db.models import query
from django.shortcuts import render, HttpResponse, redirect
from .models import Contact
from blog.models import Blog
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

# Create your views here.
# HTML pages
def home(request):
    allBlogs = Blog.objects.all()
    dict = {'allBlogs':allBlogs}
    return render(request, 'home/home.html', dict)

def contact(request):
    if request.method=='POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        if len(name)<2 or len(email)<3 or len(desc)<5:
            messages.error(request, 'Please fill the form correctly.')
        
        else:
            contact = Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
            messages.success(request, 'Your form has been submitted.')
    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def search(request):
    search = request.GET.get('search')
    if len(search)>70:
        allBlogs = Blog.objects.none()
    else:
        allBlogsTitle = Blog.objects.filter(title__icontains=search)
        allBlogsContent = Blog.objects.filter(content__icontains=search)
        allBlogsGenre = Blog.objects.filter(genre__icontains=search)
        allBlogsAuthor = Blog.objects.filter(author__icontains=search)
        allBlogs = allBlogsContent.union(allBlogsTitle, allBlogsGenre, allBlogsAuthor)
    if allBlogs.count()==0:
        messages.warning(request, 'No results found.')
    dict = {'allBlogs':allBlogs, 'search':search}
    return render(request, 'home/search.html', dict)

# authentication apis
def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # Check for errorneous inputs
        if len(username) > 30:
            messages.error(request, 'Your username must be under 30 characters')
            return redirect('home')
        if not username.isalnum():
            messages.error(request, 'Your username must be alphanumeric')
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match')
            return redirect('home')
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Your account has been successfully created')
        return redirect('home')
    else:
        return HttpResponse('Not Allowed')

def handleLogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginusername = request.POST['loginusername']
        password = request.POST['password']
        # Check the user
        user = authenticate(username = loginusername, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('home')
    else:
        return HttpResponse('Not Allowed')

def handleLogout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect('home')
