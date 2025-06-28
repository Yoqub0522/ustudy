from django.db import models
from django.utils.translation import gettext_lazy as _

class DeleteModel(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


    objects = DeleteModel()


    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save(*args, **kwargs)

class Course(BaseModel):
    name = models.CharField(_('name'),max_length=100)
    description = models.TextField(_('description'),)
    start_date = models.DateField(_('start_date'),)

    def __str__(self):
        return self.name




class Student(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    course_name = models.ForeignKey('Course', models.PROTECT)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

