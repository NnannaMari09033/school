import graphene
from graphene_django import DjangoObjectType
from .models import Grade
from students.models import students
from courses.models import courses

class GradeType(DjangoObjectType):
    class Meta:
        model = Grade
        fields = '__all__'

class Query(graphene.ObjectType):
    all_grades = graphene.List(GradeType)
    grade_by_id = graphene.Field(GradeType, id=graphene.Int(required=True))

    def resolve_all_grades(self, info):
        return Grade.objects.all()

    def resolve_grade_by_id(self, info, id):
        try:
            return Grade.objects.get(id=id)
        except Grade.DoesNotExist:
            return None

class CreateGrade(graphene.Mutation):
    class Arguments:
        student_id = graphene.Int(required=True)
        course_id = graphene.Int(required=True)
        score = graphene.Float(required=True)
        letter_grade = graphene.String(required=True)
        semester = graphene.String(required=True)

    grade = graphene.Field(GradeType)

    def mutate(self, info, student_id, course_id, score, letter_grade, semester):
        try:
            student = students.objects.get(id=student_id)
            course = courses.objects.get(id=course_id)
            grade = Grade(student=student, course=course, score=score, letter_grade=letter_grade, semester=semester)
            grade.save()
            return CreateGrade(grade=grade)
        except (students.DoesNotExist, courses.DoesNotExist):
            raise Exception("Student or Course not found")

class Mutation(graphene.ObjectType):
    create_grade = CreateGrade.Field()