from django.db import models

from teachers.models import teachers
from courses.models import courses 

class timeslot(models.Model):
    day = models.CharField(max_length=10)  # e.g., Monday
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.day} {self.start_time}-{self.end_time} ({self.room})"

class TimetableEntry(models.Model):
    courses = models.ForeignKey(courses, on_delete=models.CASCADE, related_name='timetable_entries')
    timeslot = models.ForeignKey(timeslot, on_delete=models.CASCADE, related_name='timetable_entries')
    teachers = models.ForeignKey(teachers, on_delete=models.CASCADE, related_name='timetable_entries')
    semester = models.CharField(max_length=20)  # e.g., Fall 2025

    class Meta:
        unique_together = ('course', 'timeslot', 'semester')

    def __str__(self):
        return f"{self.course} - {self.timeslot}"