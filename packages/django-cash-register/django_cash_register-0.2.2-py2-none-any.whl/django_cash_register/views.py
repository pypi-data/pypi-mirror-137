from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import LoginForm
from .models import CartList, Cart, Currency, Product


def cartBtns(request):
    """(Ajax) Interacts with buttons in the shopping cart."""

    if request.method == 'POST':
        operaton = request.POST.get('operation')
        cart_number = request.POST.get('cart_number')

        if operaton in ('item_counter_plus', 'item_counter_minus', 'item_remove'):
            product_id = request.POST.get('product_id', None)
            cart_product = get_object_or_404(Cart, pk=product_id[8:])
            product_count = get_object_or_404(Product, pk=cart_product.product.pk).product_count

            if operaton == 'item_counter_plus' and cart_product.product_count < product_count:
                cart_product.product_count_plus()

            if operaton == 'item_counter_minus' and cart_product.product_count > 1:
                cart_product.product_count_minus()

            if operaton == 'item_remove':
                cart_product.delete()

        if operaton == 'item_remove_all':
            Cart.delete_all(cart_number)
        
        if operaton == 'sell':
            Cart.sell_all(cart_number)

    return redirect(cash_register_view)


def getCartItems(request):
    """(Ajax) Returns items from the cart."""

    if request.user.is_authenticated and request.user.is_staff:
        cart = CartList.objects.get_or_create(user=request.user)
        new_update = str(cart[0].last_update)[:-6]

        currency = Currency.objects.filter(active=True).values_list('value', 'float_right')[0]

        products = Cart.objects.filter(cart_number__user=request.user).annotate(
            total_price=F('product_count') * F('product__price')).values('pk', 'product__image',
                                                                         'product__name', 'product__weight',
                                                                         'product__unit__name', 'product_count',
                                                                         'total_price', 'cart_number')

        cart_number = CartList.objects.filter(user=request.user).first().pk

        total_price = sum(item['total_price'] for item in products)

        response = {
            'cart_number': cart_number,
            'products': list(products),
            'total_price': total_price,
            'currency': currency,
            'new_update': new_update,
        }

        return JsonResponse(response)

    return redirect(cash_register_login_view)


def cash_register_logout(request):
    auth.logout(request)
    return redirect(cash_register_login_view)


def cash_register_login_view(request):
    """Login view."""

    if request.user.is_authenticated and request.user.is_staff:
        return redirect(cash_register_view)

    context = None

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(cash_register_view)
                else:
                    context = 'Disabled account'
            else:
                context = 'Invalid login'
    else:
        form = LoginForm()
    return render(request, 'django_cash_register/login.html', {'form': form, 'context': context})


def cash_register_view(request):
    """Main app view."""

    if request.user.is_authenticated and request.user.is_staff:
        currency = Currency.objects.filter(active=True).values_list('value', 'float_right')[0]

        products = Cart.objects.filter(cart_number__user=request.user).annotate(
            total_price=F('product_count') * F('product__price'))

        cart_number = CartList.objects.get_or_create(user=request.user)[0].pk

        total_price = sum(item.product.price * item.product_count for item in products)

        last_update = str(CartList.objects.get_or_create(user=request.user)[0].last_update)[:-6]

        context = {
            'cart_number': cart_number,
            'currency': currency,
            'products': products,
            'total_price': total_price,
            'last_update': last_update,
        }

        return render(request, 'django_cash_register/index.html', context)

    return redirect(cash_register_login_view)
