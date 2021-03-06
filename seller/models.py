from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.gis.db import models

from barcodelookup.models import Product


NOT_FOUND = "/media/images/product-image-not-found.gif"


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000, default='')
    phone = models.CharField(max_length=14, default='')
    website = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.user.username

    def delete(self, using=None, keep_parents=False):
        user = self.user
        super().delete(using, keep_parents)

        user.delete()


# latitude longitude
class ShopProfile(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=200, default="not available")
    location = models.PointField(null=True, blank=False, srid=4326, verbose_name="Location")
    website = models.CharField(default="not available", max_length=100)
    review_stars = models.IntegerField(default=-1)

    def __str__(self):
        return self.name


class ShopItem(models.Model):

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="")
    price = models.IntegerField(default=-1)
    description = models.TextField(default="not available")
    image_url = models.TextField(default=NOT_FOUND)
    # image_url = models.ImageField(upload_to="images/")
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.title


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
