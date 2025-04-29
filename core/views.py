from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, CustomUser, Friendship, Story
from .forms import PostForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404


@login_required
def home(request):
    profile_user = request.user  # Get the currently logged-in user
    stories = Story.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(hours=24)
    ).order_by('-created_at')
    posts = Post.objects.all().order_by('-created_at')
    
    stories = Story.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(hours=24)
    ).order_by('-created_at')
 
    posts = Post.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'core/home.html', {'posts': posts, 'form': form,'stories': stories,   'profile_user': profile_user,})

@login_required
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        if post.user == request.user:
            post.delete()
            messages.success(request, 'Post deleted successfully.')
        else:
            messages.error(request, 'You are not authorized to delete this post.')
    except Post.DoesNotExist:
        messages.error(request, 'Post not found.')
    return redirect('home')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def example_view(request):
    return render(request, 'base.html')

from django.http import JsonResponse
from .models import Like, Comment



from django.http import JsonResponse
from .forms import CommentForm
from .models import Comment

def add_comment(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            
            return JsonResponse({
                'success': True,
                'comment': {
                    'content': comment.content,
                    'username': comment.user.username,
                    'profile_pic': comment.user.profile_picture.url if comment.user.profile_picture else '',
                    'created_at': comment.created_at.strftime("%b %d, %Y %I:%M %p")
                }
            })
    return JsonResponse({'success': False, 'error': 'Invalid request'})
    
@login_required
def send_friend_request(request, user_id):
    to_user = CustomUser.objects.get(id=user_id)
    friendship, created = Friendship.objects.get_or_create(
        from_user=request.user,
        to_user=to_user,
        defaults={'status': 'pending'}
    )
    
    if not created and friendship.status == 'rejected':
        friendship.status = 'pending'
        friendship.save()
    
    return redirect('profile', username=to_user.username)

@login_required
def respond_friend_request(request, request_id, action):
    friendship = Friendship.objects.get(id=request_id)
    
    if friendship.to_user == request.user:
        if action == 'accept':
            friendship.status = 'accepted'
        elif action == 'reject':
            friendship.status = 'rejected'
        friendship.save()
    
    return redirect('friends')


@login_required
def create_story(request):
    if request.method == 'POST':
        story = Story.objects.create(
            user=request.user,
            image=request.FILES.get('image'),
            video=request.FILES.get('video')
        )
        return redirect('home')
    return render(request, 'core/create_story.html')

@login_required
def view_stories(request):
    # Get stories from friends that are not expired
    friends = CustomUser.objects.filter(
        Q(received_requests__from_user=request.user, received_requests__status='accepted') |
        Q(sent_requests__to_user=request.user, sent_requests__status='accepted')
    ).distinct()
    
    stories = Story.objects.filter(
        user__in=friends,
        created_at__gte=timezone.now() - timezone.timedelta(days=1)
    ).order_by('-created_at')
    
    return render(request, 'core/stories.html', {'stories': stories})





from django.db.models import Q

@login_required
def search(request):
    query = request.GET.get('q', '')
    users = CustomUser.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
    posts = Post.objects.filter(content__icontains=query)
    return render(request, 'core/search_results.html', {'users': users, 'posts': posts, 'query': query})

def search(request):
    query = request.GET.get('q', '')
    users = CustomUser.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
    posts = Post.objects.filter(content__icontains=query)
    return render(request, 'core/search_results.html', {'users': users, 'posts': posts, 'query': query})




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Story
from django.utils import timezone

@login_required
def view_stories(request):
    # Get stories from friends and filter out expired ones
    stories = Story.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(hours=24)
    ).order_by('-created_at')
    return render(request, 'core/stories.html', {'stories': stories})

@login_required
def create_story(request):
    if request.method == 'POST':
        story = Story.objects.create(
            user=request.user,
            image=request.FILES.get('image'),
            video=request.FILES.get('video')
        )
        return redirect('view_stories')
    return render(request, 'core/create_story.html')


def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'core/post.html', {'post': post})




from django.shortcuts import render

def search(request):
    query = request.GET.get('q', '')
    # Your search logic here
    results = []  # Replace with actual search results
    return render(request, 'core/search_results.html', {
        'query': query,
        'results': results
    })
    
    
    
    
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'core/post.html', {'form': form})




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'core/post_edit.html', {'form': form})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('home')
    return render(request, 'core/post_delete.html', {'post': post})






from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment
from .forms import CommentForm

@login_required
def comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('comment_view', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'core/comment.html', {'post': post, 'comments': comments, 'form': form})





from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Like

@login_required
def like_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    likes = post.likes.all()  # Access the related likes using the `related_name`
    for like in likes:
        if not like.user.profile_picture:
            like.user.profile_picture_url = '/static/images/default_profile_picture.png'
        else:
            like.user.profile_picture_url = like.user.profile_picture.url
    user_has_liked = likes.filter(user=request.user).exists()

    if request.method == 'POST':
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            messages.success(request, 'You unliked the post.')
        else:
            messages.success(request, 'You liked the post.')
        return redirect('like_view', post_id=post.id)

    return render(request, 'core/likes.html', {'post': post, 'likes': likes, 'user_has_liked': user_has_liked})





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, Friendship

@login_required
def search_users(request):
    query = request.GET.get('q', '')
    users = CustomUser.objects.filter(username__icontains=query).exclude(id=request.user.id)
    return render(request, 'core/friendship.html', {'users': users, 'query': query})

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(CustomUser, id=user_id)
    friendship, created = Friendship.objects.get_or_create(
        from_user=request.user,
        to_user=to_user,
        defaults={'status': 'pending'}
    )
    if created:
        messages.success(request, f'Friend request sent to {to_user.username}.')
    else:
        messages.info(request, f'You have already sent a friend request to {to_user.username}.')
    return redirect('search_users')






from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, Friendship

@login_required
def friend_view(request):
    users = CustomUser.objects.exclude(id=request.user.id)  # Exclude the current user
    return render(request, 'core/friend.html', {'users': users})

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(CustomUser, id=user_id)
    friendship, created = Friendship.objects.get_or_create(
        from_user=request.user,
        to_user=to_user,
        defaults={'status': 'pending'}
    )
    if created:
        messages.success(request, f'Friend request sent to {to_user.username}.')
    else:
        messages.info(request, f'You have already sent a friend request to {to_user.username}.')
    return redirect('friend_page')

@login_required
def manage_friend_requests(request):
    received_requests = Friendship.objects.filter(to_user=request.user, status='pending')
    return render(request, 'core/manage_friend_requests.html', {'received_requests': received_requests})

@login_required
def respond_friend_request(request, request_id, action):
    friendship = get_object_or_404(Friendship, id=request_id, to_user=request.user)
    if action == 'accept':
        friendship.status = 'accepted'
        messages.success(request, f'You are now friends with {friendship.from_user.username}.')
    elif action == 'reject':
        friendship.status = 'rejected'
        messages.info(request, f'You rejected the friend request from {friendship.from_user.username}.')
    friendship.save()
    return redirect('manage_friend_requests')





from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import CommentForm

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'core/details.html', {'post': post, 'comments': comments, 'form': form})

from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .models import Comment
from .forms import CommentForm

@login_required
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this comment.")
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'core/comment_edit.html', {'form': form, 'comment': comment})

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('post_detail', post_id=comment.post.id)
    
    return render(request, 'core/comment_confirm_delete.html', {'comment': comment})