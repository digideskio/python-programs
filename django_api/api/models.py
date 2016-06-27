from django.db import models
from django.dispatch import receiver

from . import signals


# Create your models here.


class States(models.Model):
    uf = models.CharField(max_length=2, primary_key=True, unique=True)
    state = models.CharField(max_length=200)

    def __str__(self):
        return self.uf


# class Comments(models.Model):
#     uf = models.ForeignKey(States, on_delete=models.CASCADE)
#     comment = models.CharField(max_length=200)

#     def __str__():
#         return self.comment


@receiver(signals.log_signal, sender=States)
def log_handler(sender, **kwargs):
    req = kwargs['requests']
    state = kwargs['state']
    with open('log.txt', 'a') as fd:
        fd.write('path: {} 		username: {} 	state: {}\n'.format(
            req.path, req.user.username, state.upper()))
