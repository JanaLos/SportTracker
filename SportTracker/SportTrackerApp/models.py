from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from tkinter import *
from PIL import Image

class Activity(models.Model):
    objects = None
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    km_count = models.FloatField(max_length=4)
    date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "activity"
        verbose_name_plural = "activities"
        ordering = ['-id', ]

    def __str__(self):
        return self.name

class Post(models.Model):
    objects = None
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='SportTrackerApp/static/img/default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def create_profile(sender, instance, created, *args, **kwargs):
        if not created:  # if user already exits then ignore
            return
        Profile.objects.create(user=instance)

    post_save.connect(create_profile, sender=User)

    def save(self, **kwargs):
        super(Profile, self).save(**kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
