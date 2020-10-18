from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django_currentuser.db.models import CurrentUserField
from django.utils import timezone

class Profile(models.Model):
    bio = models.TextField(max_length=120, null=True)
    avatar = CloudinaryField('image')
    
    def __str__(self):
        return self.bio
    
    def save_image(self):
        self.save()
        
    def delete_image(self):
        self.delete()
    
    @classmethod
    def update(cls, id, value):
        cls.objects.filter(id=id).update(avatar=value)
    
    
class Post(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    image_name = models.CharField(max_length=120, null=True)
    description = models.TextField(null=True)
    caption = models.TextField(max_length=120, null=True)
    date = models.DateTimeField(auto_now_add=True)
   # profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    comment = models.TextField(null=True)
    
    # class Meta:
    #     ordering = ['-date',]
    
    def __str__(self):
        return self.caption
    
    def save_image(self):
        self.save()
        
    @classmethod
    def search_by_name(cls,search_term):
        prof = cls.objects.filter(name__name__icontains=search_term)
        return prof
        
    def delete_image(self):
        self.delete()
    
    @classmethod
    def update_caption(cls, id, value):
        cls.objects.filter(id=id).update(caption=value)
    
    

