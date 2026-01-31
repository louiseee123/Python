from django.db import models

# Create your models here.

class Student(models.Model):
    s_id=models.IntegerField()
    s_name=models.CharField(max_length=67)
    s_dept=models.CharField(max_length=67)