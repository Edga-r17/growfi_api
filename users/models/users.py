from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from _base.files import upload_to_kwargs, upload_to_generic
from .base_user import GrowfiAbstractBaseUser
from _base.models import BaseModel

import uuid


class GrowfiUser(GrowfiAbstractBaseUser):
  
    phone = models.CharField(max_length=150, blank=True, null=True)
    photo = models.ImageField(upload_to=upload_to_kwargs(upload_to_generic, subfolder="user_photo"), null=True, blank=True)
    initials = models.CharField(max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if self.password and not self.password.startswith('pbkdf2_sha256$') :
            password_length = len(self.password)
            self.password_length = password_length
            self.set_password(self.password)
        
        if is_new and self.name:
            name_parts = self.name.split()  
            if len(name_parts) >= 2:
                self.initials = name_parts[0][0] + name_parts[1][0] 
            else:
                self.initials = name_parts[0][:2]  
            self.initials = self.initials.upper() 
        super(GrowfiUser, self).save(*args, **kwargs)
        
        if is_new:
            GrowfiUserToken.objects.create(growfi_user=self)

class GrowfiUserToken(BaseModel):
    id = models.BigAutoField(primary_key=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    growfi_user = models.OneToOneField('users.GrowfiUser', related_name='growfi_auth_token', on_delete=models.deletion.CASCADE)

    def save(self, *args, **kwargs):
        

        if not self.key:
            self.key = self.generate_key()


        return super(GrowfiUserToken, self).save(*args, **kwargs)


    def reset_key(self):
        self.key = self.generate_key()
        self.save()
        return self.key

    def generate_key(self):
        return uuid.uuid4()

    def __str__(self):
        return '{}: {}'.format(self.jp_user.pk, self.key)

    class Meta:
        verbose_name = '2. User Token'
        ordering = ['-created']