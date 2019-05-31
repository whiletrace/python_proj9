from django.db import models

import datetime


class Menu(models.Model):
    """
    class definition for Menu object instances and db tables

    attributes season, items, created_date,
    expiration_date to objects the values
    of attributes will be determined by
    data stored in related db tables
    """
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='items')
    created_date = models.DateField(
            default=datetime.date.today)
    expiration_date = models.DateField(
            blank=True, null=True)

    def __str__(self):
        return self.season


class Item(models.Model):
    """
    class definition for Item object instances and db tables

    attributes name, description, chef, created_date
    standard and ingredients to objects, the values
    of attributes will be determined by
    data stored in related db tables
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_date = models.DateField(
            default=datetime.date.today)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient',
                                         related_name='ingredients')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    class definition for Ingredient object instances and db tables

    attributes name will be assigned to objects, the values
    of attributes will be determined by
    data stored in related db tables
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
