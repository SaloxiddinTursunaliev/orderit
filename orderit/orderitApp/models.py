import django
from django.utils import timezone

from django.db import models

from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    id = models.BigAutoField(
        db_index=True,
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='id',
    )
    username = models.CharField(
        db_index=True,
        max_length=50,
        unique=True,
        verbose_name='username',
    )
    first_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='first name',
    )
    last_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='last name',
    )
    email = models.EmailField(
        db_index=True,
        max_length=254,
        unique=True,
        verbose_name='email address',
    )
    password = models.CharField(
        db_index=True,
        max_length=128,
        verbose_name='password',
    )
    groups = models.ManyToManyField(
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='user_set',
        related_query_name='user',
        to='auth.Group',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        blank=True, help_text='Specific permissions for this user.',
        related_name='user_set',
        related_query_name='user',
        to='auth.Permission',
        verbose_name='user permissions',
    )
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.',
        verbose_name='staff status',
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
        verbose_name='active',
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text='Designates that this user has all permissions without explicitly assigning them.',
        verbose_name='superuser status',
    )
    last_login = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='last login',
    )
    date_joined = models.DateTimeField(
        default=django.utils.timezone.now,
        verbose_name='date joined',
    )
    # activation_key = models.CharField(
    #     maxlength=40,
    # )
    # key_expires = models.DateTimeField()

    # class Meta:
    #     indexes = [
    #         models.Index(
    #             fields=[
    #                 'id',
    #                 'username',
    #                 'email',
    #                 'password',
    #             ]
    #         ),
    #     ]


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        db_index=True,
        primary_key=True,
        unique=True,
        verbose_name='user id',
        on_delete=models.CASCADE
    )
    is_tutor = models.BooleanField(
        default=False,
        help_text='Designates whether the user is a tutor.',
        verbose_name='tutor status',
    )
    image = models.ImageField(
        upload_to='images/',
        blank=True,
        default="",
    )
    background_image = models.ImageField(
        upload_to='images/',
        blank=True,
        default="",
    )
    # location = models.CharField(max_length=30, blank=True)
    # birthdate = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        # UserProfile2.objects.create(user=instance)
        # UserProfile2.objects.create(user=instance)
    instance.userprofile.save()


class UserProfileSub(models.Model):
    userSub = models.OneToOneField(
        UserProfile,
        db_index=True,
        primary_key=True,
        unique=True,
        verbose_name='user id',
        on_delete=models.CASCADE
    )
    passwordSub = models.CharField(
        db_index=True,
        max_length=128,
        verbose_name='password',
    )


@receiver(post_save, sender=UserProfile)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfileSub.objects.create(userSub=instance)

    instance.userprofilesub.save()


# class UserProfile2(models.Model):
#     user = models.ForeignKey(
#         User,
#         verbose_name='user',
#         on_delete=models.CASCADE,
#     )
#     is_tutor = models.BooleanField(
#         default=False,
#         help_text='Designates whether the user is a tutor.',
#         verbose_name='tutor status',
#     )
#     image = models.ImageField(
#         upload_to='images/',
#         blank=True,
#         default="",
#     )
#     background_image = models.ImageField(
#         upload_to='images/',
#         blank=True,
#         default="",
#     )


def user_directory_path(instance, filename):

    return 'user_{0}/{1}'.format(instance.user, filename)


class TutorApplication(models.Model):
    user = models.IntegerField(
        db_index=True,
        verbose_name='id',
    )
    bio = models.CharField(
        blank=True,
        max_length=256,
        verbose_name='bio',
    )
    video_url = models.CharField(
        blank=True,
        max_length=128,
        verbose_name='video url',
    )
    photo = models.CharField(
        blank=True,
        max_length=128,
        verbose_name='photo',
    )


class Images(models.Model):
    user = models.IntegerField(
        db_index=True,
        verbose_name='id',
    )
    images = models.ImageField(
        upload_to=user_directory_path,  # 'images/',
        db_index=True,
    )

    # upload = models.FileField(upload_to='uploads/%Y/%m/%d/')
