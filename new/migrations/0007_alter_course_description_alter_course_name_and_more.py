# Generated by Django 5.2 on 2025-06-01 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new', '0006_student_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=100, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='course',
            name='start_date',
            field=models.DateField(verbose_name='start_date'),
        ),
        migrations.AlterField(
            model_name='student',
            name='age',
            field=models.IntegerField(verbose_name='age'),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='student',
            name='full_name',
            field=models.CharField(max_length=100, verbose_name='full_name'),
        ),
        migrations.AlterField(
            model_name='student',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is_active'),
        ),
        migrations.AlterField(
            model_name='student',
            name='registration_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='registration_date'),
        ),
    ]
