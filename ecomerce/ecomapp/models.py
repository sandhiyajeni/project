from django.db import models
from django.contrib.auth.models import User
class Products(models.Model):
    CATEGORIES=((1,"cloth"),(2,"shoes"),(3,"mobile"))
    name=models.CharField(max_length=20)
    price=models.FloatField()
    cat=models.IntegerField(choices=CATEGORIES)
    desc=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    pimage=models.ImageField(upload_to='media/')
    def __str__(self) :
        return self.name
class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Products,on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
class Order(models.Model):
    oid=models.IntegerField()
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Products,on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)