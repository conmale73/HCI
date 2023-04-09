from django.shortcuts import render
from store.models import Product
from category.models import Category
from postnew.models import Postnew

def home(request):
    products = Product.objects.all().filter(is_available=True)
    post = Postnew.objects.all().filter(is_available=True)
    links = Category.objects.all()
    context = {
        'products': products,
        'links': links,
        'postnew': post,
    }
    return render(request, 'home.html', context=context)
