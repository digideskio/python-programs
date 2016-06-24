from django.db import models

# Create your models here.


class States(models.Model):
    uf = models.CharField(max_length=2, primary_key=True, unique=True)
    state = models.CharField(max_length=200)

    def __str__(self):
        return self.uf
