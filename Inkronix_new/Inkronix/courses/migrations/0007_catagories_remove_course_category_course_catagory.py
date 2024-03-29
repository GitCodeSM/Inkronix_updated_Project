# Generated by Django 4.2.1 on 2023-06-21 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_discount_course_off_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catagories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='category',
        ),
        migrations.AddField(
            model_name='course',
            name='catagory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.catagories'),
        ),
    ]
