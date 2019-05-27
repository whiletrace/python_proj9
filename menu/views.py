from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *


def menu_list(request):
    """
    :param request:
    :type request:
    :return:
    :rtype:


    """

    menus = Menu.objects.filter(
        expiration_date__lte=datetime.date.today()).order_by(
        'expiration_date').prefetch_related('items')

    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})


def menu_detail(request, pk):

    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    try: 
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
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
