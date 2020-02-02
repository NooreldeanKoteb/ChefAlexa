from django.db import models


# Create your models here.
class user(models.Model):

    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)


    allergies = models.CharField(max_length=350, blank=True)

    QuicknEazy = models.BooleanField(default=False)
    SlowCooker = models.BooleanField(default=False)
    BBQnGrill = models.BooleanField(default=False)

    American = models.BooleanField(default=False)
    Southern = models.BooleanField(default=False)
    Asian = models.BooleanField(default=False)
    Thai = models.BooleanField(default=False)
    Chinese = models.BooleanField(default=False)
    Indian = models.BooleanField(default=False)
    Mexican = models.BooleanField(default=False)
    Italian = models.BooleanField(default=False)
    European = models.BooleanField(default=False)


    Kosher = models.BooleanField(default=False)
    Vegan = models.BooleanField(default=False)
    Vegetarian = models.BooleanField(default=False)
    Diabetic = models.BooleanField(default=False)
    Gluten_Free = models.BooleanField(default=False)
    Lactose_Intolerant = models.BooleanField(default=False)

    def __str__(self):
        return self.user_name
