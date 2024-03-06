from django.db import models

class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    dis = models.IntegerField()
    # ch = models.IntegerField()

    class Meta:
        db_table = 'users'


class Stok(models.Model):
    article = models.CharField(max_length=50, primary_key=True)
    nam = models.CharField(max_length=50)
    oem = models.CharField(max_length=50)
    price = models.CharField(max_length=10)
    quantity = models.CharField(max_length=10)
    brand = models.CharField(max_length=50)

    class Meta:
        db_table = 'stok'


class Oem(models.Model):
    art = models.CharField(max_length=50, primary_key=True)
    oem = models.CharField(max_length=50)

    class Meta:
        db_table = 'oem'