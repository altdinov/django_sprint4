from django.contrib import admin

from .models import Category, Location, Post, Comment


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
    list_display_links = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'is_published',
        'created_at',
        'pub_date',
        'title',
        'author',
        'location',
        'category',
        'comments_number'
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('title',)
    list_display_links = ('title',)

    @admin.display(description="Кол-во ком.")
    def comments_number(self, obj):
        return obj.comments.all().count()


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'author',
        'post',
        'text',
    )
    search_fields = ('author',)
    list_display_links = ('author', 'text',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
