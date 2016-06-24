from django.db import models

# Create your models here.


class Comentario(models.Model):
    state = models.CharField(max_length=2)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.comment
