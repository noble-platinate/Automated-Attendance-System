from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

class user_data(models.Model):
    rno = models.IntegerField()
    fname = models.CharField(max_length=64)
    lname = models.CharField(max_length=64)
    present = models.BooleanField()
    aruco_id = models.IntegerField(primary_key=True)
