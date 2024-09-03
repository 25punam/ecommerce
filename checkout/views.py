from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import CustomerPaymentDetails
from products.models import CartModel, Order
import uuid
from django.views.decorators.csrf import csrf_exempt
import razorpay

@csrf_exempt
@login_required(login_url='/')
def checkout(request):
    cart_items = CartModel.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        payment_method = request.POST.get('payment-method')

        order = Order.objects.create(
            cart=cart_items.first(),
            quantity=cart_items.count()
        )

        transaction_id = str(uuid.uuid4())

        CustomerPaymentDetails.objects.create(
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

        cart_items.delete()

        if payment_method == 'razorpay':
            amount = int(total_price * 100)  
            order_currency = 'INR'

            client = razorpay.Client(
            auth=("rzp_test_uvJ9RLNvlUxw8Y", "yg7jO31c5YDExNLJ1bhkXUDa"))

            payment = client.order.create({
                'amount': amount,
                'currency': 'INR',
                'payment_capture': '1'
            })

            return render(request, 'payment.html', {
                'payment': payment,
                'amount': total_price,
                'currency': order_currency,
                'order_id': payment['id']
            })
        return redirect('order_success')

    return render(request, 'checkout.html',{'cart_items':cart_items,'total_price':total_price})


@csrf_exempt
def order_success(request):
    return render(request, "order_success.html")
