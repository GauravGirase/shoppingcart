from django.shortcuts import render,HttpResponseRedirect,redirect
from .models import Product, Customer, Order
from django.contrib.auth.hashers import make_password, check_password
from store.middlewares.auth import auth_middleware

def store(request):
    if request.method == "POST":
        product = request.POST.get('product')
        print(product)
        remove = request.POST.get('remove')
        print(remove)
        cart = request.session.get('cart')
        print(cart)
        if cart:
            quantity = cart.get(product)
            print(quantity)

            if quantity:
                print(type(quantity))
                if remove:
                    if quantity<= 1:
                        cart.pop(product)
                    else:
                     cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        return redirect('home')
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = Product.objects.all()
    return render(request,'store/base.html',{'products':products})

def user_login(request):
    if request.method =="POST":
        data = request.POST
        email = data.get('email')
        password = data.get("password")
        print(email, password)
        customer = Customer.objects.get(email=email)
        error_message = None

        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['email'] = customer.email

                return redirect('home')

            else:
                error_message = 'Email Or Password Is Incorrect..!'


        else:
            error_message = 'Email Or Password Is Incorrect..!'
        return render(request,'store/login.html',{'error':error_message})
    else:
        return render(request,'store/login.html')





def cart(request):
    ids = list(request.session.get('cart').keys())
    products = Product.objects.filter(id__in=ids)

    return render(request,'store/cart.html',{'products':products})

def user_logout(request):
    request.session.clear()
    return redirect("login")

def user_signup(request):
    if request.method == "POST":
        data = request.POST
        f = data.get('firstname')
        l = data.get('lastname')
        e = data.get('email')
        m = data.get('mobile')
        p = data.get('password')
        hashpass = make_password(p)
        customer = Customer.objects.create(firstname=f,lastname=l,email=e,mobile=m,password=hashpass)
        return HttpResponseRedirect('/')
    else:
        return render(request,'store/signup.html')

def checkout(request):
    if request.method == "POST":
        address = request.POST.get('address')
        number = request.POST.get('mobile')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        ids = list(request.session.get('cart').keys())
        products = Product.objects.filter(id__in=ids)
        for product in products:
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          quantity=cart.get(str(product.id)),
                          address=address,
                          phone=number
                          )
            order.save()
        request.session['cart'] = {}
        return redirect('cart')
    else:
        return render(request, 'store/checkout.html')

@auth_middleware
def orders(request):
    if request.method == "GET":
        customer = request.session.get('customer')
        orders = Order.objects.filter(customer=customer)
        return render(request,'store/orders.html',{'orders': orders})