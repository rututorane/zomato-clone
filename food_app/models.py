from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    description=models.TextField()
    image=models.ImageField(upload_to='food_images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_veg= models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    item=models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    added_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.item.name}"

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    item=models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.user.username} - {self.item.name} ({self.quantity})"

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    total_bill =models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
    def __str__(self):
        return f"order {self.id} by {self.user.username}"

class Review(models.Model):
    food_item = models.ForeignKey('FoodItem', on_delete=models.CASCADE, related_name='reviews')
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    rating=models.IntegerField(choices=[(i,i) for i in range(1,6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - ({ self.rating}⭐)"

class Coupon(models.Model):
    code=models.CharField(max_length=20,unique=True)
    discount_amount=models.IntegerField()
    active=models.BooleanField(default=True)
    def __str__(self):
        return self.code

class Rating(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def remaining_stars(self):
        return 5 - self.rating

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_pic = models. ImageField(upload_to='profiles/', blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender,instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()