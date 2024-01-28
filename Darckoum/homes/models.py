from django.db import models

class UserManager(models.Manager):
    def get_by_natural_key(self, email):
        return self.get(email=email)
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)
   
class User(models.Model):

    gender_choices = [
        ('M', 'Male'),
        ('F','Female'),
    ]
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField() 
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=1,choices=gender_choices)
    password = models.CharField(max_length=50)
    objects = UserManager()
    @property
    def is_anonymous(self):
        return False
    @property
    def is_authenticated(self):
        return True
    def get_by_natural_key(self, email):
        return self.objects.get(email=email)

    REQUIRED_FIELDS = ['first_name', 'last_name','phone', 'gender']
    USERNAME_FIELD = 'email'

    ACCOUNT_UNIQUE_EMAIL = True
    def __str__(self):
        return self.email
    

class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    typename = models.CharField(max_length=50)

class Transaction(models.Model):
    trans_id = models.AutoField(primary_key=True)
    transname= models.CharField(max_length=50)

class House(models.Model):
    house_id = models.AutoField(primary_key=True)
    title =models.CharField(max_length=255)
    price =models.DecimalField(max_digits=10,decimal_places=2)
    address =models.CharField(max_length=255)
    city =models.CharField(max_length=50)
    description =models.TextField()
    user_id = models.ForeignKey('User',on_delete=models.CASCADE)
    property_type_id = models.ForeignKey('Property',on_delete=models.CASCADE)
    transaction_id=models.ForeignKey('Transaction',on_delete=models.CASCADE)
