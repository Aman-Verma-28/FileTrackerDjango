"""hello"""
import uuid
from django.db import models

# Create your models here.

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class FileModel(models.Model):
    """Function printing python version."""
    fileid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    tags = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    qrimage = models.ImageField()

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filename


class FileHistoryModel(models.Model):
    """Function printing python version."""
    file_state = models.ForeignKey(
        FileModel, related_name="prev_file", on_delete=models.CASCADE
    )
    owners = models.JSONField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    # def __str__(self):

    #     return self.file_state


class UserManager(BaseUserManager):
    """Function printing python version."""
    def create_user(
        self, email, fname, lname, department, password=None, password2=None
    ):
        """
        Creates and saves a User with the given email,fname, lname, department, password
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            fname=fname,
            lname=lname,
            department=department,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fname, lname, department, password=None):
        """
        Creates and saves a superuser with the given email,fname, lname, department, password
        """
        user = self.create_user(
            email,
            password=password,
            fname=fname,
            lname=lname,
            department=department,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """Function printing python version."""

    email = models.EmailField(
        verbose_name="email",
        max_length=255,
        unique=True,
    )
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        FileModel, related_name="file_owner", on_delete=models.CASCADE, null=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fname", "lname", "department"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


from django.db import models

# Create your models here.

class Contact(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    email=models.CharField(max_length=100)
    content=models.TextField()
    timeStamp=models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return "Message from "+self.name+ " - "+ self.email