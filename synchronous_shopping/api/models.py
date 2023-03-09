from django.db import models

# Create your models here.


class SynchronousShopping(models.Model):
    """
    parameters (string): shopping centers, roads, fish types
    shoping_centers (string): Fish types available in each shopping center
    roads (string): Interconnection and travel time between two shopping center
    duration_time (int): Minimum time to purchase all fish types
    """
    id = models.AutoField(primary_key=True)
    parameters = models.CharField(max_length=100)
    shoping_centers = models.CharField(max_length=100)
    roads = models.CharField(max_length=100)
    duration_time = models.IntegerField()
