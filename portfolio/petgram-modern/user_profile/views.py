from django.shortcuts import render, redirect, get_object_or_404
from user_profile.models import CustomUser
from post.models import Post
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request, user_id):
    profile_user = CustomUser.objects.get(id=user_id)
    user_posts = Post.objects.filter(display_name=profile_user).order_by('-created_at')
    
    # Calculate counts dynamically
    following_count = profile_user.follows.count()
    follower_count = profile_user.followers.count() if hasattr(profile_user, 'followers') else 0

    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'user_posts': user_posts,
        'following_count': following_count,
        'follower_count': follower_count,
    })

@login_required
def follow_view(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)
    if target_user != request.user:
        request.user.follows.add(target_user)
    return redirect(f'/profile/{user_id}')

@login_required
def unfollow_view(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)
    if target_user != request.user:
        request.user.follows.remove(target_user)
    return redirect(f'/profile/{user_id}')

@login_required
def edit_profile_view(request, user_id):
    user_to_edit = get_object_or_404(CustomUser, id=user_id)
    if request.user != user_to_edit:
        return redirect(f'/profile/{request.user.id}')
    
    if request.method == 'POST':
        user_to_edit.bio = request.POST.get('bio', user_to_edit.bio)
        if 'profile_image' in request.FILES:
            user_to_edit.profile_image = request.FILES['profile_image']
        user_to_edit.save()
        return redirect(f'/profile/{user_id}')
        
    return render(request, 'edit_profile.html', {'user_to_edit': user_to_edit})

@login_required
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(CustomUser, id=user_id)
    if request.user == user_to_delete:
        user_to_delete.delete()
        return redirect('/signup/')
    return redirect(f'/profile/{user_id}')

@login_required
def search_bar(request):
    query = request.GET.get('q', '')
    users = CustomUser.objects.filter(username__icontains=query) if query else []
    return render(request, 'search_results.html', {'users': users, 'query': query})

def error_404_view(request, exception=None):
    return render(request, '404.html', status=404)

def error_500_view(request, exception=None):
    return render(request, '500.html', status=500)