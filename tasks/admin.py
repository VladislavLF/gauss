from django.contrib import admin

# Register your models here.

from .models import *

class Category_Tasks_Filter_Admin(admin.ModelAdmin):
   prepopulated_fields = {"slug": ("name",)}


admin.site.register(Task)
admin.site.register(Category_Options)
admin.site.register(Category_Tasks)
admin.site.register(Theory_item)
admin.site.register(Theory_category)
admin.site.register(Category_Tasks_Filter, Category_Tasks_Filter_Admin)
admin.site.register(Comment)

