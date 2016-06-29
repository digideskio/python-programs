from django.db import models
from django.dispatch import receiver

import threading

from . import signals


# Create your models here.
lock = threading.Lock()


class Comment(models.Model):
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.comment


class States(models.Model):
    uf = models.CharField(max_length=2, primary_key=True, unique=True)
    state = models.CharField(max_length=200)
    comment = models.ManyToManyField(Comment)

    def __str__(self):
        return self.uf


def write_file(request, state, log_file):
    lock.acquire()
    with open(log_file, 'a') as fd:
        fd.write('path: {}       username: {}       state: {}\n'.format(
            request.path, request.user.username, state.upper()))
    lock.release()


@receiver(signals.log_signal, sender=States)
def log_handler(sender, **kwargs):
    req = kwargs['requests']
    state = kwargs['state']
    log_file = kwargs['file']
    try:
        threading.Thread(target=write_file, args=(req, state, log_file)).start()
    except Exception as e:
        print 'Error: {}'.format(e)
