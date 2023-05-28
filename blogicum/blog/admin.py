from django.contrib import admin
from .models import Category, Location, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'is_published',
        'created_at',
        'title',
        'description',
        'slug',
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('title',)
    list_filter = ('title',)
    list_display_links = ('title',)


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'is_published',
        'created_at',
        'name'
    )
    search_fields = ('name',)
    list_filter = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'is_published',
        'created_at',
        'title',
        'pub_date',
        'author',
        'location',
        'category'
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
