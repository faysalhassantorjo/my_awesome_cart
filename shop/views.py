from math import ceil
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Coupon, Product, Profile, CartItem, Suggestion, Order, OrderItem
from .forms import SuggestionForm
from django.core.paginator import Paginator


@login_required
def buy_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        order = Order.objects.create(user=request.user, status='pending')
        OrderItem.objects.create(order=order, product=product, quantity=quantity)
        return redirect('checkout', order_id=order.id)

    return redirect('product_details', product_id=product.id)


@login_required
def checkout_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()  # related_name অনুযায়ী ঠিক করা হয়েছে
    total_price = sum(item.product.price * item.quantity for item in order_items)

    return render(request, 'shop/checkout.html', {
        'order': order,
        'order_items': order_items,
        'total_price': total_price,
    })


@login_required
def apply_coupon(request):
    code = request.GET.get('code')
    try:
        coupon = Coupon.objects.get(code=code, is_active=True)
        return JsonResponse({'valid': True, 'discount': coupon.discount_percent})
    except Coupon.DoesNotExist:
        return JsonResponse({'valid': False})


def suggestion_page(request):
    all_suggestions = Suggestion.objects.all().order_by('-created_at')
    paginator = Paginator(all_suggestions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = SuggestionForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = SuggestionForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('suggestion_page')
        else:
            return redirect('login')

    return render(request, 'shop/suggestion.html', {
        'page_obj': page_obj,
        'form': form
    })


def edit_suggestion(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk)
    if request.user != suggestion.user:
        return redirect('suggestion_page')

    if request.method == 'POST':
        form = SuggestionForm(request.POST, request.FILES, instance=suggestion)
        if form.is_valid():
            form.save()
            return redirect('suggestion_page')
    else:
        form = SuggestionForm(instance=suggestion)

    return render(request, 'shop/edit_suggestion.html', {
        'form': form,
        'suggestion': suggestion
    })


def delete_suggestion(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk)
    if request.user == suggestion.user:
        suggestion.delete()
    return redirect('suggestion_page')


def middleware(request):
    x = 10 / 0  # Just for testing
    return HttpResponse("This is the middleware test view.")


@login_required
def profile(request):
    profile = request.user.profile
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'shop/profile.html', {
        'profile': profile,
        'orders': orders,
        'user': request.user,
    })


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']
        profile_pic = request.FILES.get('profile_pic')

        if password != confirm:
            messages.error(request, 'Passwords do not match')
            return redirect('signup_view')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signup_view')

        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user, profile_pic=profile_pic)

        messages.success(request, 'Account created successfully')
        return redirect('login_view')

    return render(request, 'shop/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('ShopHome')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login_view')
    return render(request, 'shop/login.html')


def logout_view(request):
    logout(request)
    return redirect('login_view')


def index(request):
    allProds = []
    hero = Product.objects.all()
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        allProds.append([cat, prod])

    return render(request, 'shop/index.html', {
        'allProds': allProds,
        'hero': hero
    })


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_page.html', {'product': product})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        cart_item.quantity = quantity if created else cart_item.quantity + quantity
        cart_item.save()
    else:
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('view_cart')


def view_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total = sum(item.subtotal() for item in cart_items)
        return render(request, 'shop/view_cart.html', {
            'cart_items': cart_items,
            'total': total,
            'session_cart': None
        })
    else:
        cart = request.session.get('cart', {})
        products = []
        total = 0
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            subtotal = product.price * quantity
            products.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
            total += subtotal

        return render(request, 'shop/view_cart.html', {
            'cart_items': None,
            'total': total,
            'session_cart': products
        })


def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
        item.delete()
        messages.success(request, "Item removed from cart.")
    else:
        cart = request.session.get('cart', {})
        cart.pop(str(product_id), None)
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")

    return redirect('view_cart')
