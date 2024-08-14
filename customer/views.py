
from django.shortcuts import render,redirect
from .models import ProductModel, CartModel 
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(["POST"])
def create_product(request):
    if request.method == "POST":
        try:
            name = request.data.get("name")
            desc = request.data.get("desc")
            price = request.data.get("price")
            image = request.FILES.get("image")
            
            ProductModel.objects.create(
                name=name,
                desc=desc,
                price=price,
                image=image
            )
            
            return Response({"message": "Product created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
@api_view(["POST"])
def delete_product(request):
    if request.method == "POST":
        try :
            ProductModel.objects.filter(name=request.data["name"]).delete()

            return Response("Product delete successfully",status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)},status=status.HTTP_400_BAD_REQUEST)
        

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
        # If the item already exists in the cart, increase the quantity
        cart_item.quantity += 1
    else:
        # If the item was just created, set the initial quantity
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


@login_required(login_url='/')
def checkout(request):
  
    return render(request,'checkout.html')
