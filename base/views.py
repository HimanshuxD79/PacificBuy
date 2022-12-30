from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .models import Cart, Customers, Product, OrderPlaced
from .forms import CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.


def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'base/home.html')


class ProductView(View):
    def get(self, request):
        mobiles = Product.objects.filter(category='M')
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        shoes = Product.objects.filter(category='SH')
        watches = Product.objects.filter(category='W')
        laptop = Product.objects.filter(category='L')

        return render(request, 'index.html', {
            'mobiles': mobiles,
            'topwears': topwears,
            'bottomwears': bottomwears,
            'shoes': shoes,
            'watches': watches,
            'laptop': laptop})


class Product_detail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'base/productdetail.html', {'product': product,'item_already_in_cart':item_already_in_cart})


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Apple' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__gt=10000)
    return render(request, 'base/mobile.html', {'mobiles': mobiles})


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            print("Quantity", p.quantity)
            print("Selling Price", p.product.discounted_price)
            print("Before", amount)
            amount += tempamount
            # print("After", amount)
        # print("Total", amount)
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount+shipping_amount
        }
        return JsonResponse(data)
    else:
        return HttpResponse("")


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.00
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            print("Quantity", p.quantity)
            print("Selling Price", p.product.discounted_price)
            print("Before", amount)
            amount += tempamount
            # print("After", amount)
        # print("Total", amount)
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount+shipping_amount
        }
        return JsonResponse(data)
    else:
        return HttpResponse("")


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            # print("Quantity", p.quantity)
            # print("Selling Price", p.product.discounted_price)
            # print("Before", amount)
            amount += tempamount
            # print("After", amount)
        # print("Total", amount)
        data = {
            'amount': amount,
            'totalamount': amount+shipping_amount
        }
        return JsonResponse(data)
    else:
        return HttpResponse("")


def add_to_cart(request):
    user = request.user
    product_id = request.GET['prod_id']
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()

    return redirect('/cart/')


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        total_amount = 0.0
        shipping_amount = 70.00
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity*p.product.discounted_price)
                amount += tempamount
                total_amount = amount+shipping_amount

        return render(request, 'base/addtocart.html', {'cart': cart, 'totalamount': total_amount, 'amount': amount})
    else:
        return redirect("handlelogin")





class ProfileView(View):

    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'base/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customers(user=user, name=name, locality=locality,
                            city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated')

        return render(request, 'base/profile.html', {'form': form, 'active': 'btn-primary'})


@login_required
def checkout(request):
    user = request.user
    add = Customers.objects.filter(user=request.user)

    cart_items = Cart.objects.filter(user=request.user)
    amount = 0.0
    shipping_amount = 70.00
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount += tempamount
        totalamount = amount+shipping_amount
    return render(request, 'base\checkout.html', {'cart_items': cart_items, 'totalamount': totalamount, 'add': add})


def payment_done(request):
    custid = request.GET.get('custid')
    print("Customer ID", custid)
    user = request.user
    cartid = Cart.objects.filter(user=user)
    customer = Customers.objects.get(id=custid)
    print(customer)
    for cid in cartid:
        OrderPlaced(user=user, customer=customer,
                    product=cid.product, quantity=cid.quantity).save()
        print("Order Saved")
        cid.delete()
        print("Cart Item Deleted")
    return redirect("orders")


def address(request):
    add = Customers.objects.filter(user=request.user)
    return render(request, 'base/address.html', {'add': add, 'active': 'btn-primary'})


def orders(request):
    if request.user.is_authenticated:
        op = OrderPlaced.objects.filter(user=request.user)
        return render(request, 'base/orders.html', {'order_placed': op})
    else:
        return redirect("handlelogin")
