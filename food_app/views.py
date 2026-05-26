from django.shortcuts import render,redirect
from django.shortcuts import  redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
from decimal import Decimal
from .forms import CheckoutForm
from .models import FoodItem, Wishlist, Cart,Order,UserRating,Coupon
from .models import Profile
def home(request):
    items = FoodItem.objects.all()

    cat = request.GET.get('category')
    if cat:
        items = items.filter(category__name__iexact=cat)

    item_type = request.GET.get('type')
    if item_type == 'veg':
        items = items.filter(is_veg=True)
    elif item_type == 'non-veg':
        items = items.filter(is_veg=False)

    search_query = request.GET.get('search', '')
    if search_query:
        items = items.filter(name__icontains=search_query)

    user_wishlist_ids = []

    if request.user.is_authenticated:
        user_wishlist_ids = Wishlist.objects.filter(
            user=request.user
        ).values_list('item_id', flat=True)

    return render(request, 'index.html', {
        'items': items,
        'user_wishlist_ids': list(user_wishlist_ids)
    })
    
def add_to_Wishlist(request,item_id):
    if request.user.is_authenticated:
        item=get_object_or_404(FoodItem, id=item_id)
        wishlist_item=Wishlist.objects.filter(user=request.user,item=item)
        if wishlist_item.exists():
            wishlist_item.delete()
        else:
            Wishlist.objects.create(user=request.user,item=item)
        return redirect('/' )
    else:
        return redirect('/admin/')
def wishlist_page(request):
    if request.user.is_authenticated:
        my_wishlist=Wishlist.objects.filter(user=request.user)
        return render(request, 'wishlist.html',{'wishlist':my_wishlist})
    else:
        return redirect('/admin/')

def add_to_cart(request,item_id):
    if request.user.is_authenticated:
        item=get_object_or_404(FoodItem, id=item_id)
        cart_item, created=Cart.objects.get_or_create(user=request.user, item=item)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('/')
    else:
        return redirect('/admin/')

def cart_page(request):
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
        total_bill=0
        for entry in cart_items:
            total_bill += entry.item.price * entry.quantity
        return render(request,'cart.html', {'cart_items':cart_items, 'total':total_bill})
    else:
        return redirect('/admin/')
def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        cart_item= Cart.objects.filter(user=request.user, id=item_id).first()
        if cart_item:
            if cart_item.quantity >1:
                cart_item.quantity -=1
                cart_item.save()
            else:
                cart_item.delete()
        return redirect('cart_page')
    else:
        return redirect('/admin/')

def delete_cart_item(request, item_id):
    if request.user.is_authenticated:
        item=Cart.objects.filter(user=request.user, id=item_id).first()
        if item:
            item.delete()
        return redirect('cart')
    else:
        return redirect('/admin/')

def checkout(request):
    form =CheckoutForm()
    if request.method == 'POST':
        form=CheckoutForm(request.POST)
    if form.is_valid():
        payment_method=request.POST.get('payment_method')
        user_coupon=request.POST.get('coupon_code','').strip()
        cart_items =Cart.objects.filter(user=request.user)
        total=sum(item.item.price * item.quantity for item in cart_items)
        discount=0
        if user_coupon:
            try:
              coupon_obj=Coupon.objects.get(code__iexact=user_coupon,active=True) 
              discount=coupon_obj.discount_amount
              print(f"✅Coupon Applied! Discount: Rs.{discount}")
            except Coupon.DoesNotExist:
                print("❌Invalid Coupon Code!") 
        final_total= total-discount
        if final_total < 0:
            final_total=0
        order=form.save(commit=False)
        order.user=request.user
        order.total_bill=final_total 
        order.save()
        cart_items.delete()
        if payment_method == 'UPI':
            return redirect('upi_payment')
        else:
            return redirect('order_success')
    else:
        form=CheckoutForm()
    return render(request,'checkout.html',{'form':form})

def signup_view(request):
    if request.method =='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('home')
    else:
        form=UserCreationForm()
    return render(request,'signup.html',{'form':form})

def login_view(request):
    if request.method =='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            Profile.objects.get_or_create(user=user)
            return redirect('view_profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def my_orders_view(request):
    orders= Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request,'my_orders.html', {'orders':orders})

def order_success(request):
    latest_order=Order.objects.filter(user=request.user).last()
    return render(request, 'order_success.html',{'order':latest_order})

def track_order(request,order_id):
    try:
        order=Order.objects.get(id=order_id,user=request.user)
    except Order.DoesNotExist:
        return redirect('home')
    return render(request,'track_order.html',{'order':order})

def food_detail(request, item_id):
    item = get_object_or_404(FoodItem, id=item_id)
    ratings = UserRating.objects.filter(food_item=item)
    context = {
        'item' : item,
        'ratings' : ratings,
    }
    return render(request, 'food_detail.html', context)

def save_rating(request, item_id):
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        review_text = request.POST.get('review')
        food_item = get_object_or_404(FoodItem, id=item_id)
        if request.user.is_authenticated:
            UserRating.objects.create(
                user=request.user,
                food_item=food_item,
                rating=rating_value,
                review=review_text,
            )
            return redirect('food_detail', item_id=item_id)
        else:
            return redirect('login')
    return redirect('home')


@login_required
def view_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        print("Phone from POST:", request.POST.get('phone'))
        print("Address from POST:", request.POST.get('address'))
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        if request.FILES.get('profile_pic'):
            profile.profile_pic = request.FILES.get('profile_pic')
        profile.save()
        messages.success(request, 'profile updated successfully!')
        return redirect('view_profile')
    return render(request, 'profile.html', {'profile':profile})

def update_profile(request):
    profile=profile.objects.get(user=request.user)

    if request.method =='POST':
        phone=request.POST.get('phone')

        if len(phone)!= 10 or not phone.isdigit():
            messages.error(request, "phone number must be exactly 10 digits!")
        else:
            profile.phone=phone
            profile.address=request.POST.get('address')
            if request.FILES.get('profile_pic'):
                profile.profile_pic=request.FILES.get('profile_pic')
            profile.save()
            messages.success(request, "profile updated successfully!")
        return redirect('profile')
        