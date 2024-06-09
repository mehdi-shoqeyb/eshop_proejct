import time

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponse
from order_module.models import Order, OrderDetail
from product_module.models import Product
from django.shortcuts import redirect,reverse
import requests
import json

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "نهایی کردن خرید شما از سایت ما"  # Required
email = ''  # Optional
mobile = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify-payment/'


def add_product_to_order(request: HttpRequest):
    product_id = request.GET.get('product_id')
    count = int(request.GET.get('count'))
    if count < 1:
        return JsonResponse({
            'status': 'invalid_count',
            'text': 'میزان وارد شده معتبر نمی باشد',
            'confirmButtonText':'مرسی از شما',
            'icon':'warning',
        })

    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id,is_active=True,is_delete=False).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False,user_id=request.user.id)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += count
                current_order_detail.save()
                return JsonResponse({
                    'status': 'success',
                    'text': 'محصول مورد نظر با موفقیت به سبد خرید اضافه شد',
                    'confirmButtonText': 'باشه ممنونم',
                    'icon': 'success',
                })
            else:
                new_detail = OrderDetail(order_id=current_order.id,product_id=product_id,count=count)
                new_detail.save()
                return JsonResponse({
                    'status': 'success',
                    'text': 'محصول مورد نظر با موفقیت به سبد خرید اضافه شد',
                    'confirmButtonText': 'باشه ممنونم',
                    'icon': 'success',
                })
        else:
            return JsonResponse({
                'status': 'not_found',
                'text': 'محصول مورد نظر یافت نشد',
                    'confirmButtonText': 'مرسی',
                    'icon': 'error',
            })
    else:
        return JsonResponse({
            'status': 'not_auth',
            'text': 'برای افزودن محصول به سبد خرید باید ابتدا وارد سایت شوید',
            'confirmButtonText': 'باشه ممنونم',
            'icon': 'error',
        })

@login_required
def request_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False,user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    if total_price == 0 :
        return redirect(reverse('user_basket_page'))

    req_data = {
        "merchant_id": MERCHANT,
        "amount": total_price * 10,
        "callback_url": CallbackURL,
        "description": description,
        # "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json", "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")

@login_required
def verify_payment(request: HttpRequest):
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
                current_order.is_paid = True
                current_order.payment_date = time.time()
                current_order.save()
                return HttpResponse('Transaction success.\nRefID: ' + str(
                    req.json()['data']['ref_id']
                ))

            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')
