from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Menu, Item, Ingredient

from . import views

import datetime

client = Client

from .forms import MenuForm


# models tests
class TestModels(TestCase):

    def setUp(self):
        user = User.objects.create_user(username= 'trace')
        """ tests creation of mineral objects:

        asserts correct type, instance of, and contains
        """

        menu = Menu.objects.create(
            season='spring',
            created_date=datetime.date.today(),
            expiration_date=datetime.date(year=2007, month=12, day=25)
        )

        items = Item.objects.create(
            name='soda',
            description='a very yummy type of thing',
            chef=user,
            created_date=datetime.date.today(),
            standard=False,
            )

    ingredients = Ingredient.objects.create(
            name= 'swiss miss'
             )

    def test_model(self):
        menu = Menu.objects.get(season='spring')
        item = Item.objects.get(name='soda')


        menu.items.add(item)

        self.assertIsInstance(menu, Menu)
        self.assertTrue(menu, type(object))
        self.assertTrue(hasattr(menu, 'expiration_date'))
        self.assertTrue(hasattr(menu, 'items'))


class Test_Views(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='ben')
        """ setup for tests to instantiate mineral objects to test against"""
        self.menu = Menu.objects.create(
            season='spring',
            created_date=datetime.date.today(),
            expiration_date=datetime.date(year=2007, month=12, day=25)
            )

        self.items = Item.objects.create(
            name='soda',
            description='a very yummy type of thing',
            chef=user,
            created_date=datetime.date.today(),
            standard=False,
            )

    def test_menu_list(self):
        resp = self.client.get('/')
        self.assertEquals(resp.status_code, 200)
        self.assertEqual(resp.resolver_match.func, views.menu_list)
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')

    def test_menu_detail(self):
        resp = self.client.get(reverse('menu:menu_detail',
                                       kwargs={'pk': self.menu.pk}))
        self.assertEquals(resp.status_code, 200)
        self.assertEqual(self.menu, resp.context['menu'])

    def test_item_detail(self):
        resp = self.client.get(reverse('menu:item_detail',
                                       kwargs={'pk': self.items.pk}))
        self.assertEquals(resp.status_code, 200)
        self.assertEqual(self.items, resp.context['item'])