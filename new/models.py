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


from cloudinary.models import CloudinaryField

class Student(BaseModel):
    full_name = models.CharField(_('full_name'),max_length=100)
    age = models.IntegerField(_('age'),)
    course_name = models.ForeignKey(Course, models.PROTECT)
    email = models.EmailField(_('email'),unique=True)
    image = CloudinaryField(_('image'),'image', blank=True, null=True)
    video = CloudinaryField(_('video'),'video', blank=True, null=True)
    file = CloudinaryField(_('file'),'file', blank=True, null=True)
    registration_date = models.DateTimeField(_('registration_date'),auto_now_add=True)
    is_active = models.BooleanField(_('is_active'),default=True)

