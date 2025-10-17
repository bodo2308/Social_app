from django import forms
from django.contrib.auth.models import User
from .models import Profile, Post

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_picture', 'bio', 'phone',
            'employee_id', 'department', 'position', 
            'office_location'
        ]
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'id_profile_picture'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...',
                'maxlength': '500'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., (555) 123-4567'
            }),
            'employee_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., EMP001'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Engineering'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Senior Developer'
            }),
            'office_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Floor 3, Room 301'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            # Only validate if it's a new file upload (has content_type attribute)
            if hasattr(picture, 'content_type'):
                # Check file size (5MB max)
                if hasattr(picture, 'size') and picture.size > 5 * 1024 * 1024:
                    raise forms.ValidationError("Image file too large ( > 5MB )")
                
                # Check file type
                if not picture.content_type.startswith('image/'):
                    raise forms.ValidationError("File must be an image")
            # If it's an existing ImageFieldFile, just return it as-is
        return picture
    
    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        if employee_id:
            # Check if employee_id is unique (excluding current instance)
            if self.instance and self.instance.pk:
                existing = Profile.objects.filter(employee_id=employee_id).exclude(pk=self.instance.pk)
            else:
                existing = Profile.objects.filter(employee_id=employee_id)
            
            if existing.exists():
                raise forms.ValidationError("Employee ID already exists")
        return employee_id

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Share something with your team...',
                'class': 'form-control border-0 bg-transparent'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }