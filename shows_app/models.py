from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['first_name']) < 3:
            errors['first_name'] = 'First Name must be at least 2 characters'
        if len(postData['last_name']) < 3:
            errors['last_name'] = 'Last Name must be at least 2 characters'
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        email_check=User.objects.filter(email=postData['email'])
        if email_check:
            errors['email'] = ("Email address already taken!")

        if len(postData['password']) < 8 :
            errors['password'] = 'Password must be at least 8 characters'
        if postData['password'] != postData['confirm_password']:
            errors['password'] = 'Passwords do not match'
        return errors
    
    def validate_login(request):
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.pw_hash.encode()):
            print("password match")
        else:
            print("failed password")

    def register(self, postData):
        pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()
        return User.objects.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = pw,
        )

    def authenticate(self, email, password):
        users = User.objects.filter(email=email)
        if users:
            user=users[0]
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return True
            else:
                return False
        return False

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class ShowManager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        if len(postData['title']) < 3:
            errors['title'] = 'Title should be at least 3 characters'
        if len(postData['network']) < 3:
            errors['network'] = 'Network should be at least 3 characters'
        if len(postData['description']) < 3:
            errors['description'] = 'Description should be at least 3 characters'
        if len(postData['release_date']) < 3:
            errors['release'] = 'Release Date must be included'
        return errors

class Show(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    release_date = models.DateField(auto_now=False)
    description = models.TextField()
    owner = models.ForeignKey(User, related_name = 'shows', on_delete=models.CASCADE)
    made = models.ManyToManyField(User, related_name = 'made_movies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()