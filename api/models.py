from django.db import models

class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    dis = models.IntegerField()
    ch = models.IntegerField()

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

        
class Card(models.Model):
    article = models.CharField(max_length=50, primary_key=True)
    nam = models.TextField()
    quantity = models.CharField(max_length=10)
    dis0 = models.CharField(max_length=10)
    dis1 = models.CharField(max_length=10)
    dis2 = models.CharField(max_length=10)
    dis3 = models.CharField(max_length=10)
    dis4 = models.CharField(max_length=10)
    dis5 = models.CharField(max_length=10)
    dis6 = models.CharField(max_length=10)
    dis7 = models.CharField(max_length=10)
    dis8 = models.CharField(max_length=10)
    dis9 = models.CharField(max_length=10)
    dis10 = models.CharField(max_length=10)
    dis11 = models.CharField(max_length=10)
    dis12 = models.CharField(max_length=10)
    dis13 = models.CharField(max_length=10)
    dis14 = models.CharField(max_length=10)
    dis15 = models.CharField(max_length=10)
    dis16 = models.CharField(max_length=10)
    new_item = models.CharField(max_length=10)
    oem = models.CharField(max_length=10)
    brand = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'card'