from django.shortcuts import render
from courses.models import Course,Catagories


# Create your views here.
def index(request):
    catagory = Catagories.objects.all().order_by('id')[0:6]
    courses = Course.objects.all().order_by('id')

    context = {
        'catagory':catagory,
        'courses': courses

    }

    return render(request, 'home/index.html', context)


# def contact(request):
#     return render(request, 'home/contact.html')


def allcategory(request):
    return render(request, 'home/allcategory.html')


def about(request):
    return render(request, 'home/about.html')


def testing(request):
    return render(request, 'home/testing.html')