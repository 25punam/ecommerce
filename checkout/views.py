from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import CustomerPaymentDetails
from products.models import CartModel, Order
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.urls import reverse
import uuid

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
        total_price = sum(item.total_price() for item in cart_items)

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

        if payment_method == 'paypal':
            return redirect('process_paypal_payment', order_id=order.id, amount=total_price, user_id=request.user.id)
        return redirect('order_success')

    return render(request, 'checkout.html')

def process_paypal_payment(request, order_id, amount, user_id):
    amount = float(amount)
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": f"{amount:.2f}",
        "item_name": f"Order {order_id}",
        "invoice": str(order_id),
        "currency_code": "INR",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('order_success')),
        "cancel_return": request.build_absolute_uri(reverse('checkout')),
        "custom": str(user_id),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_paypal_payment.html', {'form': form})

def order_success(request):
    return render(request, "order_success.html")
