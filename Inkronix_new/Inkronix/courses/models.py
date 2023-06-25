from django.db import models
from accounts.models import Instructor, Student
from django.utils.text import slugify
from django.db.models.signals import pre_save

# Create your models here.
class Catagories(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    def get_all_catagory(self):
        return Catagories.objects.all().order_by('id')
    
class Level(models.Model):
    name = models.CharField(max_length=100)

    def  __str__(self):
        return self.name

class Course(models.Model):
    author          = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    student         = models.ManyToManyField(Student)
    title           = models.CharField(max_length=255)
    image           = models.ImageField(upload_to='images/courses')
    
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    off_price = models.IntegerField(default=0)

    language        = models.CharField(max_length=50)

    # COURSE_CATEGORY = (
    #     ("app-web-development", "App & Web Development"),
    #     ("digital-marketing", "Digital Marketing"),
    #     ("graphics-designing", "Graphics Designing"),
    #     ("python-programming", "Python Programming"),
    #     ("artificial-intelligence", "Artificial Intelligence"),
    #     ("government-exams", "Government Exams"),
    # )

    # category        = models.CharField(max_length=100)
    catagory        = models.ForeignKey(Catagories, on_delete=models.CASCADE, null=True)
    level           = models.ForeignKey(Level, on_delete=models.CASCADE,null=True)

    short_intro     = models.CharField(max_length=50)
    description     = models.TextField()
    slug            = models.SlugField(default='', max_length=500, null =True, blank=True)
    Certificate     = models.CharField(null=True,max_length=100)

    created_on      = models.DateTimeField(auto_now_add=True)
    updated_on      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("course-details", kwargs={'slug': self.slug})
    

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Course)

class Requirements(models.Model):
    courses = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self):
        return self.points
    
class Lesson(models.Model):
    courses = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name + " - " + self.courses.title
    
class Video(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="images/courses",null=True)
    courses = models.ForeignKey(Course,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    time_duration = models.FloatField(null=True)
    preview = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title
    
# class Description(models.Model):
#     des = models.ForeignKey(Course, on_delete=models.CASCADE)
#     points = models.CharField(max_length=500)

#     def __str__(self):
#         return self.points
    