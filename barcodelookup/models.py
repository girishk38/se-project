from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# image url with image not found
NOT_FOUND = "https://i.ibb.co/dj1qb0D/product-image-not-found.gif"

# Create your models here.
class Product(models.Model):
    """product details for barcode"""

    barcode = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=200, default='')
    description = models.TextField(default="")
    image_url = models.TextField(default=NOT_FOUND)

    def __str__(self):
        return self.title


class Asin(models.Model):
    product = models.OneToOneField(Product, on_delete=models.PROTECT)
    asin = models.CharField(max_length=40)
    link = models.TextField()

    def __str__(self):
        return self.link

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    shop_name = models.CharField(max_length=100, default='')
    shop_address = models.CharField(max_length=1000, default='')
    shop_city = models.CharField(max_length=100, default='')
    website = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=14, default='')

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

    post_save.connect(create_profile, sender=User)
