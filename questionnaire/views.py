from rest_framework import status
from . import models
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
# Stripe import


@api_view(['GET', 'POST'])
@permission_classes([])
def testing(request):
    if request.method == "GET":
        return JsonResponse({'message': 'Testing responce'}, status=status.HTTP_200_OK)
    if request.method == "POST":
        coming_data = JSONParser().parse(request)
        print(coming_data)
        return JsonResponse({'message': coming_data}, status=status.HTTP_200_OK)
