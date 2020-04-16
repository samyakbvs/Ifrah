import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Ifrah.settings')

import django
django.setup()

import random
from Gallery.models import Painting
from faker import Faker

fake = Faker()

categories = ['Elegant','Minimal','Luxury','Dark','Professional']
mediums = ['water','acrylic','soft pastel','oil']

for i in range(20):
    painting = Painting(category=categories[random.randint(0,4)],medium=mediums[random.randint(0,3)],artist=fake.name(),price=random.randint(0,100),height=random.randint(0,100),width=random.randint(0,100) )
    painting.save()

# class Post(models.Model):
#     Name = models.CharField(max_length = 264)
#     Init_time = models.DateTimeField()
#     Description = models.TextField()
#     Author = models.CharField(max_length = 264)
#     Image = models.FileField(blank=True)
#     Video = models.FileField(blank=True)
#     Doc = models.FileField(blank=True)
#
#     def __str__(self):
#         return self.Name

# class Painting(models.Model):
#     category = models.CharField(max_length=264)
#     artist = models.CharField(max_length=264)
#     price = models.IntegerField()
#     height = models.IntegerField()
#     width = models.IntegerField()
