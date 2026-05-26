from django.contrib import admin

# Register your models here.
from .models import Category, FoodItem, Wishlist, Order
from.models import Review
from .models import Coupon
from .models import Profile

admin.site.register(Category)
admin.site.register(FoodItem)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Coupon)
admin.site.register(Profile)

