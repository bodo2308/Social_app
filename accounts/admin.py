from django.contrib import admin
from .models import Profile, Post, Friend

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'department', 'position', 'is_active', 'created_at']
    list_filter = ['department', 'position', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'employee_id', 'department', 'position']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['user__last_name', 'user__first_name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'content_preview', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'author__username']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['from_user__username', 'to_user__username']
