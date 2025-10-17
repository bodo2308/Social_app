from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm

def friends(request):
    """Friends page view - manage connections"""
    return render(request, 'accounts/friends.html')

@login_required
def profile(request):
    """Profile page view - view and edit user profile"""
    # Get or create profile for the user
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        # Debug: Print form data
        print(f"User form valid: {user_form.is_valid()}")
        print(f"Profile form valid: {profile_form.is_valid()}")
        
        if user_form.is_valid() and profile_form.is_valid():
            try:
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('accounts:profile')
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}')
                print(f"Error saving profile: {e}")
        else:
            # Show form errors
            if not user_form.is_valid():
                for field, errors in user_form.errors.items():
                    for error in errors:
                        messages.error(request, f'User {field}: {error}')
            if not profile_form.is_valid():
                for field, errors in profile_form.errors.items():
                    for error in errors:
                        messages.error(request, f'Profile {field}: {error}')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/profile.html', context)
