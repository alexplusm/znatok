from django.shortcuts import render

from django.http import HttpResponse


def site(request):
    return render(request, 'site.html')

def registration(request):
	return render(request, 'registration.html')