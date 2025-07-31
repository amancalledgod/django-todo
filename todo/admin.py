from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'complete', 'due_date', 'created')
    list_filter = ('complete', 'due_date')
    search_fields = ('title', 'description')
