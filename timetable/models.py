# timetable/models.py
from django.db import models
from courses.models import courses  
from teachers.models import teachers

class timeslot(models.Model):
    day = models.CharField(
        max_length=10,
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday'),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.day} {self.start_time}-{self.end_time} ({self.room})"

    class Meta:
        unique_together = ('day', 'start_time', 'room')  # Optional: ensures unique time slots

class TimetableEntry(models.Model):
    course = models.ForeignKey(courses, on_delete=models.CASCADE, related_name='timetable_entries')
    timeslot = models.ForeignKey(timeslot, on_delete=models.CASCADE, related_name='timetable_entries')
    teacher = models.ForeignKey(teachers, on_delete=models.CASCADE, related_name='timetable_entries')
    semester = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.course.name} - {self.timeslot} ({self.semester})"

    class Meta:
        unique_together = ('course', 'timeslot', 'semester')