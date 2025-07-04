import graphene
from graphene_django import DjangoObjectType
from django_filters import FilterSet
from graphene_django.filter import DjangoFilterConnectionField
import graphene_django_optimizer as optimizer
from .models import students

class StudentType(DjangoObjectType):
    class Meta:
        model = students  
        fields = '__all__'
        interfaces = (graphene.relay.Node,)

class StudentFilter(FilterSet):
    class Meta:
        model = students
        fields = {
            'first_name': ['exact', 'icontains'],
            'surname': ['exact', 'icontains'],
            'student_id': ['exact'],
            'email': ['exact'],
        }

class Query(graphene.ObjectType):
    all_students = DjangoFilterConnectionField(StudentType, filterset_class=StudentFilter, max_limit=100)
    student_by_id = graphene.Field(StudentType, id=graphene.Int(required=True))

    def resolve_all_students(self, info, **kwargs):
        return optimizer.query(students.objects.select_related('courses').all(), info)

    def resolve_student_by_id(self, info, id):
        try:
            return students.objects.get(id=id)
        except students.DoesNotExist:
            return None

class CreateStudent(graphene.Mutation):
    class Arguments:
        surname = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        date_of_birth = graphene.Date(required=True)
        enrollment_date = graphene.Date(required=True)
        student_id = graphene.String(required=True)

    student = graphene.Field(StudentType)

    def mutate(self, info, surname, first_name, last_name, email, date_of_birth, enrollment_date, student_id):
        student = students(  
            surname=surname,
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_of_birth=date_of_birth,
            enrollment_date=enrollment_date,
            student_id=student_id
        )
        student.save()
        return CreateStudent(student=student)

class UpdateStudent(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        surname = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        date_of_birth = graphene.Date()
        enrollment_date = graphene.Date()
        student_id = graphene.String()

    student = graphene.Field(StudentType)

    def mutate(self, info, id, **kwargs):
        try:
            student = students.objects.get(id=id)
            for key, value in kwargs.items():
                setattr(student, key, value)
            student.save()
            return UpdateStudent(student=student)
        except students.DoesNotExist:
            raise Exception("Student not found")

class DeleteStudent(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            student = students.objects.get(id=id)
            student.delete()
            return DeleteStudent(success=True)
        except students.DoesNotExist:
            raise Exception("Student not found")

class Mutation(graphene.ObjectType):
    create_student = CreateStudent.Field()
    update_student = UpdateStudent.Field()
    delete_student = DeleteStudent.Field()