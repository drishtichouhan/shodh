from django.contrib import admin
from basic.models import User,  Student, Professor, Vacancy
# Register your models here.
admin.site.register(User)
# admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Vacancy)
