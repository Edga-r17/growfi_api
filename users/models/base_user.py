from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from _base.models import BaseModel
from users.manager import GrowfiUserManager

# Create your models here.


class GrowfiBaseUser(AbstractBaseUser, PermissionsMixin):
    """
    Enables the use of Django's built-in permissions and groups system;
    useful when we have N different user types inheriting from this class.
    This model is created in the database.
    """

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='growfi_users',  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='growfi_users_permissions',  
        blank=True
    )

    class Meta:
        abstract = True
    def __str__(self):
        return "{}".format(self.pk)


class GrowfiAbstractBaseUser(BaseModel, GrowfiBaseUser):
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150, default='', blank=True)
    email = models.EmailField(max_length=50, unique=True)


    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    email_notification = models.BooleanField(default=False)


    objects = GrowfiUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        # This model should not be created in the database
        abstract = True

    def __str__(self):
        return "{email}".format(email=self.email)

    @property
    def is_staff(self):
        """Returns if the user can access to Django Admin site"""
        return self.is_admin

    @property
    def short_name(self):
        return self.name

    @property
    def full_name(self):
        return "{} {} {}".format(self.id, self.name, self.surname)