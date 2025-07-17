from django.contrib import admin
from .models import students
from unfold.admin import ModelAdmin
from .models import YourModel

@admin.register(YourModel)
class YourModelAdmin(ModelAdmin):
    ...

admin.site.register(students)

