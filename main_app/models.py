from django.db import models
import re

class UserManager(models.Manager):
    def validate_register(self, postData):
        errors = {}
       
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Your first name must be longer than 1 chars"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Your last name must be longer than 1 chars"
        if len(postData['user_name']) < 2:
            errors['user_name'] = "Your user name must be longer than 1 character"
        user_name_list = User.objects.filter(user_name = postData['user_name'])
        if len(user_name_list) > 0:
            errors['user_name_duplicate'] = "Username already exists within DataBase"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):       
            errors['email'] = "Invalid email address!"
        user_list = User.objects.filter(email = postData['email'])
        if len(user_list) > 0:
            errors['email_duplicate'] = "Email already exists within DB"
        if len(postData['password']) < 9:
            errors['password'] = "Password must be at least 8 chars"
        if postData['password'] != postData['confirm_password']:
            errors['match_password'] = "Your Password and Confirm Password must match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    user_name = models.CharField(max_length=45)
    email = models.CharField(max_length = 45)
    password = models.CharField(max_length = 255)

    # businesses = LIST OF ALL BUSINESSES CREATED BY THIS USER
    # organizations = LIST OF ALL ORGANIZATIONS CREATED BY THIS USER
    objects = UserManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BusinessManager(models.Manager):
    def validate_business(self, postData):
        errors = {}
        if len(postData['business']) < 2:
            errors['business'] = "Your business name must be longer than 1 chars"
        if len(postData['address']) < 2:
            errors['address'] = "Please provide street address"
        if len(postData['city']) < 2:
            errors['city'] = "City name must be longer than 1 chars"
        if len(postData['state']) < 2:
            errors['state'] = "State name must be longer than 1 chars"
        if len(postData['description']) < 2:
            errors['description'] = "Description must be longer than 1 chars"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):       
            errors['email'] = "Invalid email address!"
        return errors

class Business(models.Model):
    business = models.CharField(max_length = 45)
    bus_type = models.CharField(max_length = 45)
    address = models.CharField(max_length=45)
    city = models.CharField(max_length = 45)
    state = models.CharField(max_length = 45)
    description = models.TextField(max_length=45)
    email = models.CharField(max_length = 45)
    telephone = models.CharField(max_length = 45)
    website = models.CharField(max_length = 45)

    user = models.ForeignKey(User, related_name = "businesses", on_delete = models.CASCADE)
    objects = BusinessManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrganizationManager(models.Manager):
    def validate_organization(self, postData):
        errors = {}
        if len(postData['organization']) < 2:
            errors['organization'] = "Your organization name must be longer than 1 chars"
        if len(postData['address']) < 2:
            errors['address'] = "Please provide street address"
        if len(postData['city']) < 2:
            errors['city'] = "City name must be longer than 1 chars"
        if len(postData['state']) < 2:
            errors['state'] = "State name must be longer than 1 chars"
        if len(postData['description']) < 2:
            errors['description'] = "Description must be longer than 1 chars"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):       
            errors['email'] = "Invalid email address!"
        return errors

class Organization(models.Model):
    organization = models.CharField(max_length = 45)
    address = models.CharField(max_length=45)
    city = models.CharField(max_length = 45)
    state = models.CharField(max_length = 45)
    description = models.TextField(max_length=45)
    email = models.CharField(max_length = 45)
    telephone = models.CharField(max_length = 45)
    website = models.CharField(max_length = 45)

    user = models.ForeignKey(User, related_name = "organizations", on_delete = models.CASCADE)
    objects = OrganizationManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)