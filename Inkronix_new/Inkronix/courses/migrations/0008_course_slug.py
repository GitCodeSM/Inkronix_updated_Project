# Generated by Django 4.2.1 on 2023-06-21 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_catagories_remove_course_category_course_catagory'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=500, null=True),
        ),
    ]
