from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import Post
from accounts.forms import PostForm

def inbox(request):
    """Messages inbox view"""
    return render(request, 'messaging/inbox.html')

def newsfeed(request):
    """Newsfeed view with post creation and display"""
    posts = Post.objects.all().order_by('-created_at')
    form = None
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                messages.success(request, 'Your post has been published!')
                return redirect('messaging:newsfeed')
        else:
            form = PostForm()
    
    context = {
        'posts': posts,
        'form': form
    }
    return render(request, 'messaging/newsfeed.html', context)
