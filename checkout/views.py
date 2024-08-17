from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Order, CustomerPaymentDetails
from django.contrib.auth.models import User
from products.models import CartModel  

@login_required(login_url='/')
def checkout(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        payment_method = request.POST.get('payment-method')

        cart_items = CartModel.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('order_list')

        total_price = sum(item.total_price() for item in cart_items)

        order = Order.objects.create(
            cart=cart_items.first(),
            quantity=cart_items.count()
        )
        
        transaction_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        payment_details = CustomerPaymentDetails.objects.create(
            order=order,
            user=request.user,
            amount=total_price,
            payment_date=datetime.now(),
            transaction_id=transaction_id,
            status='Pending',
            shipping_address=address,
            zip_code=zip_code,
            city=city,
            state=state,
            payment_method=payment_method
        )

        if payment_method == 'paypal':
            return redirect('/')  
        
        return redirect('order_success')  
  

    return render(request, 'checkout.html',)


def order_success(request):
    return render(request,"order_success.html")

