from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.db.models import Q
from accounts.models import User

@login_required
def post_list(request):
    # Base query for posts user can see
    if request.user.role == User.VISITOR or not request.user.department:
        # Visitors see only general posts
        posts = Post.objects.filter(target_type='GE')
    else:
        # Department members see general + department-related posts
        posts = Post.objects.filter(
            Q(target_type='GE') | 
            Q(department=request.user.department) |
            Q(course__department=request.user.department) |
            Q(professor=request.user)
        ).distinct()
    
    posts = posts.order_by('-created_at')
    
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    
    return render(request, 'posts/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

@login_required
def create_post(request):
    # Deny visitors the ability to create posts
    if request.user.role == User.VISITOR:
        messages.error(request, 'Visitors are not allowed to create posts.')
        return redirect('post_list')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            # Set target_type based on selected target
            if post.department:
                post.target_type = Post.DEPARTMENT
            elif post.course:
                post.target_type = Post.COURSE
            elif post.professor:
                post.target_type = Post.PROFESSOR
            else:
                post.target_type = Post.GENERAL
                
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm(user=request.user)
    
    return render(request, 'posts/post_form.html', {'form': form})