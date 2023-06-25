from django.urls import path
from blog import views
from blog.views import BlogView, BlogAV, BlogDetailAV, WriterAV, BlogSearchView
# from django.conf.urls import url

urlpatterns = [
    path('', views.bloghome, name='blog'),
    path('blog-form', views.BlogFormView, name='blog-form'),
    path('<int:pk>', BlogView.as_view(), name='blog-page'),
    path('blog-view', BlogAV.as_view(), name='blog-view'),
    path('blog-view/<int:pk>', BlogDetailAV.as_view(), name='blog-detail'),
    path('writer', WriterAV.as_view(), name='writer'),
    path('search-view/', BlogSearchView.as_view(), name="search-view")
]
