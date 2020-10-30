from django.contrib import admin
from .models import  Todo
#to be able to read files from the models even if they are not editable
class TodoAdmin(admin.ModelAdmin):
    readonly_fields=("created",)
admin.site.register(Todo,  TodoAdmin)
# Register your models here.
