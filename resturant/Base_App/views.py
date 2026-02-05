from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as AuthLoginView
from Base_App.models import BookTable, AboutUs, Feedback, ItemList, Items, Cart
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import View


def add_to_cart(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        item = Items.objects.get(id=item_id)

        cart = request.session.get("cart", {})

        if item_id in cart:
            cart[item_id]["quantity"] += 1
        else:
            cart[item_id] = {
                "name": item.Item_name,
                "price": item.Price,
                "quantity": 1
            }

        request.session["cart"] = cart

        return JsonResponse({"message": f"{item.Item_name} added to cart!"})


def get_cart_items(request):
    cart = request.session.get("cart", {})
    items_list = []
    total_amount = 0

    for item_id, v in cart.items():
        total = v["price"] * v["quantity"]
        total_amount += total
        items_list.append({
            "name": v["name"],
            "price": v["price"],
            "quantity": v["quantity"],
            "total": total
        })

    return JsonResponse({
        "items": items_list,
        "total_amount": total_amount
    })

class LoginView(AuthLoginView):
    template_name = 'login.html'
    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('admin:index')  
        return reverse_lazy('Home')  

def LogoutView(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('Home')  

def SignupView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('Home')
        else:
            messages.error(request, 'Error during signup. Please try again.')
    else:
        form = UserCreationForm()
    return render(request, 'login.html', {'form': form, 'tab': 'signup'})


def HomeView(request):
    items =  Items.objects.all()
    list = ItemList.objects.all()
    review = Feedback.objects.all().order_by('-id')[:5]
    return render(request, 'home.html',{'items': items, 'list': list, 'review': review})


def AboutView(request):
    data = AboutUs.objects.all()
    return render(request, 'about.html',{'data': data})


def MenuView(request):
    items =  Items.objects.all()
    list = ItemList.objects.all()
    return render(request, 'menu.html', {'items': items, 'list': list})


def BookTableView(request):
    if request.method == 'POST':
        name = request.POST.get('user_name')
        email = request.POST.get('user_email')
        phone = request.POST.get('phone_number')
        date = request.POST.get('booking_data')
        guests = request.POST.get('total_person')

        subject = 'Table Booking Confirmation'
        message = f'Thank you {name}! Your table for {guests} guests on {date} is confirmed.'
        from_email = f'{name} <restaurant@example.com>'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, f'Thank you {name}! Your table has been booked.')

        return render(request, 'book_table.html')  

    return render(request, 'book_table.html')


def FeedbackView(request):
    if request.method == 'POST':
        name = request.POST.get('User_name')
        feedback = request.POST.get('Description') 
        rating = request.POST.get('Rating')
        image = request.FILES.get('Selfie')  


        if name != '':
            feedback_data = Feedback(
                User_name=name,
                Description=feedback,
                Rating=rating,
                Image=image  
            )
            feedback_data.save()

            messages.success(request, 'Feedback submitted successfully!')

            return render(request, 'feedback.html', {'success': 'Feedback submitted successfully!'})

    return render(request, 'feedback.html')


class CartPageView(View):
    def get(self, request):
        cart = request.session.get("cart", {})

        cart_items = []
        total_amount = 0

        for item_id, item_data in cart.items():
            item_total = item_data["price"] * item_data["quantity"]
            total_amount += item_total

            cart_items.append({
                "id": item_id,   
                "name": item_data["name"],
                "price": item_data["price"],
                "quantity": item_data["quantity"],
                "total": item_total
            })

        return render(request, "cart.html", {
            "cart_items": cart_items,
            "total_amount": total_amount,
        })


def increase_quantity(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")

        cart = request.session.get("cart", {})

        if item_id in cart:
            cart[item_id]["quantity"] += 1
            request.session["cart"] = cart
            return JsonResponse({"message": "Quantity increased"})

        return JsonResponse({"error": "Item not found"}, status=404)

def decrease_quantity(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")

        cart = request.session.get("cart", {})

        if item_id in cart:
            if cart[item_id]["quantity"] > 1:
                cart[item_id]["quantity"] -= 1
            else:
                del cart[item_id]  

            request.session["cart"] = cart
            return JsonResponse({"message": "Quantity decreased"})

        return JsonResponse({"error": "Item not found"}, status=404)

def delete_cart_item(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")

        cart = request.session.get("cart", {})

        if item_id in cart:
            del cart[item_id]
            request.session["cart"] = cart
            return JsonResponse({"message": "Item removed"})

        return JsonResponse({"error": "Item not found"}, status=404)

def clear_cart(request):
    request.session["cart"] = {}
    return JsonResponse({"message": "Cart cleared"})
