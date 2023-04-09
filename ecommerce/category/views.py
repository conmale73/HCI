from django.shortcuts import render
from category.models import Category

def btn_category(request):
    links = Category.objects.all()
    context = {
        'links': links,
    }
    return render(request, 'base.html', context)