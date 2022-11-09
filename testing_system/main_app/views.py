from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse({'ura': 'blya', 'user': request.user})
