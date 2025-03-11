from django.contrib.auth.models import BaseUserManager


class GrowfiUserManager(BaseUserManager):
    def create_user(self, email, **kwargs):
        """
        Creates and saves a generic User whitin the given email, name,
        and password.
        """
        if not email:
            raise ValueError('Users must have an email')

        user = self.model(
            email=self.normalize_email(email),
            name=kwargs.pop('name', ''),
            **kwargs
        )

        password = kwargs.pop('password', None)
        if password:
            user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        user = self.create_user(*args, **kwargs)
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
