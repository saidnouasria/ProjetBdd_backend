from django.db import models

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
    

class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    typename = models.CharField(max_length=50)

class Transaction(models.Model):
    trans_id = models.AutoField(primary_key=True)
    transname= models.CharField(max_length=50)

class house(models.Model):
    house_id = models.AutoField(primary_key=True)
    title =models.CharField(max_length=255)
    price =models.DecimalField(max_digits=10,decimal_places=2)
    address =models.CharField(max_length=255)
    city =models.CharField(max_length=50)
    description =models.TextField()
    user_id = models.ForeignKey('User',on_delete=models.CASCADE)
    property_type_id = models.ForeignKey('Property',on_delete=models.CASCADE)
    transaction_id=models.ForeignKey('Transaction',on_delete=models.CASCADE)