from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Company(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    color = models.CharField(max_length=25, blank=True, null=True)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields['company'] = Company.objects.get(pk=extra_fields['company'])
        print(extra_fields)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'company']


class Form(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.TextField(max_length=30, primary_key=True)

class Question(models.Model):
    TEXT = 'text'
    MCQ = 'mcq'
    QUESTION_TYPES = [
        (TEXT, 'Text'),
        (MCQ, 'MCQ'),
    ]
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=QUESTION_TYPES, default=TEXT)
    text = models.CharField(max_length=255)
    is_required = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

class QuestionChoices(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text_answer = models.TextField(blank=True, null=True)
    mcq_answer = models.CharField(max_length=255, blank=True, null=True)
    file_answer = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)

class Reply(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

