from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django_currentuser.db.models import CurrentUserField
from django.utils import timezone
from django.db.models.signals import post_save

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


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
    image = models.ImageField(upload_to=user_directory_path, verbose_name='Picture', null=True)
    image_name = models.CharField(max_length=120, null=True)
    caption = models.TextField(max_length=1000, verbose_name='Caption', null=True)
    date = models.DateTimeField(auto_now_add=True)
   # profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    comment = models.TextField(null=True)
    
    # class Meta:
    #     ordering = ['-date',]
    
    def __str__(self):
        return self.image_name
    
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
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    
class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def add_post(sender,instance,*args,**kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
            stream.save()
            
post_save.connect(Stream.add_post, sender=Post)
    

