from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)

# class Department(models.Model):
#     name = models.CharField(max_length = 264, unique=True)
#
#     def __str__(self):
#         return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rollnumber = models.IntegerField(unique=True,primary_key=True)
    # department = models.OneToOneField(Department, on_delete=models.CASCADE)
    # department = models.ForeignKey(Department, on_delete=models.CASCADE)


    def __str__(self):
        return  str(self.rollnumber)  + "--" + self.user.username

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # department = models.OneToOneField(Department, on_delete=models.CASCADE)
    # department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Vacancy(models.Model):
    name = models.CharField(max_length = 264,default = 'name')
    vacancyid = models.IntegerField(primary_key=True)
    department = models.CharField(max_length = 264,default = 'dept')
    prof_name = models.CharField(max_length = 264,default = 'profname')
    prof_email = models.CharField(max_length = 264, default = 'profmail')
    isopen = models.BooleanField(default=False)
    def __str__(self):
        return self.name

# class Vacancy(models.Model):
# 	vacancyid = models.IntegerField(unique=True)
# 	name = models.CharField(max_length=264,unique=True)
# 	department = models.ForeignKey(Department,on_delete=models.CASCADE)
# 	prof = models.ForeignKey(ProfUserInfo,on_delete=models.CASCADE)

# 	def __str__(self):
#         return self.name
