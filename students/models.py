from django.db import models
class students(models.Model):
  surname = models.CharField(max_length=200, blank=False)
  first_name = models.CharField(max_length=50,blank=False)
  last_name = models.CharField(max_length=50, blank=False)
  date_of_birth = models.DateField()
  enrollment_date = models.DateField()
  email = models.EmailField(unique=True)
  student_id = models.CharField(max_length=150, unique=True)
  # students/models.py

  def __str__(self):
    return f"{self.surname} {self.firt_name} {self.last_name}"
  


    

