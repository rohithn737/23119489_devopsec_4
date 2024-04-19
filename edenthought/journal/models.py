#************IMPORTANT********************

#For migrations of the models use the below command

#python manage.py makemigrations

#To apply the migrations of the models to the database use the below command --

#python manage.py migrate

#After creating the models and migrate the model we need to update here

from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User

class Thought(models.Model):

    title = models.CharField(max_length=150)
    content = models.CharField(max_length=1000)
    date_now = models.DateTimeField(default=timezone.now) #This is will automatically set created date for our conetnts stored in the database

    #FOREIGN KEY
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null = True) 
    #If the uer is deleted then thought will also be deleted
    #Foreign key will linked to the user module

#This model is to upload a pic to our user model
class Profile(models.Model):

    profile_pic = models.ImageField(null = True, blank = True, default = 'Default.png') # (null = True)It will keep null value in the database
    #(null = True) will allow you to keep blank value in the form, (default = '') will keep a default pic untill u change it

     #FOREIGN KEY
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null = True) 
    #If the uer is deleted then thought will also be deleted
    #Foreign key will linked to the user module

class FitnessTrack(models.Model):

    week = models.CharField(max_length=150)
    weight = models.IntegerField(null = True)
    fat = models.IntegerField(null = True)
    progress = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)
    diet = models.CharField(max_length=1000)
    water = models.CharField(max_length=1000)
    image = models.ImageField(null = True)

    #FOREIGN KEY
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null = True) 
    #If the uer is deleted then thought will also be deleted
    #Foreign key will linked to the user module
class BMIcal(models.Model):

    weight = models.IntegerField(null = True)
    height = models.IntegerField(null = True)
    image = models.ImageField(null = True)
    
    #FOREIGN KEY
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null = True)










