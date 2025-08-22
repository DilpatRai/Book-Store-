from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Book

def list_books(request):
    q = request.GET.get("q","")
    books = Book.objects.all()
    if q:
        books = books.filter(Q(title__icontains=q) | Q(author__icontains=q))
    return render(request, "books/list.html", {"books": books, "q": q})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "books/detail.html", {"book": book})
