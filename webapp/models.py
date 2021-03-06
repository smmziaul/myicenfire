# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=200)
    isbn = models.CharField(max_length=200)
    authors = models.JSONField()

    number_of_pages = models.IntegerField()
    publisher = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    release_date = models.CharField(max_length=200)

    def __str__(self):
        return self.fname
