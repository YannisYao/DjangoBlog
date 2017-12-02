from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Category, Tag

#定制admin后台
class PostAdmin(admin.ModelAdmin):
		list_display = ['title','create_time','modified_time','category','author']

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
