import graphene
from graphene_django import DjangoObjectType
from .models import Course
from teachers.models import Teacher
from students.models import Student

class CourseType(DjangoObjectType):
    class Meta:
        model = Course
        fields = '__all__'

class Query(graphene.ObjectType):
    all_courses = graphene.List(CourseType)
    course_by_id = graphene.Field(CourseType, id=graphene.Int(required=True))

    def resolve_all_courses(self, info):
        return Course.objects.all()

    def resolve_course_by_id(self, info, id):
        try:
            return Course.objects.get(id=id)
        except Course.DoesNotExist:
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
            teacher = Teacher.objects.get(id=teacher_id)
            course = Course(name=name, code=code, teacher=teacher, credits=credits)
            course.save()
            return CreateCourse(course=course)
        except Teacher.DoesNotExist:
            raise Exception("Teacher not found")

class EnrollStudent(graphene.Mutation):
    class Arguments:
        student_id = graphene.Int(required=True)
        course_id = graphene.Int(required=True)

    course = graphene.Field(CourseType)

    def mutate(self, info, student_id, course_id):
        try:
            student = Student.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)
            course.students.add(student)
            return EnrollStudent(course=course)
        except (Student.DoesNotExist, Course.DoesNotExist):
            raise Exception("Student or Course not found")

class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()
    enroll_student = EnrollStudent.Field()