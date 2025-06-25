from django.db import models
from students.models import students
from courses.models import courses

class grades(models.Model):
  students = models.ForeignKey(students, on_delete=models.CASCADE, related_name='grades')
  courses = models.ForeignKey(courses, on_delete=models.CASCADE, related_name='grades')
  score = models.FloatField()  
  letter_grade = models.CharField(max_length=2) 
  semester = models.CharField(max_length=20)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta():
    unique_together = ('students', 'courses', 'semester')

  def __str__(self):
    return f"{self.students} {self.courses} {self.letter_grade}"
  