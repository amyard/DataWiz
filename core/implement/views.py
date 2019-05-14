from django.shortcuts import render



def index(request):
    return render(request, 'implement/main.html', context={'test':'AWESOME'})