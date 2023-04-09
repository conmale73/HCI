from re import split
from carts.models import Cart, CartItem
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate
from .forms import RegistrationForm
from accounts.models import Account
from carts.views import _cart_id
from category.models import Category

import requests


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            current_site = get_current_site(request=request)
            mail_subject = 'Kích hoạt tài khoản blog của bạn.'
            message = render_to_string('accounts/active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            send_email = EmailMessage(mail_subject, message, to=[email])
            #send_email.send()
            messages.success(
                request=request,
                message="Bạn đã đăng ký thành công, hãy đăng nhập vào tài khoản mới được tạo."
            )
            return redirect('login')
        else:
            messages.error(request=request, message="Đăng kí thất bại!")
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        check = Account.objects.filter(email=email)
        #username = Account.objects.get(email=email.lower()).username
        #print(check)
        #print(username)
        if email == '' or password == '':
            messages.error(request=request, message="Đăng nhập không thành công!")
        elif check is None:
            messages.error(request=request, message="Đăng nhập không thành công!")
        else:
            username = Account.objects.get(email=email.lower()).username
            #print(email)
            #print(password)
            print(username)
            user = authenticate(username=username, password=password)
            #print(user)
            if user is not None:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    cart_items = CartItem.objects.filter(cart=cart)
                    if cart_items.exists():
                        product_variation = []
                        for cart_item in cart_items:
                            variations = cart_item.variations.all()
                            product_variation.append(list(variations))
                            # cart_item.user = user
                            # cart_item.save()
                        cart_items = CartItem.objects.filter(user=user)
                        existing_variation_list = [list(item.variations.all()) for item in cart_items]
                        id = [item.id for item in cart_items]

                        for product in product_variation:
                            if product in existing_variation_list:
                                index = existing_variation_list.index(product)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity += 1
                                item.user = user
                                item.save()
                            else:
                                cart_items = CartItem.objects.filter(cart=cart)
                                for item in cart_items:
                                    item.user = user
                                    item.save()
                except Exception:
                    pass
                auth.login(request=request, user=user)
                messages.success(request=request, message="Đăng nhập thành công!")

                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    params = dict(x.split("=") for x in query.split("&"))
                    if "next" in params:
                        next_page = params["next"]
                        return redirect(next_page)
                except Exception:
                    return redirect('dashboard')
            else:
                messages.error(request=request, message="Đăng nhập không thành công!")
    links = Category.objects.all()
    context = {
        'email': email if 'email' in locals() else '',
        'password': password if 'password' in locals() else '',
        'links': links,
    }
    return render(request, 'accounts/login.html', context=context)


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request=request, message="Bạn đã đăng xuất!")
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request=request, message="Tài khoản của bạn đã được kích hoạt, vui lòng đăng nhập!")
        return render(request, 'accounts/login.html')
    else:
        messages.error(request=request, message="Liên kết kích hoạt không hợp lệ!")
        return redirect('home')


@login_required(login_url="login")
def dashboard(request):
    user = request.user
    links = Category.objects.all()
    print(user)
    fistname = user.first_name
    phone = user.phone_number
    email = user.email
    context = {
        'fistname': fistname,
        'phone': phone,
        'email': email,
        'links':links,
    }
    return render(request, "accounts/dashboard.html", context=context)


def forgotPassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request=request)
            mail_subject = 'Đặt lại mật khẩu của bạn'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.sendmail()

            messages.success(
                request=request, message="Email đặt lại mật khẩu đã được gửi đến địa chỉ email của bạn")
    except Exception:
        messages.error(request=request, message="Tài khoản không tồn tại!")
    finally:
        context = {
            'email': email if 'email' in locals() else '',
        }
        return render(request, "accounts/forgotPassword.html", context=context)


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request=request, message='Xin hãy thiết lập lại mật khẩu của bạn')
        return redirect('reset_password')
    else:
        messages.error(request=request, message="Liên kết này đã hết hạn!")
        return redirect('home')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, message="Đặt lại mật khẩu thành công!")
            return redirect('login')
        else:
            messages.error(request, message="Mật khẩu không khớp!")
    return render(request, 'accounts/reset_password.html')
