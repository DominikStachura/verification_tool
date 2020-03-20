from django.db import models


class ItemQuerySet(models.query.QuerySet): #to sa metody wywolywane na querysecie, np. na item.objects.all()
    def get_by_url(self, url):
        return self.filter(url_image=url).first()  #get_queryset() to tak jak Product.objects


class ItemManager(models.Manager): # to jest model menager dziala na item.objects
    def get_queryset(self): # przeciazam get queryset dla Item
        return ItemQuerySet(self.model, using=self._db)

    def get_by_url(self, url):
        return self.get_queryset().get_by_url(url=url)  #tutaj tez ustalam ta metode zeby mozna bylo wywolywac i na item.objects.all().get_by_url() i na item.objects.get_by_url()


# Create your models here.
class Item(models.Model):
    id = models.IntegerField(default=9999999999, primary_key=True)
    file_name = models.TextField(default='')
    item_type = models.TextField(default='')
    item_shape = models.TextField(default='')
    item_cat = models.TextField(default='')
    item_value = models.IntegerField(default=0)
    x_1 = models.IntegerField(default=0)
    y_1 = models.IntegerField(default=0)
    x_2 = models.IntegerField(default=0)
    y_2 = models.IntegerField(default=0)
    frame = models.TextField(default='')
    cropped_frame = models.TextField(default='')
    region = models.TextField(default='')
    url_image = models.URLField(default='')
    comments = models.TextField(default='')

    objects = ItemManager()

    class Meta:
        ordering = ['id']

class ImageItem(models.Model):
    id = models.IntegerField(default=9999999999, primary_key=True)
    image_name = models.TextField(default='')

    class Meta:
        ordering = ['id']

class SignType(models.Model):
    sign_type = models.TextField(default='')

class SignShape(models.Model):
    sign_shape = models.TextField(default='')

class SignIcon(models.Model):
    sign_icon = models.TextField(default='')