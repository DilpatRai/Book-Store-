from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import Order, OrderItem
from cart.models import CartItem

@login_required
@transaction.atomic
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related("book")
    if not cart_items.exists():
        messages.info(request, "Your cart is empty.")
        return redirect("view_cart")

    order = Order.objects.create(user=request.user)
    total = 0
    for ci in cart_items:
        OrderItem.objects.create(
            order=order, book=ci.book, quantity=ci.quantity, price=ci.book.price
        )
        total += ci.quantity * ci.book.price
    order.total = total
    order.save()
    cart_items.delete()
    messages.success(request, f"Order placed! Total: {total}")
    return redirect("order_history")

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items__book")
    return render(request, "orders/history.html", {"orders": orders})

