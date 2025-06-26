import graphene
from graphene_django import DjangoObjectType
from .models import courses
from teachers.models import teachers
from students.models import students

class CourseType(DjangoObjectType):
    class Meta:
        model = courses
        fields = '__all__'

class Query(graphene.ObjectType):
    all_courses = graphene.List(CourseType)
    course_by_id = graphene.Field(CourseType, id=graphene.Int(required=True))

    def resolve_all_courses(self, info):
        return courses.objects.all()

    def resolve_course_by_id(self, info, id):
        try:
            return courses.objects.get(id=id)
        except courses.DoesNotExist:
            return None

class CreateCourse(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        code = graphene.String(required=True)
        teacher_id = graphene.Int(required=True)
        credits = graphene.Int(required=True)

    course = graphene.Field(CourseType)

    def mutate(self, info, name, code, teacher_id, credits):
        try:
            teacher = teachers.objects.get(id=teacher_id)
            course = courses(name=name, code=code, teacher=teacher, credits=credits)
            course.save()
            return CreateCourse(course=course)
        except teachers.DoesNotExist:
            raise Exception("Teacher not found")

class EnrollStudent(graphene.Mutation):
    class Arguments:
        student_id = graphene.Int(required=True)
        course_id = graphene.Int(required=True)

    course = graphene.Field(CourseType)

    def mutate(self, info, student_id, course_id):
        try:
            student = students.objects.get(id=student_id)
            course = courses.objects.get(id=course_id)
            course.students.add(student)
            return EnrollStudent(course=course)
        except (students.DoesNotExist, courses.DoesNotExist):
            raise Exception("Student or Course not found")

class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()
    enroll_student = EnrollStudent.Field()