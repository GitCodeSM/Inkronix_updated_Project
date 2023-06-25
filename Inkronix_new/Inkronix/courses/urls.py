from django.urls import path
from .views import courses, courseDetails, courseList, course_added, filter_data

urlpatterns = [
    path('', courses, name='courses'),
    path('level/filter-data',filter_data,name="filter-data"),
    path('course-list', courseList, name='course-list'),
    path('course-details/<slug:slug>', courseDetails, name='course-details'),
    path('course-added', course_added.as_view(), name='course_added'),
]
