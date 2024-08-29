from django.shortcuts import render,redirect
from .models import ProductModel, CartModel 
from django.contrib.auth.decorators import login_required

def home(request):
    products = ProductModel.objects.all()
    username = request.session.get('username', 'None')
    return render(request, 'home.html', {'products': products})


def cart_detail(request, product_id):
    detail = ProductModel.objects.get(id=product_id)
    return render(request, 'detail.html', {'detail': detail})


@login_required(login_url='/')
def add_to_cart(request, product_id):
    product = ProductModel.objects.get(id=product_id)
    cart_item, created = CartModel.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    
    cart_item.save()
    return redirect('order_list')



@login_required(login_url='/')
def order_list(request):
    items= CartModel.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in items) 
    return render(request ,'order_list.html',{'items': items,'total': total_price})


@login_required(login_url='/')
def update_quantity(request, product_id):
    cart_item = CartModel.objects.get( user=request.user, product_id=product_id)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1
        
        cart_item.save()
        
    return redirect('order_list')


@login_required(login_url='/')
def remove_from_cart(request, product_id):
    cart_item = CartModel.objects.get(user=request.user ,product_id=product_id)
    cart_item.delete()
    return redirect('order_list')