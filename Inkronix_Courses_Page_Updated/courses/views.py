from django.shortcuts import render
from django.views.generic import CreateView

from django.shortcuts import redirect
from django.core.paginator import Paginator
from .forms import Course_Form
from .models import Course


# Create your views here.
def courses(request):

    courses = Course.objects.all()
    paginator = Paginator(courses, per_page=2)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    context = {
        'courses': courses,
        'page_obj': page_obj
    }

    return render(request, 'courses/courses.html', context)


class course_added(CreateView):
    model = Course()
    form_class = Course_Form
    template_name = 'instructor/instructor-add-course.html'

    def form_valid(self, form):
        course = form.save()
        return redirect('courses')





def courseDetails(request):
    return render(request, 'courses/course-details.html')


def courseList(request):
    return render(request, 'courses/course-list.html')