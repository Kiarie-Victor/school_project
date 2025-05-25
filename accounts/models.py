from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from Utils.uuidgenerator import UUIDGenerator



class MemberManager(BaseUserManager):
    def create_user(self, firstname, secondname, reg_no, email, faculty, year_of_study, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            firstname=firstname,
            secondname=secondname,
            email=email,
            reg_no=reg_no,
            faculty=faculty,
            year_of_study=year_of_study,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, firstname, secondname, reg_no, email, faculty, year_of_study, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(
            firstname=firstname,
            secondname=secondname,
            email=email,
            reg_no=reg_no,
            faculty=faculty,
            year_of_study=year_of_study,
            password=password,
            **extra_fields
        )


class Member(AbstractBaseUser, PermissionsMixin, UUIDGenerator, models.Model):  # Use PermissionsMixin
    firstname = models.CharField(max_length=100)
    secondname = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    faculty = models.CharField(max_length=100)
    year_of_study = models.IntegerField()
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="member_groups",  # Unique name
        related_query_name="member",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="member_permissions",  # Unique name
        related_query_name="member",
    )

    objects = MemberManager()

    USERNAME_FIELD = 'reg_no'
    REQUIRED_FIELDS = ['firstname', 'secondname',
                       'email', 'faculty', 'year_of_study']

    def __str__(self):
        return self.reg_no



class Otp(UUIDGenerator, models.Model):

    otp_code = models.CharField(max_length=6)
    reg_no = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.otp_code

# accounts/models.py or core/models.py


class Faculty(models.Model):
    FACULTY_CHOICES = [
        ('CIT', 'CIT'),
        ('FST', 'FST'),  # Faculty of Science and Technology
        ('FSS', 'FSS'),  # Faculty of Social Sciences
        ('BUS', 'BUS'),  # Business
        ('ENG', 'ENG'),  # Engineering
        ('MMC', 'MMC'),  # Media & Communication
    ]

    code = models.CharField(
        max_length=10, choices=FACULTY_CHOICES, unique=True)

    def __str__(self):
        return self.get_code_display()  # Show human-readable value
