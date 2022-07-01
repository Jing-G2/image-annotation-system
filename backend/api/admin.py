from django.contrib import admin
from .models import Labels, Dataset, AnnotatedSet, AnnotateText


@admin.register(Labels)
class LabelsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'color', 'shortcut', 'user_id')


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'status', 'num','publisher_id')


@admin.register(AnnotatedSet)
class AnnotatedSetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'status', 'num', 'owner_id')


@admin.register(AnnotateText)
class UploadTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
