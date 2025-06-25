from django.db import models
from teachers.models import teachers
from students.models import students

class courses(models.Model):
  name = models.CharField(max_length=100)
  code = models.CharField(max_length=50, unique=True)
  teacher = models.ForeignKey(teachers, on_delete=models.CASCADE,  related_name='courses')
  students = models.ManyToManyField(students, related_name='courses')
  credits = models.PostiveIntegerField()

  def __str__(self):
    return {self.name}
  


