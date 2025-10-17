from django import forms
from django.contrib.auth.models import User
from .models import FriendRequest

class FriendRequestForm(forms.ModelForm):
    """Form for sending friend requests"""
    class Meta:
        model = FriendRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add a personal message (optional)...',
                'maxlength': '500'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].required = False

