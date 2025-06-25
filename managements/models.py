from django.db import models

class management(models.Model):
  firt_name = models.CharField(max_length=100, blank=False)
  last_name = models.CharField(max_length=100, blank=False)
  email = models.EmailField()
  date_of_birth = models.DateField()
  role = models.CharField(max_length=100,unique=True)
  department = models.CharField(max_length=100)

  def __str__(self):
    return f"{self.firt_name} {self.last_name} - {self.role}"
