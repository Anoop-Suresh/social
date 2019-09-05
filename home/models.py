from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.conf import settings
# Create your models here.


#
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     Name= models.CharField(max_length=250,blank=True)
#     Bio= models.TextField(max_length=500, blank=True)
#     Age=models.IntegerField(blank=True)
#     Phone = models.IntegerField(default=0,null=True)
#     Image = models.FileField(blank=True, upload_to='media/images/')
#
#     #
#     # @receiver(post_save, sender=User)
#     # def create_user_profile(sender, instance, created, **kwargs):
#     #     if created:
#     #         Profile.objects.create(user=instance)
#     #
#     # @receiver(post_save, sender=User)
#     # def save_user_profile(sender, instance, **kwargs):
#     #     instance.profile.save()
#
#     def __str__(self):
#         return self.Name


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class NewsFeedItem(models.Model):
    """Profile status update."""

    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    cover = models.FileField(blank=True, upload_to='media/images/')
    created_on = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation(Like)


    def __str__(self):
        """Return the model as a string."""

        return self.status_text

    @property
    def total_likes(self):
        return self.likes.count()

User = get_user_model()


