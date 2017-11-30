from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField(max_length=100)
    age = models.IntegerField(default=0)
    profile_image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)


class FeedBack(models.Model):
    topic = models.CharField(max_length=500)
    feed = models.CharField(max_length=10000)

    def __str__(self):
        return self.topic


class Post(models.Model):
    post = models.CharField(max_length=10000)
    date_posted = models.DateField(auto_now=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.post


class MyComments(models.Model):
    user = models.ForeignKey(User)
    post_associated = models.ForeignKey(Post, null=True)
    comment = models.CharField(max_length=500)

    def __str__(self):
        return self.comment


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)




