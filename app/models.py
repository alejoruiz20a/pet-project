from django.db import models

class User(models.Model):
    user = models.CharField(primary_key=True,max_length=100)
    password = models.CharField(max_length=100)
    money = models.IntegerField()

class Pet(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    health = models.IntegerField()
    lasthealth = models.DateTimeField()
    happiness = models.IntegerField()
    lasthapiness = models.DateTimeField()
    hunger = models.IntegerField()
    lasthunger = models.DateTimeField()
    energy = models.IntegerField()
    lastenergy = models.DateTimeField()
    shittiness = models.IntegerField()
    lastshit = models.DateTimeField()
    age = models.IntegerField()
    money = models.IntegerField()
    lastjob = models.DateTimeField()
    birthday = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()
    id_user = models.ForeignKey(User,on_delete=models.CASCADE)