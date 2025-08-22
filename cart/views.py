from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import CartItem
from books.models import Book

@login_required
def view_cart(request):
    items = CartItem.objects.filter(user=request.user).select_related("book")
    subtotal = sum(i.line_total() for i in items)
    return render(request, "cart/cart.html", {"items": items, "subtotal": subtotal})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    item, created = CartItem.objects.get_or_create(user=request.user, book=book)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f"Added {book.title} to cart.")
    return redirect("book_detail", pk=book_id)

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.info(request, "Removed item from cart.")
    return redirect("view_cart")
