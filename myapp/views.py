from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


# Create your views here.
def about(request):
    a = "<p>Welcome to CarOGraphy!</p>"
    return HttpResponse(a)