import graphene
from graphene_django import DjangoObjectType
from .models import timeSlot, TimetableEntry
from courses.models import courses
from teachers.models import teachers

class TimeSlotType(DjangoObjectType):
    class Meta
        model = timeSlot
        fields = '__all__'

class TimetableEntryType(DjangoObjectType):
    class Meta:
        model = TimetableEntry
        fields = '__all__'

class Query(graphene.ObjectType):
    all_timeslots = graphene.List(TimeSlotType)
    all_timetable_entries = graphene.List(TimetableEntryType)
    timeslot_by_id = graphene.Field(TimeSlotType, id=graphene.Int(required=True))
    timetable_entry_by_id = graphene.Field(TimetableEntryType, id=graphene.Int(required=True))

    def resolve_all_timeslots(self, info):
        return timeSlot.objects.all()

    def resolve_all_timetable_entries(self, info):
        return TimetableEntry.objects.all()

    def resolve_timeslot_by_id(self, info, id):
        try:
            return timeSlot.objects.get(id=id)
        except timeSlot.DoesNotExist:
            return None

    def resolve_timetable_entry_by_id(self, info, id):
        try:
            return TimetableEntry.objects.get(id=id)
        except TimetableEntry.DoesNotExist:
            return None

class CreateTimeSlot(graphene.Mutation):
    class Arguments:
        day = graphene.String(required=True)
        start_time = graphene.Time(required=True)
        end_time = graphene.Time(required=True)
        room = graphene.String(required=True)

    timeslot = graphene.Field(TimeSlotType)

    def mutate(self, info, day, start_time, end_time, room):
        timeslot = timeSlot(day=day, start_time=start_time, end_time=end_time, room=room)
        timeslot.save()
        return CreateTimeSlot(timeslot=timeslot)

class CreateTimetableEntry(graphene.Mutation):
    class Arguments:
        course_id = graphene.Int(required=True)
        timeslot_id = graphene.Int(required=True)
        teacher_id = graphene.Int(required=True)
        semester = graphene.String(required=True)

    timetable_entry = graphene.Field(TimetableEntryType)

    def mutate(self, info, course_id, timeslot_id, teacher_id, semester):
        try:
            course = Courses.objects.get(id=course_id)
            timeslot =timeSlot.objects.get(id=timeslot_id)
            teacher = teachers.objects.get(id=teacher_id)
            entry = TimetableEntry(course=course, timeslot=timeslot, teacher=teacher, semester=semester)
            entry.save()
            return CreateTimetableEntry(timetable_entry=entry)
        except (Courses.DoesNotExist, timeSlot.DoesNotExist, teachers.DoesNotExist):
            raise Exception("Course, TimeSlot, or Teacher not found")

class Mutation(graphene.ObjectType):
    create_timeslot = CreateTimeSlot.Field()
    create_timetable_entry = CreateTimetableEntry.Field()