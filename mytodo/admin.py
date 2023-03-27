from django.contrib import admin
from .models import MyUser, ToDoModel


# Register your models here.
admin.site.register(MyUser)
admin.site.register(ToDoModel)