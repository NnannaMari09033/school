import graphene
from graphene_django import DjangoObjectType
from .models import Student

class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        fields = '__all__'

class Query(graphene.ObjectType):
    all_students = graphene.List(StudentType)
    student_by_id = graphene.Field(StudentType, id=graphene.Int(required=True))

    def resolve_all_students(self, info):
        return Student.objects.all()

    def resolve_student_by_id(self, info, id):
        try:
            return Student.objects.get(id=id)
        except Student.DoesNotExist:
            return None

class CreateStudent(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        date_of_birth = graphene.Date(required=True)
        enrollment_date = graphene.Date(required=True)
        student_id = graphene.String(required=True)

    student = graphene.Field(StudentType)

    def mutate(self, info, first_name, last_name, email, date_of_birth, enrollment_date, student_id):
        student = Student(
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_of_birth=date_of_birth,
            enrollment_date=enrollment_date,
            student_id=student_id
        )
        student.save()
        return CreateStudent(student=student)

class Mutation(graphene.ObjectType):
    create_student = CreateStudent.Field()