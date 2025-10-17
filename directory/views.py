from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import FriendRequest, Friendship
from .forms import FriendRequestForm

def directory(request):
    """Main directory view with simple search"""
    members = Profile.objects.filter(is_active=True).select_related('user')
    
    # Simple search by name or username
    search_query = request.GET.get('search', '')
    if search_query:
        members = members.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )
    
    # Get friend status for each member (if user is logged in)
    friend_status = {}
    if request.user.is_authenticated:
        for member in members:
            if member.user != request.user:
                friend_status[member.user.id] = get_friend_status(request.user, member.user)
    
    context = {
        'members': members,
        'search_query': search_query,
        'friend_status': friend_status,
    }
    return render(request, 'directory/directory.html', context)

@login_required
def member_detail(request, user_id):
    """Detailed view of a specific member"""
    member = get_object_or_404(Profile, user_id=user_id, is_active=True)
    friend_status = get_friend_status(request.user, member.user)
    
    # Get recent posts by this member
    recent_posts = member.user.posts.all()[:5] if hasattr(member.user, 'posts') else []
    
    context = {
        'member': member,
        'friend_status': friend_status,
        'recent_posts': recent_posts,
    }
    return render(request, 'directory/member_detail.html', context)

@login_required
def send_friend_request(request, user_id):
    """Send a friend request to another user""" 
    if request.method == 'POST':
        to_user = get_object_or_404(User, id=user_id)
        
        if Friendship.are_friends(request.user, to_user):
            return JsonResponse({'success': False, 'message': 'You are already friends with this user.'})
        
        existing_request = FriendRequest.objects.filter(
            from_user=request.user,
            to_user=to_user,
            status='pending'
        ).first()
        
        if existing_request:
            return JsonResponse({'success': False, 'message': 'Friend request already sent.'})
        
        reverse_request = FriendRequest.objects.filter(
            from_user=to_user,
            to_user=request.user,
            status='pending'
        ).first()
        
        if reverse_request:
            reverse_request.status = 'accepted'
            reverse_request.save()
            Friendship.objects.create(user1=request.user, user2=to_user)
            
            return JsonResponse({
                'success': True, 
                'message': 'Friend request accepted! You are now friends.',
                'action': 'accepted'
            })
        
        any_existing = FriendRequest.objects.filter(
            from_user=request.user,
            to_user=to_user
        ).first()
        
        if any_existing:
            if any_existing.status in ['accepted', 'declined']:
                any_existing.status = 'pending'
                any_existing.message = request.POST.get('message', '')
                any_existing.save()
                return JsonResponse({
                    'success': True, 
                    'message': 'Friend request sent successfully!',
                    'action': 'sent'
                })
            else:
                return JsonResponse({'success': False, 'message': 'Friend request already exists.'})
        
        message = request.POST.get('message', '')
        friend_request = FriendRequest.objects.create(
            from_user=request.user,
            to_user=to_user,
            message=message
        )
        
        return JsonResponse({
            'success': True, 
            'message': 'Friend request sent successfully!',
            'action': 'sent'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request.'})

@login_required
def respond_friend_request(request, request_id, action):
    """Accept or decline a friend request"""
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    
    if friend_request.status != 'pending':
        return JsonResponse({'success': False, 'message': 'This request has already been processed.'})
    
    if action == 'accept':
        friend_request.status = 'accepted'
        friend_request.save()
        
        # Create friendship
        Friendship.objects.create(user1=friend_request.from_user, user2=friend_request.to_user)
        
        return JsonResponse({
            'success': True, 
            'message': f'You are now friends with {friend_request.from_user.get_full_name()}!',
            'action': 'accepted'
        })
    
    elif action == 'decline':
        friend_request.status = 'declined'
        friend_request.save()
        
        return JsonResponse({
            'success': True, 
            'message': 'Friend request declined.',
            'action': 'declined'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid action.'})

@login_required
def cancel_friend_request(request, request_id):
    """Cancel a sent friend request"""
    friend_request = get_object_or_404(FriendRequest, id=request_id, from_user=request.user)
    
    if friend_request.status != 'pending':
        return JsonResponse({'success': False, 'message': 'This request cannot be cancelled.'})
    
    friend_request.status = 'cancelled'
    friend_request.save()
    
    return JsonResponse({
        'success': True, 
        'message': 'Friend request cancelled.',
        'action': 'cancelled'
    })

@login_required
def remove_friend(request, user_id):
    """Remove a friend"""
    friend = get_object_or_404(User, id=user_id)
    
    if not Friendship.are_friends(request.user, friend):
        return JsonResponse({'success': False, 'message': 'You are not friends with this user.'})
    
    Friendship.objects.filter(
        Q(user1=request.user, user2=friend) | Q(user1=friend, user2=request.user)
    ).delete()
    
    return JsonResponse({
        'success': True, 
        'message': f'You are no longer friends with {friend.get_full_name()}.',
        'action': 'removed'
    })

@login_required
def my_friends(request):
    """View current user's friends"""
    friends = Friendship.get_friends(request.user)
    friend_profiles = Profile.objects.filter(user__in=friends, is_active=True)
    
    # Get only pending friend requests
    pending_requests = FriendRequest.objects.filter(
        to_user=request.user, 
        status='pending'
    ).select_related('from_user')
    
    context = {
        'friends': friend_profiles,
        'pending_requests': pending_requests,
    }
    return render(request, 'directory/my_friends.html', context)


def get_friend_status(user1, user2):
    """Get the friendship status between two users"""
    if user1 == user2:
        return 'self'
    
    if Friendship.are_friends(user1, user2):
        return 'friends'
    
    # Check for pending requests
    sent_request = FriendRequest.objects.filter(
        from_user=user1, 
        to_user=user2, 
        status='pending'
    ).first()
    
    if sent_request:
        return 'request_sent'
    
    received_request = FriendRequest.objects.filter(
        from_user=user2, 
        to_user=user1, 
        status='pending'
    ).first()
    
    if received_request:
        return 'request_received'
    
    return 'not_friends'
