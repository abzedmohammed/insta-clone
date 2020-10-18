from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django_currentuser.db.models import CurrentUserField

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    
    
class Image(models.Model):
    user = CurrentUserField()
    image = CloudinaryField('image')
    name = models.CharField(max_length=120, null=True)
    caption = models.CharField(max_length=120, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, blank=True, related_name = 'image_like')
    comment = models.TextField(null=True)
    
    def __str__(self):
        return self.name
    
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
    
    

