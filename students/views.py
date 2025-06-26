from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student
from rest_framework.decorators import api_view
import json

@csrf_exempt
@api_view(['GET', 'POST'])
def student_list(request):
    if request.method == 'GET':
        students = Student.objects.all()
        data = [{
            'id': student.id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'student_id': student.student_id
        } for student in students]
        return JsonResponse({'students': data})

    elif request.method == 'POST':
        data = json.loads(request.body)
        student = Student.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            date_of_birth=data['date_of_birth'],
            enrollment_date=data['enrollment_date'],
            student_id=data['student_id']
        )
        return JsonResponse({
            'id': student.id,
            'first_name': student.first_name,
            'student_id': student.student_id
        }, status=201)
    