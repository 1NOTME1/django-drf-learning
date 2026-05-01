from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    is_active = models.BooleanField(default=True)
    department = models.ForeignKey(
        Department, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name
