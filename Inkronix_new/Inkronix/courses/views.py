from django.shortcuts import render
from django.views.generic import CreateView
from django.shortcuts import redirect
from .forms import Course_Form
from .models import *
from django.db.models import Sum
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core import paginator
from django.core.paginator import Paginator


# Create your views here.
def courses(request):
    catagory = Catagories.get_all_catagory(Catagories)
    courses = Course.objects.all()
    level  = Level.objects.all()
    pag    = Paginator(Course.objects.all(), 2)
    page = request.GET.get('page')
    courses_all = pag.get_page(page)
    nums = "a" * courses_all.paginator.num_pages

    context = {
        'catagory':catagory, 
        'courses': courses,
        'level' : level,
        'courses_all': courses_all,
        'nums':nums,
    }
    return render(request, 'courses/courses.html', context)


class course_added(CreateView):
    model = Course()
    form_class = Course_Form
    template_name = 'instructor/instructor-add-course.html'

    def form_valid(self, form):
        course = form.save()
        return redirect('courses')


def courseDetails(request, slug):
    catagory = Catagories.get_all_catagory(Catagories)
    courses = Course.objects.filter(slug = slug)
    time_duration = Video.objects.filter(courses__slug = slug).aggregate(sum=Sum('time_duration'))
    
    context = {
        'courses':courses,
        'catagory':catagory,
        'time_duration':time_duration
    }
    return render(request, 'courses/course-details.html', context)


def courseList(request):
    return render(request, 'courses/course-list.html')

def filter_data(request):
    category = request.GET.get('catagory[]')
    level = request.GET.get('level[]')

    if category:
        course = Course.objects.filter(category__id__in = category).order_by('id')
    elif level:
        course = Course.objects.filter(level__id__in = level).order_by('id')
    else:
        course = Course.objects.all().order_by('id')

    context ={
        'course': course
    }

    t = render_to_string('ajax/course.html', context )
    return JsonResponse({'data': t})