from django.shortcuts import render
from .models import Postnew
from django.core.paginator import Paginator
from category.models import Category
# Create your views here.
def postnew(request):
    post = Postnew.objects.all().filter(is_available=True)
    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(post, 3)
    paged_postnew = paginator.get_page(page)
    postnew_count = post.count()
    links = Category.objects.all()
    context = {
        'postnews': paged_postnew,
        'postnew_count': postnew_count,
        'links': links,
    }
    return render(request, 'postnew/postnews.html', context)

def postnew_detail(request, postnew_slug=None):
    post = Postnew.objects.get(slug=postnew_slug)
    links = Category.objects.all()
    context = {
        'postnew': post,
        'links': links,
    }
    return render(request, 'postnew/postnew_detail.html', context)
    