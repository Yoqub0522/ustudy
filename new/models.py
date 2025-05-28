from django.db import models

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
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()

    def __str__(self):
        return self.name


from cloudinary.models import CloudinaryField

class Student(BaseModel):
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    course_name = models.ForeignKey(Course, models.PROTECT)
    email = models.EmailField(unique=True)
    image = CloudinaryField('image', blank=True, null=True)
    video = CloudinaryField('video', blank=True, null=True)
    file = CloudinaryField('file', blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

