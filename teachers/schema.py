import graphene
from graphene_django import DjangoObjectType
from .models import Teacher

class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher
        fields = '__all__'

class Query(graphene.ObjectType):
    all_teachers = graphene.List(TeacherType)
    teacher_by_id = graphene.Field(TeacherType, id=graphene.Int(required=True))

    def resolve_all_teachers(self, info):
        return Teacher.objects.all()

    def resolve_teacher_by_id(self, info, id):
        try:
            return Teacher.objects.get(id=id)
        except Teacher.DoesNotExist:
            return None

class CreateTeacher(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        hire_date = graphene.Date(required=True)
        subject_specialization = graphene.String(required=True)

    teacher = graphene.Field(TeacherType)

    def mutate(self, info, first_name, last_name, email, hire_date, subject_specialization):
        teacher = Teacher(
            first_name=first_name,
            last_name=last_name,
            email=email,
            hire_date=hire_date,
            subject_specialization=subject_specialization
        )
        teacher.save()
        return CreateTeacher(teacher=teacher)

class Mutation(graphene.ObjectType):
    create_teacher = CreateTeacher.Field()