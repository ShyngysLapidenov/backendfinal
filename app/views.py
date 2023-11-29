from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sigin')
    else:
        form = RegistrationForm()
    return render(request, 'registr.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('signin')
    else:
        return render(request, 'signin.html')


def logout(request):
    auth.logout(request)
    return redirect('')


def index(request):
    hotels = Hotel.objects.all()
    context = {
        'hotels': hotels
    }
    return render(request, 'index.html', context)


def add_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = HotelForm()
    return render(request, 'add_hotel.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


@login_required
def profile_edit(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = EditUserForm(instance=user)
        profile_form = EditProfileForm(instance=profile)
    return render(request, 'profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})


def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    comments = Comment.objects.filter(hotel=hotel)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.hotel = hotel
            comment.user = request.user
            comment.save()
            form = CommentForm()  # Create a new form for the next comment submission
    else:
        form = CommentForm()

    context = {'hotel': hotel, 'comments': comments, 'form': form}
    return render(request, 'hotel_detail.html', context)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        if request.method == 'POST':
            comment.delete()
    return redirect('detail', pk=comment.hotel.id)


def delete_hotel(request, pk):
    myobject = get_object_or_404(Hotel, pk=pk)
    myobject.delete()
    return redirect('')


def update_hotel(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        form = HotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = HotelForm(instance=hotel)
    return render(request, 'update.html', {'form': form})


def search_hotel(request):
    hotel_name = request.GET.get('hotel_name')
    city_name = request.GET.get('city_name')

    hotels = Hotel.objects.all()

    if hotel_name:
        hotels = hotels.filter(name__icontains=hotel_name)

    if city_name:
        hotels = hotels.filter(city__name__icontains=city_name)

    context = {'hotels': hotels, 'hotel_name': hotel_name, 'city_name': city_name}
    return render(request, 'search_hotel.html', context)


@login_required
def book_hotel(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            num_guests = form.cleaned_data['num_guests']

            # Create a new instance of Booking with the user
            booking = Booking(hotel=hotel, user=request.user, check_in_date=check_in_date,
                              check_out_date=check_out_date, num_guests=num_guests)
            booking.save()

            # Redirect to a success page or display a success message
            return redirect('booking_list')  # Replace 'success' with the appropriate URL name
    else:
        form = BookingForm()

    return render(request, 'book_hotel.html', {'form': form, 'hotel': hotel})


def booking_list(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user)
        return render(request, 'bookings.html', {'bookings': bookings})
    else:
        return redirect('login')


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    return redirect('booking_list')


@login_required
def add_to_cart(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, hotel=hotel)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


@login_required
def remove_from_cart(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, hotel=hotel)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


@login_required
def cart(request):
    cart = Cart.objects.get(user=request.user)
    context = {'cart': cart}
    return render(request, 'basket.html', context)
