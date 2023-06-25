from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.http import HttpRequest, HttpResponse, request
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.generic.base import View
from django.views.generic import ListView
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from blog.models import Blog, Writer, Comment, Category
from blog.serializers import BlogSerializer, WriterSerializer
from blog.forms import CommentForm, BlogForm

def bloghome(request):

    if request.method == 'GET':
        # blogs = Blog.objects.all()
        categories = Category.objects.all()
        category_id = request.GET.get('category')
        
        if category_id:
            blogs = Blog.get_blogs_by_category_id(category_id=category_id).order_by('-blog_date_time')
        else:
            blogs = Blog.objects.all().order_by('-blog_date_time')

        paginator = Paginator(blogs, per_page=2)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        try:
            blogs = paginator.page(page_number)
        except PageNotAnInteger:
            page_number = 1
            blogs = paginator.page(page_number)
        except EmptyPage:
            page_number = paginator.num_pages
            blogs = paginator.page(page_number)

    # return render(request, 'Blogs/blog.html', {'page_obj':page_obj, 'categories':categories})
    return render(request, 'Blogs/blog.html', {'blogs':blogs, 'page_obj':page_obj, 'categories':categories})

# Blog-form-view
def BlogFormView(request):

    blog_form = BlogForm()

    if request.method == "POST":
        blog_form = BlogForm(request.POST, request.FILES)

        if blog_form.is_valid():
            blog_form.save()

            messages.success(request, ('Your blog was successfully added!'))
        else:
            messages.error(request, 'Error saving form')

        return redirect('blog')

    return render(request=request, template_name="Blogs/blog-form.html", context={'blog_form':blog_form})

class BlogView(View):

    def get(self,request,pk):

        blog = Blog.objects.get(id=pk)
        comment_form = CommentForm()
        comments = Comment.objects.filter(blog = blog.id).order_by('-created_on')
        categories = Category.objects.all()
        category_id = request.GET.get('category')

        if category_id:
            blogs = Blog.get_blogs_by_category_id(category_id=category_id).order_by('-blog_date_time')
            return render(request, 'Blogs/blog.html', {'blogs':blogs, 'categories':categories})
        else:
            return render(request,'Blogs/blog-view.html', {'blog':blog, 'comment_form':comment_form, 'comments':comments, 'categories':categories})

    def post(self,request,pk):

        blog = Blog.objects.get(id=pk)
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid:
            blog_id = blog.id
            new_comment = comment_form.save(commit=False)
            new_comment.blog = blog_id
            new_comment.save()

        # messages.success(request, ('Your comment was added successfully!'))
        return redirect('blog')
        # return render(request, 'Blogs/blog-view.html', {'comment_form':comment_form})


class BlogSearchView(ListView):
    model = Blog
    template_name = 'Blogs/search-view.html'
    # context_object_name = 'blogs'
    paginate_by = 2

    def get_context_data(self, **kwargs):

        context = super(BlogSearchView,self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', "")
        query = self.request.GET.get('query')

        categories = Category.objects.all()
        category_id = self.request.GET.get('category_id')
        
        if query:
            if category_id:
                queryset = Blog.objects.filter(
                    Q(blog_title__icontains=query) |
                    Q(blog_text__icontains=query)
                ).distinct().order_by('-blog_date_time').filter(blog_category_id=category_id)
            else:
                queryset = Blog.objects.filter(
                    Q(blog_title__icontains=query) |
                    Q(blog_text__icontains=query)
                ).distinct().order_by('-blog_date_time')
            
            paginator = Paginator(queryset, self.paginate_by)
            page_number = self.request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            try:
                blogs = paginator.page(page_number)
            except PageNotAnInteger:
                page_number = 1
                blogs = paginator.page(page_number)
            except EmptyPage:
                page_number = paginator.num_pages
                blogs = paginator.page(page_number)

            context['blogs'] = blogs
            context['page_obj'] = page_obj
            context['categories'] = categories
            return context


class BlogAV(APIView):

    def get(self, request):

        blogs = Blog.objects.all().order_by('-blog_date_time')
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogDetailAV(APIView):

    def get(self, request, pk):
        try:
            blog = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response({'error':'Not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        serializer = Blog(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        blog.delete()
        # return Response({'message':'this data is deleted'})
        return Response(status=status.HTTP_204_NO_CONTENT)


class WriterAV(APIView):

    def get(self, request):
        writer = Writer.objects.all()
        serializer = WriterSerializer(writer, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = WriterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
