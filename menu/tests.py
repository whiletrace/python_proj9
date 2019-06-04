from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import MenuForm
from .models import Menu, Item, Ingredient
from . import views

import datetime

client = Client


# models tests
class TestModels(TestCase):

    def setUp(self):
        """
        creates model instances of User, Menu, Item

        these instances are used as stubs within the
        this TestCase when evaluating assertions
        :var: user
        :var: menu
        :var: items
        :var: ingredients

        :rtype: object
        """
        user = User.objects.create_user(username='trace')

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

    ingredients = Ingredient.objects.create(
        name='swiss miss'
        )

    def test_model(self):
        """
        Tests that models functionality is executing as expected

        this test verifies that menu is an instance of the class Menu
        that menu is typ object and has attributes expiration_date
        and items as defined in models.py

        :rtype: object
        """
        menu = Menu.objects.get(season='spring')

        self.assertIsInstance(menu, Menu)
        self.assertTrue(menu, type(object))
        self.assertTrue(hasattr(menu, 'expiration_date'))
        self.assertTrue(hasattr(menu, 'items'))


class TestViews(TestCase):

    def setUp(self):
        """
        creates model instances of User, Menu, Item

        these instances are used as stubs within the
        TestCase when evaluating assertions ach
        instance will have attribute values that
        have been set to mimic model.py objects
        attributes
        :var: user
        :var: menu
        :var: items
        :var: ingredients

        :rtype: object
        """
        user = User.objects.create_user(username='ben')

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
        self.ingredients = Ingredient.objects.create(
            name='swiss miss'
            )

        spring_menu = self.menu
        spring_items = self.items
        spring_ingredients = self.ingredients

        spring_items.ingredients.add(spring_ingredients)
        spring_items.save()

        spring_menu.items.add(spring_items)
        spring_menu.save()

        self.form_data = {'season': 'spring',
                          'items': [spring_items],
                          'expiration_date': '2007-12-25'
                          }

    def test_menu_list(self):
        """
        Unit test to test menu_list view

        uses djangos built in test client
        tests whether URL status code is 200
        whether the whether logic is coming from
        views.menu_list
        correct view and tests to make sure that
        template being rendered is menu/list_all_current_menus.html

        :rtype: object

        """
        resp = self.client.get('/')
        self.assertEquals(resp.status_code, 200)
        self.assertEqual(resp.resolver_match.func, views.menu_list)
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')

    def test_menu_detail(self):
        """
        Unit test to test menu_detail view

        uses djangos built in test client
        tests whether URL status code is 200
        tests whether view is routed to intended URL
        whether the whether logic is coming from views.menu.detail
        tests to makes sure view is passing correct values as context

        :rtype: object

        """

        resp = self.client.get(reverse('menu:menu_detail',
                                       kwargs={'pk': self.menu.pk}))
        self.assertEquals(resp.status_code, 200)
        self.assertEqual(self.menu, resp.context['menu'])

    def test_item_detail(self):
        """
        Unit test to test item_detail view

        uses djangos built in test client
        tests whether URL status code is 200
        tests whether view is routed to intended URL
        tests to makes sure view is passing correct values as context

        :rtype: object

        """
        resp = self.client.get(reverse('menu:item_detail',
                                       kwargs={'pk': self.items.pk}))
        self.assertEquals(resp.status_code, 200)
        self.assertEqual(self.items, resp.context['item'])

    # test to cover create_new_menu
    # not getting coverage in view as expected
    # reviewer please add suggestions so
    # to help me get better penetration

    def test_create_new_menu(self):
        form = MenuForm(data=self.form_data)

        self.assertTrue(form.is_valid())
        req = self.client.post('/menu/new/', {'form': form})
        self.assertEquals(req.status_code, 200)
        self.assertEquals(Menu.objects.last().expiration_date, datetime.date(
            year=2007, month=12, day=25))

        self.assertTemplateUsed(req, 'menu/menu_edit.html')
