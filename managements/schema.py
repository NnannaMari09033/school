import graphene
from graphene_django import DjangoObjectType
from .models import management

class ManagementType(DjangoObjectType):
    class Meta:
        model = management
        fields = '__all__'

class Query(graphene.ObjectType):
    all_managements = graphene.List(ManagementType)
    management_by_id = graphene.Field(ManagementType, id=graphene.Int(required=True))

    def resolve_all_managements(self, info):
        return management.objects.all()

    def resolve_management_by_id(self, info, id):
        try:
            return management.objects.get(id=id)
        except management.DoesNotExist:
            return None

class CreateManagement(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        role = graphene.String(required=True)
        department = graphene.String()

    management = graphene.Field(ManagementType)

    def mutate(self, info, first_name, last_name, email, role, department=None):
        management = management(
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role,
            department=department or ''
        )
        management.save()
        return CreateManagement(management=management)

class Mutation(graphene.ObjectType):
    create_management = CreateManagement.Field()