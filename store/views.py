import datetime
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import CreateUserForm
from .models import *
from .utils import cartData, guestOrder


def home(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'home.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('ecommWebsite:home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                phone = form.cleaned_data.get('phone')
                Customer.objects.create(
                    user=user,
                    name=user.username,
                    phone=phone
                )
                messages.success(request, 'Account was created for ' + username + '!')
                return redirect('ecommWebsite:login')

        context = {'form': form}
        return render(request, 'register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('ecommWebsite:menu')

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('ecommWebsite:menu')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('ecommWebsite:login')


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'checkout.html', context)


def categories(request):
    return {
        'categories': Category.objects.all()
    }


def menu(request):
    data = cartData(request)
    cartItems = data['cartItems']

    categories = Category.objects.all()
    products = Product.objects.all().order_by('category')
    pizzas = Product.objects.filter(category__name__contains="Pizza").order_by('price')
    pastas = Product.objects.filter(category__name__contains="Pasta").order_by('price')
    sides = Product.objects.filter(category__name__contains="Sides").order_by('price')
    beverages = Product.objects.filter(category__name__contains="Beverages").order_by('price')
    context = {'products': products, 'cartItems': cartItems, 'categories': categories, 'pizzas': pizzas,
               'pastas': pastas, 'sides': sides, 'beverages': beverages}
    return render(request, 'menu.html', context)


def about(request):
    context = {}
    return render(request, 'about.html', context)


def contact(request):
    context = {}
    return render(request, 'contact.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added.', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            transaction_id=transaction_id,
            customer=customer,
            order=order,
            housenum=data['shipping']['housenum'],
            brgy=data['shipping']['brgy'],
            city=data['shipping']['city'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment Complete!', safe=False)
