from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class UserProfile(models.Model):
    name = models.CharField(max_length=264)
    address = models.CharField(max_length=528)
    pincode = models.BigIntegerField()
    city = models.CharField(max_length=264)
    # country = models.CharField(max_length=264)
    # age = models.IntegerField()
    email = models.EmailField()
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Painting(models.Model):
    TempImg = path_join('media', 'anaya.jpg')
    title = models.CharField(max_length=264)
    artist = models.CharField(max_length=264)
    price = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()
    sold = models.BooleanField(default=False)
    description = models.TextField()
    image = models.ImageField(upload_to='media/',default=temp_img)

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    paintings =  models.ManyToManyField(Painting,related_name='c_paintings')

    def __str__(self):
        return (self.user.userprofile.name + "'s cart")

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    bill = models.BigIntegerField(default=0)
    uid = models.CharField(max_length=264)
    paintings =  models.ManyToManyField(Painting,related_name='o_paintings')
    successful = models.BooleanField(default=False)

    def __str__(self):
        return (self.user.userprofile.name + "'s cart")

class Member(models.Model):
    name = models.CharField(max_length=264)
    post = models.CharField(max_length=264)
    image = models.ImageField(image = models.ImageField(upload_to='media/'))

    def __str__(self):
        return self.name
