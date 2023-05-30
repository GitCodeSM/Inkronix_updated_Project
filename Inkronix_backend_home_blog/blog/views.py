from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.http import request
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User, auth
from django.contrib import messages
# from django.views import View
from django.views.generic.base import View
from django.views.generic import ListView
# from django.views.generic.edit import CreateView, UpdateView
from blog.models import Blog, Writer, Comment, Category
from blog.serializers import BlogSerializer, WriterSerializer
from blog.forms import CommentForm, BlogForm#, ReactionForm
# from accounts.models import Users
# Create your views here.

def bloghome(request):

    if request.method == 'GET':
        blogs = Blog.objects.all()
        # writer_id = request.session.get('user_id')
        # user = Users.objects.get(writer_id)

        # if writer_id:
        #     for 
        #     if writer_name = user.name
        categories = Category.objects.all()
        category_id = request.GET.get('category')

        if category_id:
            blogs = Blog.get_blogs_by_category_id(category_id=category_id)
        else:
            blogs = Blog.objects.all()

    return render(request, 'Blogs/blog.html', {'blogs':blogs, 'categories':categories})

# class BlogFormView(View):

#     def get(self, request):

#         blog_form = BlogForm()
#         return render(request, 'Blogs/blog-form.html', {'blog_form':blog_form})

#     def post(self, request):
#         return BlogFormView.if_post(request)

#     def if_post(request):
#         blog_form = BlogFormView(request.POST)#, request.FILES

#         if blog_form.is_valid():
#             blog_form.save()
#             messages.success(request, ('Your blog was successfully added!'))
#         else:
#             messages.error(request, 'Error saving form')

#         # return bloghome(request)
#         return render('Blogs/blog.html')

# def BlogFormView(request):
#     # if request.method == 'GET':
#     blog_form = BlogForm()
#     # return render(request, 'Blogs/blog-form.html', {'blog_form':blog_form})
#     # else:
#     if request.method == "POST":
#         blog_form = BlogFormView(request.POST)#, request.FILES
#         if blog_form.is_valid():
#             blog_form.save()
#             messages.success(request, ('Your blog was successfully added!'))
#         else:
#             messages.error(request, 'Error saving form')

#         # return bloghome(request)
#     return render(request, 'Blogs/blog-form.html', {'blog_form':blog_form})

def BlogFormView(request):

    blog_form = BlogForm()
    # books = Book.objects.all()

    if request.method == "POST":
        blog_form = BlogForm(request.POST, request.FILES)

        if blog_form.is_valid():
            blog_form.save()
            # book_form.save(commit=True) # option
            messages.success(request, ('Your blog was successfully added!'))
        else:
            messages.error(request, 'Error saving form')
            
        return redirect('Blogs/blog.html')
        
    return render(request=request, template_name="Blogs/blog-form.html", context={'blog_form':blog_form})

# class BlogCreate(CreateView):
#     model = Blog
#     form_class = BlogForm
#     template_name = 'Blogs/blog-form.html'

class BlogListView(ListView):
    paginate_by = 2
    model = Blog

class BlogView(View):

    def get(self,request,pk):

        blog = Blog.objects.get(id=pk)
        comment_form = CommentForm()
        # comments = Comment.objects.all()
        comments = Comment.objects.filter(blog_id = blog.id)
        categories = Category.objects.all()
        # category_id = request.GET.get('category')

        # if category_id:
        #     blogs = Blog.get_blogs_by_category_id(category_id=category_id)
        # else:
        #     blogs = Blog.objects.all()

        return render(request,'Blogs/blog-view.html', {'blog':blog, 'comment_form':comment_form, 'comments':comments, 'categories':categories})

    def post(self,request,pk):
        # blog_id = request.POST['blog_id']
        comment_form = CommentForm(request.POST, pk)
        # if comment_form.fields.get('your_comment') == None:
        comment_form.save()
        messages.success(request, ('Your comment was added successfully!'))
        return render(request, 'Blogs/blog-view.html', {'comment_form':comment_form})


# def create_superuser(self, email, password):
#         """
#         Create and return a `User` with superuser (admin) permissions.
#         """
#         if password is None:
#             raise TypeError('Superusers must have a password.')

#         user = self.create_user(email, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()

#         return user


class BlogAV(APIView):

    def get(self, request):

        blogs = Blog.objects.all()
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

    def delete(self, request, pk): #request is important
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

