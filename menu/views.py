from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from .forms import *


def menu_list(request):
    """
    logic for URL '/'

    outputs a list of menus that expiration dates are
    less than or equal to today's date pre_fetches related
    items this is stored in the variable menu and is passed
    as context to the list_all_current_menus.html template
    :param request: HTTP GET Request
    :type request: object
    :return: HTTP Response
    :rtype: object
     """

    menus = Menu.objects.filter(
        expiration_date__lte=datetime.date.today()).order_by(
        'expiration_date').prefetch_related('items')

    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})


def menu_detail(request, pk):
    """
    logic for  URL '/menu/<int:pk'

    detail of menu that matches menu_id passed through URL
    items this is stored in the variable menu and is passed
    as context to the menu_detail.html template
    :param request: HTTP GET Request
    :type request: object
    :param pk: menu_id
    :type pk: int
    :return: HTTP Response
    :rtype: object
    """

    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    """
    logic for URL /menu/item/<int:pk>

    detail of item that matches item_id passed through URL
    this is stored in the variable item and is passed
    as context to the detail_item.html template
    :param request: HTTP GET Request
    :type request: object
    :param pk: item_id
    :type pk: int
    :return: HTTP Response
    :rtype: object
    """
    item = Item.objects.get(pk=pk)

    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    """
        responsible for logic for URL /menu/new/

        handles logic to create a new menu object
        this function instantiates a form object
        forms.MenuForm which is a ModelForm
        if data received by form from user is valid
        the form will save and a new Model object instance
        of Menu will be created with its attributes values defined
        within the forms fields
        :param request: HTTP POST request
        :type request: object
        :return: HTTP Response
        :rtype: object
    """

    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = datetime.date.today()
            menu.save()
            return redirect('menu:menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/menu_edit.html', {'form': form})


def edit_menu(request, pk):
    """
        responsible for logic for URL /menu/<int:pk>/edit

        handles logic to update a  menu object
        this function instantiates a form object
        forms.MenuForm which is a ModelForm
        form is prepopulated with data from menu object
        whose id is passed through the URL
        if data received by form from user is valid
        the form will save and a new Model object instance
        of Menu will be created with its attributes values defined
        within the forms fields
        :param pk: menu_id
        :type pk: int
        :param request: HTTP POST request
        :type request: object
        :return: HTTP Response
        :rtype: object

    """
    menu = get_object_or_404(Menu, pk=pk)

    form = MenuForm(instance=menu)
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.save()
            return redirect('menu:menu_detail', pk=menu.pk)
        else:
            form = MenuForm(instance=menu)
    return render(request, 'menu/menu_edit.html', {'form': form,
                                                   'menu': menu})
