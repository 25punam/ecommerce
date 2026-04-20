from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import CustomerPaymentDetails
from .forms import CheckoutForm
from products.models import CartModel, Order
import uuid
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import hmac
import hashlib

@csrf_exempt
@login_required(login_url='/account/login/')
def checkout(request):
    cart_items = CartModel.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    if request.method == "POST":
        if not cart_items.exists():
            messages.error(request, 'Your cart is empty. Please add items before checking out.')
            return redirect('order_list')

        form = CheckoutForm(request.POST)
        
        if form.is_valid():
            # Extract validated data from form
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            zip_code = form.cleaned_data.get('zip_code')
            payment_method = form.cleaned_data.get('payment_method')

            order = Order.objects.create(
                cart=cart_items.first(),
                quantity=cart_items.count()
            )

            transaction_id = str(uuid.uuid4())

            CustomerPaymentDetails.objects.create(
                order=order,
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                email=email,
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

            # Send email notification BEFORE showing payment page
            try:
                send_mail(
                    'Order Confirmation - Your Order Has Been Received',
                    f"""Hello {first_name} {last_name},

Thank you for your order! Your order has been successfully created and is awaiting payment.

Order ID: {order.id}
Transaction ID: {transaction_id}
Total Amount: ₹{total_price}

Shipping Address:
{address}
{city}, {state} {zip_code}

Please complete your payment to finalize your order. You will receive another confirmation email once payment is successful.

Best regards,
The E-Commerce Team""",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                messages.warning(request, f'Order created but email notification failed: {str(e)}')

            # Process Razorpay payment (only payment method available)
            amount = int(total_price * 100)  

            try:
                client = razorpay.Client(
                    auth=("rzp_test_drrQ8dUerWW3jC", "pbKoVGS3BT0ykzMu9wnKE3Hr")
                )

                payment = client.order.create({
                    'amount': amount,
                    'currency': 'INR',
                    'payment_capture': '0'
                })

                # Store payment details in session for verification later
                request.session['razorpay_order_id'] = payment['id']
                request.session['order_id'] = order.id
                request.session['customer_email'] = email
                request.session['customer_name'] = f"{first_name} {last_name}"

                return render(request, 'payment.html', {
                    'payment': payment,
                    'amount': total_price,
                    'order_id': payment['id'],
                    'user': request.user,
                    'order': order
                })
            except Exception as e:
                messages.error(request, f'Payment gateway error: {str(e)}')
                return redirect('order_list')
            
            return redirect('order_success')
        else:
            # Form validation failed
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.replace("_", " ").title()}: {error}')
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price
    })


@csrf_exempt
@login_required(login_url='/account/login/')
def payment_success(request):
    """
    Handle successful Razorpay payment and redirect to homepage with cleared cart.
    """
    if request.method == 'POST':
        try:
            # Get payment details from request
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_signature = request.POST.get('razorpay_signature')
            
            # Verify payment signature
            payment_details = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id
            }
            
            client = razorpay.Client(
                auth=("rzp_test_drrQ8dUerWW3jC", "pbKoVGS3BT0ykzMu9wnKE3Hr")
            )
            
            # Verify signature
            is_valid = verify_razorpay_signature(
                payment_details,
                razorpay_signature,
                "pbKoVGS3BT0ykzMu9wnKE3Hr"
            )
            
            if is_valid:
                # Update payment status to successful
                try:
                    payment_record = CustomerPaymentDetails.objects.get(
                        order_id=request.session.get('order_id')
                    )
                    payment_record.status = 'Completed'
                    payment_record.transaction_id = razorpay_payment_id
                    payment_record.save()
                    
                    # Clear cart items for this user
                    CartModel.objects.filter(user=request.user).delete()
                    
                    # Clear session
                    if 'razorpay_order_id' in request.session:
                        del request.session['razorpay_order_id']
                    if 'order_id' in request.session:
                        del request.session['order_id']
                    
                    messages.success(request, 'Payment successful! Thank you for your order.')
                except CustomerPaymentDetails.DoesNotExist:
                    messages.error(request, 'Payment recorded but order not found.')
            else:
                messages.error(request, 'Payment signature verification failed.')
                return redirect('order_list')
        except Exception as e:
            messages.error(request, f'Error processing payment: {str(e)}')
            return redirect('order_list')
    
    # Redirect to homepage with cleared cart and session
    return redirect('home')


@csrf_exempt
def payment_cancel(request):
    """
    Handle payment cancellation - redirect to homepage with cleared session.
    """
    try:
        # Clear session data
        if 'razorpay_order_id' in request.session:
            del request.session['razorpay_order_id']
        if 'order_id' in request.session:
            del request.session['order_id']
        if 'customer_email' in request.session:
            del request.session['customer_email']
        if 'customer_name' in request.session:
            del request.session['customer_name']
        
        request.session.save()
        messages.info(request, 'Payment cancelled. You can continue shopping or try again later.')
    except Exception as e:
        print(f"Error clearing session: {str(e)}")
    
    # Redirect to homepage
    return redirect('home')


@csrf_exempt
@login_required(login_url='/')
def order_success(request):
    """
    Order success page - clears cart and session.
    """
    # Clear cart items
    CartModel.objects.filter(user=request.user).delete()
    
    # Clear payment-related session data
    if 'razorpay_order_id' in request.session:
        del request.session['razorpay_order_id']
    if 'order_id' in request.session:
        del request.session['order_id']
    
    request.session.save()
    return render(request, "order_success.html")


def verify_razorpay_signature(payment_details, razorpay_signature, secret_key):
    """
    Verify Razorpay payment signature for security.
    """
    try:
        message = f"{payment_details['razorpay_order_id']}|{payment_details['razorpay_payment_id']}"
        signature = hmac.new(
            secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature == razorpay_signature
    except Exception:
        return False










