from django.test import TestCase
from django.contrib.auth.models import User
from django.test import TestCase
from .models import *
import datetime as dt

class ProfileTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        
        Profile.objects.create(user=user, location='Kenya', bio='me..me', avatar='image.jpg')
        
        self.location = Profile(location='Kenya')
        
    def test_instance(self):
        self.assertTrue(isinstance(self.location,Profile))
        
class FollowTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        
        Follow.objects.create(follower=user, following=user)
        
        self.follower = Follow(follower=user)
        
    def test_instance(self):
        self.assertTrue(isinstance(self.follower,Follow))
        
class StreamTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        profile = Profile.objects.create(user=user, location='Kenya', bio='me..me', avatar='image.jpg')
        post = Post.objects.create(user=user, image='image.jpg', image_name='Simba', caption='king', date='2012-09-04 06:00:00.000000-08:00', profile=profile, like=10)
        
        Stream.objects.create(following=user, user=user, post=post, date='2012-09-04 06:00:00.000000-08:00')
        
        self.following = Stream(following=user)
        
    def test_instance(self):
        self.assertTrue(isinstance(self.following,Stream))
        
class LikesTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        profile = Profile.objects.create(user=user, location='Kenya', bio='me..me', avatar='image.jpg')
        post = Post.objects.create(user=user, image='image.jpg', image_name='Simba', caption='king', date='2012-09-04 06:00:00.000000-08:00', profile=profile, like=10)
        
        Likes.objects.create(user=user, post=post)
        
        self.user = Likes(user=user)
        
    def test_instance(self):
        self.assertTrue(isinstance(self.user,Likes))
        
class CommentTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        profile = Profile.objects.create(user=user, location='Kenya', bio='me..me', avatar='image.jpg')
        post = Post.objects.create(user=user, image='image.jpg', image_name='Simba', caption='king', date='2012-09-04 06:00:00.000000-08:00', profile=profile, like=10)
        
        Comment.objects.create(comment='its testing!!!', user=user, date='2012-09-04 06:00:00.000000-08:00', post=post)
        self.comment = Comment(comment='its testing!!!')
        
    def test_instance(self):
        self.assertTrue(isinstance(self.comment,Comment))
    
class TestPost(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        profile = Profile.objects.create(user=user, location='Kenya', bio='me..me', avatar='image.jpg')
        self.post_test = Post(user=user, image='image.jpg', image_name='Simba', caption='king', date='2012-09-04 06:00:00.000000-08:00', profile=profile, like=10)

    def test_instance(self):
        self.assertTrue(isinstance(self.post_test, Post))

    def test_save_post(self):
        self.post_test.save_image()
        after = Post.objects.all()
        self.assertTrue(len(after) > 0)

    def test_delete_image(self):
        self.post_test.delete_image()
        images = Post.objects.all()
        self.assertTrue(len(images) == 0)

    def test_update_image(self):
        self.post_test.save_image()
        self.post_test.update_caption(self.post_test.id, 'test work')
        changed_img = Post.objects.filter(caption='test work')
        self.assertTrue(len(changed_img) > 0)

    def tearDown(self):
        Post.objects.all().delete()
      