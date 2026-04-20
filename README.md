# E-commerce Project

A modern, full-featured e-commerce platform built with Django and Razorpay payment integration. This platform provides an intuitive shopping experience with secure payment processing.

<img width="1072" height="630" alt="image" src="https://github.com/user-attachments/assets/ad333d96-cf94-4bbb-9413-a4d561ceea10" />

<img width="1074" height="625" alt="image" src="https://github.com/user-attachments/assets/b2542d89-6def-49f4-a7d7-34873ca4849b" />

<img width="1067" height="629" alt="image" src="https://github.com/user-attachments/assets/59ff608c-b00c-41d3-a108-18badaeec2e1" />

![Screenshot 2024-09-04 181135](https://github.com/user-attachments/assets/459e7135-f017-498a-ac50-867a0619c980)

![Screenshot 2024-09-04 181159](https://github.com/user-attachments/assets/c2c2edc7-e509-4e51-9a97-851feb7e750e)

---


## 📦 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- MySQL/SQLite Database

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/25punam/ecommerce.git
   cd ecommerce
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   source env/Scripts/activate  # On Windows
   source env/bin/activate      # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

---

## 💳 Payment Guide

### **For New Users - Complete Payment Walkthrough**

Follow these simple steps to complete your purchase:

#### **Step 1: Browse Products**
1. Visit the homepage
2. Browse through available products
3. View product details by clicking the **"View"** button
4. When you find a product you like, click **"Add to Cart"**
5. A confirmation popup will appear saying "Product added to cart!"
6. Continue browsing or proceed to checkout

#### **Step 2: Review Your Cart**
1. Click the **Cart** icon at the top of the page
2. Review all items in your cart
3. You can:
   - Increase/decrease quantity using the +/- buttons
   - Remove items by clicking the delete icon
   - See the total price calculated at the bottom

#### **Step 3: Proceed to Checkout**
1. Click the **"Checkout"** button in your cart

#### **Step 4: Enter Shipping Information**
Fill in the following details:

**Billing Information:**
- **First Name**: Your first name
- **Last Name**: Your last name
- **Email Address**: A valid email (e.g., `your.email@example.com`)
  - This email will receive your order confirmation
  - Must be in valid format: `user@domain.com`
  - Invalid emails will be rejected
- **Shipping Address**: Your complete delivery address
- **City**: Your city
- **State**: Your state/province
- **ZIP Code**: Your postal/ZIP code (5-6 digits)


#### **Step 5: Select Payment Method**
Currently, we support **Razorpay** as our primary payment method.

**Why Razorpay?**
- Secure and trusted payment gateway
- Supports multiple payment options (Credit/Debit card, UPI, Net Banking, Wallets)
- Instant payment confirmation
- Safe and encrypted transactions

#### **Step 6: Complete the Payment**
1. Click **"Complete Purchase"** button
2. You'll be redirected to Razorpay's secure payment page
3. Enter your payment details:
   - **Card/UPI Details**: Depending on your chosen payment method
   - **OTP**: Verify with the one-time password sent to your phone/email
4. Once payment is successful, you'll receive a confirmation message


