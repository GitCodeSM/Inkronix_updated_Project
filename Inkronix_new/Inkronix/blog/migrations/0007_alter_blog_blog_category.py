# Generated by Django 4.2.1 on 2023-06-11 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_blog_blog_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.category'),
        ),
    ]