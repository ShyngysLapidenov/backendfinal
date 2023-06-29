from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class City(models.Model):
		id = models.AutoField(primary_key=True)
		name=models.CharField(max_length=100)
		def __str__(self):
					return self.name
		@staticmethod
		def search(query):
				cities = City.objects.filter(name__icontains=query)
				return cities
class Comment(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
class Hotel(models.Model):
		name = models.CharField(max_length=100)
		city = models.ForeignKey(City, on_delete=models.CASCADE)
		address=models.CharField(max_length=100)
		price = models.DecimalField(max_digits=8, decimal_places=0)
		description = models.TextField(max_length=180)
		phone = models.CharField(max_length=20)
		image = models.ImageField(upload_to='shoes/')
		rating = models.DecimalField(max_digits=3, decimal_places=2)
		created_at = models.DateTimeField(auto_now_add=True)
		id=models.AutoField(primary_key=True)
		bookings = models.ManyToManyField(User, through='Booking')
		@staticmethod
		def search(query, city=None, min_price=None, max_price=None):
				hotels = Hotel.objects.filter(name__icontains=query)
				# if city:
				# 	hotels = hotels.filter(city__name__icontains=city)
				# if min_price:
				# 	hotels = hotels.filter(price__gte=min_price)
				# if max_price:
				# 	hotels = hotels.filter(price__lte=max_price)
				return hotels
		def str(self):
			return self.name
		
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    id=models.AutoField(primary_key=True)
    def str(self):
        return f'{self.user.username} Profile'
				
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Hotel, through='CartItem')

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.cart_items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.hotel.price * self.quantity
		
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_guests = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)