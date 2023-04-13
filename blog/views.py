from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import CommentForm, PostForm
from .models import Post, Tag

def frontpage(request):
    posts = Post.objects.all()

    return render(request, 'blog/frontpage.html', {'posts': posts})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, 'Your post has been created!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

def post_detail(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

def posts_by_tag(request, slug):
    tag = Tag.objects.get(slug=slug)
    posts = Post.objects.filter(tags=tag)
    other_tags = Tag.objects.exclude(slug=slug)
    context = {'tag': tag, 'posts': posts, 'other_tags': other_tags}
    return render(request, 'blog/posts_by_tag.html', context)