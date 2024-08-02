from django.contrib import admin
from .models import Post, PostCategory, Category


def nullify_rating(modeladmin, request, queryset):
    queryset.update(rating=0)


nullify_rating.short_description = 'Обнулить рейтинг'


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'dateCreation', 'rating']
    list_filter = ['title', 'dateCreation', 'rating']
    search_fields = ('title', 'postCategory__name')
    actions = [nullify_rating]


admin.site.register(Post, PostAdmin)
admin.site.register(Category)

# Register your models here.
