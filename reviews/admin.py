from django.contrib import admin
from .models import Review, Survey, SurveyResponse


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['created_at', 'rating', 'product']
    search_fields = ['user__username', 'product__name', 'content']
    date_hierarchy = 'created_at'
    readonly_fields = ['product', 'user', 'rating', 'content', 'created_at']


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'active']
    list_editable = ['active']
    search_fields = ['title']


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['survey', 'user', 'submitted_at']
    list_filter = ['survey', 'submitted_at']
    search_fields = ['survey__title', 'user__username']
    readonly_fields = ['survey', 'user', 'responses', 'submitted_at']
