from django.contrib import admin
from .models import *
from .forms import *


@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_displaly = ('name', 'user')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published')
    search_fields = ('title', 'body')
    prepopulated_fields = {
        'slug': ('title',)
    }

    filter_horizontal = ('categories',)
    form = PostForm

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'title',
                    'body',
                    'featured_image',
                    'categories',
                    'tags'
                )
            }
        ),
        (
            None,
            {
                'fields': (
                    'slug',
                    'author',
                    'blogger',
                    'published',
                    'excerpt'
                )
            }
        )
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(PostAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

        if db_field.name == 'author':
            field.initial = request.user

        return field
