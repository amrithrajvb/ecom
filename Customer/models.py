from django.db import models

# Create your models here.
from datetime import timedelta,date
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, role, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            role=role,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            role="admin",
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    role=models.CharField(max_length=100,default="customer")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class Product(models.Model):
    edd = date.today()
    product_name=models.CharField(max_length=100,unique=True)
    company=models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    stocks = models.IntegerField()
    category = models.CharField(max_length=100, null=True)
    image=models.ImageField(upload_to="images",null=True)
    status=models.CharField(max_length=100,default="Active")
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True)
    date=models.DateField(default=edd,null=True)



class Order(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True)
    price = models.CharField(max_length=100)
    option=(("home delivery","home delivery"),
            ("gpay","gpay"))
    payment_method=models.CharField(max_length=100,choices=option,default="home delivery")
    order_status=models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True,null=True)

class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity=models.IntegerField()