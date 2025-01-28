import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class AddressModel(models.Model):
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    postalCode = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    class Meta:
        managed = True
        db_table = 'address'

# Create your models here.
class CustomUserModel(AbstractUser):
    phone = models.CharField(max_length=250)
    referral_code = models.CharField(max_length=200, null=True, blank=True, default='No Referals')
    address =  models.ForeignKey(AddressModel, null=True, on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = 'custom_user'

class TokenModel(models.Model):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=250, )
    expired = models.BooleanField(default=False)
    use_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:

        managed = True
        db_table='token_table'
    pass