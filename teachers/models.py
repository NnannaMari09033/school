from django.db import models

class teachers(models.Model):
  firts_name = models.CharField(max_length=50, blank=False)
  last_name = models.CharField(max_length=50, blank=False)
  date_of_birth = models.DateField()
  email = models.EmailField()
  hire_date = models.DateField()
  subject_specification = models.CharField(max_length=250)


  def __str__(self):
    return f"{self.firts_name} {self.last_name}"
  

