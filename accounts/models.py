from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.mail import send_mail  
from django.dispatch import receiver

def upload_Music(instance, filename):
    return 'prfile/{filename}'.format(filename=filename)

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email,  password, **othersField):
        othersField.setdefault('is_superuser', True)
        othersField.setdefault('is_staff', True)
        othersField.setdefault('is_active', True)

        if othersField.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')
        
        if othersField.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')
        
        return self.create_user(email,  password,  **othersField)

    def create_user(self, email, password, **othersField):
        if not email:
            raise ValueError(_('you must provide an email address'))
        email =  self.normalize_email(email)
        user = self.model(email=email, **othersField)
        user.set_password(password)
        user.save()
        return user

        

# Custom authentication model
class NewUsers(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), max_length=254, unique=True)
    first_name = models.CharField(_("First_name"), max_length=50, default='')
    profilePic = models.ImageField(upload_to=upload_Music, default='')
    last_name = models.CharField(_("Last_name"), max_length=50, default='default.jpg')
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)