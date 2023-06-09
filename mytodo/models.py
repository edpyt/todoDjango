from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# Create your models here.
def get_photo_user(instance, filename):
    return f'{instance.username}/{filename}'


class MyUser(AbstractUser):
    photo = models.ImageField(_('Photo'),
                              upload_to=get_photo_user,
                              blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_profile')


class ToDoModel(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    content = models.TextField(_('Content'), blank=True)
    date_created = models.DateTimeField(_('Date created'), auto_now_add=True)
    date_ending = models.DateTimeField(_('Expiration Date'))

    user = models.ForeignKey('MyUser', on_delete=models.CASCADE)

    is_done = models.BooleanField(_('Is done?'), default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('is_done', 'date_ending')