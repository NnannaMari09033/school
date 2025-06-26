import graphene
from students.schema import Query as StudentQuery, Mutation as StudentMutation
from teachers.schema import Query as TeacherQuery, Mutation as TeacherMutation
from managements.schema import Query as ManagementQuery, Mutation as ManagementMutation
from courses.schema import Query as CourseQuery, Mutation as CourseMutation
from grades.schema import Query as GradeQuery, Mutation as GradeMutation
from timetable.schema import Query as TimetableQuery, Mutation as TimetableMutation

class Query(
    StudentQuery,
    TeacherQuery,
    ManagementQuery,
    CourseQuery,
    GradeQuery,
    TimetableQuery,
    graphene.ObjectType
):
    pass

class Mutation(
    StudentMutation,
    TeacherMutation,
    ManagementMutation,
    CourseMutation,
    GradeMutation,
    TimetableMutation,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)