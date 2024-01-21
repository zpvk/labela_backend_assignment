from django.http import JsonResponse
from rest_framework import generics

class NotFoundView(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request):
        return JsonResponse({
            'status_code': 404,
            'error': f'The {request.get_full_path()} was not found'
        })