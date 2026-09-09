from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from post.models import Post, Comment, Hashtags
from post.forms import PostForm, CommentForm
from user_profile.models import CustomUser
from notification.models import Notification, NotifyComment
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify
import re

@login_required
def homepage(request):
    notify = Notification.objects.filter(reciever=request.user, read=False).count()
    cnotify = NotifyComment.objects.filter(reciever=request.user, read=False).count()
    total_notify = notify + cnotify
    all_posts = Post.objects.all().order_by('-created_at')
    feed = [post for post in all_posts if post.display_name in request.user.follows.all() or request.user == post.display_name]
    most_recent = Post.objects.all().order_by('-created_at')[0:10]
    return render(request, 'homepage.html', {'feed': feed, 'total_notify': total_notify, 'most_recent': most_recent})

def error_404_view(request,):
    return render(request, '404.html', status=404)

def error_500_view(request):
    return render(request, '500.html', status=500)

@login_required
def post_view(request):
    notify = Notification.objects.filter(reciever=request.user, read=False).count()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_data = Post.objects.create(
                display_name = request.user,
                caption = form.cleaned_data['caption'],
                post_file = form.cleaned_data['post_file'],
            )

            hashtags = re.findall(r'#(\S+)', form.cleaned_data['caption'])
            for item in hashtags:
                tag = slugify(item[0:50])
                new_tag = Hashtags.objects.get_or_create(
                    slug = tag
                )[0]
                new_tag.post.add(new_data)
                new_tag.save()
                print(new_tag)
        
            notifications = re.findall(r'@(\S+)', form.cleaned_data['caption'])
            for string in notifications:
                user = CustomUser.objects.filter(username=string).first()
                if user:
                    Notification.objects.create(
                        read = False,
                        text = new_data,
                        reciever = user
                    )
            print(notifications)
            return redirect(reverse('post_detail', args=[new_data.id]))
    else:
        form = PostForm()
    return render(request, 'upload_form.html', {'form': form, 'notify': notify})

@login_required
def post_detail(request, post_id):
    notify = Notification.objects.filter(reciever=request.user, read=False).count()
    post = Post.objects.get(id=post_id)
    cap = post.caption.split(' ')
    hashtags = re.findall(r'#(\S+)', post.caption)
    cnotify = NotifyComment.objects.filter(reciever=request.user, read=False).count()
    total_notify = notify + cnotify
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            print(request.user.id)
            data=form.cleaned_data
            comment = Comment.objects.create(
                comment = data['comment'],
                user = request.user,
                post = post
            )
            return redirect(f'/post_detail/{post.id}')
    else: 
        form = CommentForm()
        comments = Comment.objects.filter(post_id=post.id).order_by('-created_at')
        return render(request, 'post_detail.html', {
            'post': post,
            'comments': comments, 
            'form': form, 
            'total_notify': total_notify, 
            'hashtags': hashtags, 
            'cap': cap
            })

@login_required
def comment_delete(request, id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    return redirect(f'/post_detail/{comment.post.id}')

@login_required
def users_feed(request):
    notify = Notification.objects.filter(reciever=request.user, read=False).count()
    cnotify = NotifyComment.objects.filter(reciever=request.user, read=False).count()
    total_notify = notify + cnotify
    tag = Post.objects.all().order_by('-created_at')
    multi_of_nine = []
    for i in range(1000):
        if i%9 == 0:
            multi_of_nine.append(i)
    return render(request, 'users_feed.html', {'tag': tag, 'total_notify': total_notify, 'multi_of_nine': multi_of_nine})

@login_required
def hashtag_view(request, slug_id):
    tag = Hashtags.objects.get(slug=slug_id)
    post = tag.post.all().order_by('-created_at')
    for item in post:
        caption = item.caption.split(' ')
        for word in caption:
            if word[0] == '#':
                hashtag = word
    return render(request, 'hashtag.html', {'tag':tag, 'post': post, 'hashtag': hashtag})

@login_required
def like_view(request, post_id):
    post = Post.objects.get(id=post_id)
    post.user_likes.add(request.user)
    post.likes += 1
    post.save()
    return HttpResponseRedirect(f'/post_detail/{post.id}')

@login_required
def unlike_view(request, post_id):
    post = Post.objects.get(id=post_id)
    post.user_likes.remove(request.user)
    post.likes -= 1
    post.save()
    return HttpResponseRedirect(f'/post_detail/{post.id}')

@login_required
def delete_post_view(request, post_id):
    current_post = Post.objects.get(id=post_id)
    current_post.delete()
    return HttpResponseRedirect('/')

@login_required
def editPost_view(request, post_id=id):
    notify = Notification.objects.filter(reciever=request.user, read=False).count()
    cnotify = NotifyComment.objects.filter(reciever=request.user, read=False).count()
    total_notify = notify + cnotify
    edit = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form =PostForm(request.POST, instance=edit)
        form.save()
        return HttpResponseRedirect(f'/post_detail/{post_id}')
    form = PostForm(instance=edit)
    return render(request, 'upload_form.html', {'total_notify': total_notify, 'form': form})

