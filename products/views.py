from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import ProductModel, CartModel 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token

def home(request):
    csrf_token = get_token(request)
    products = ProductModel.objects.all()
    username = request.session.get('username', 'None')
    return render(request, 'home.html', {'products': products, 'csrf_token': csrf_token})


def cart_detail(request, product_id):
    detail = ProductModel.objects.get(id=product_id)
    return render(request, 'detail.html', {'detail': detail})


@login_required(login_url='/account/login/')
def add_to_cart(request, product_id):
    product = ProductModel.objects.get(id=product_id)
    cart_item, created = CartModel.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    
    cart_item.save()
    return redirect('order_list')


@require_POST
@login_required(login_url='/account/login/')
def add_to_cart_ajax(request):
    """AJAX endpoint for adding products to cart without page reload"""
    try:
        product_id = request.POST.get('product_id')
        if not product_id:
            return JsonResponse({'success': False, 'message': 'Product ID is required'}, status=400)
        
        product = ProductModel.objects.get(id=product_id)
        cart_item, created = CartModel.objects.get_or_create(user=request.user, product=product)
        
        if not created:
            cart_item.quantity += 1
        else:
            cart_item.quantity = 1
        
        cart_item.save()
        return JsonResponse({
            'success': True, 
            'message': f'{product.name} added to cart!',
            'product_name': product.name,
            'cart_count': CartModel.objects.filter(user=request.user).count()
        })
    except ProductModel.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)



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