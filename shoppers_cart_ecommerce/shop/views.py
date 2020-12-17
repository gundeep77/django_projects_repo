from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from math import ceil
from django.contrib import messages


def index(request):
    allProds = []
    catProds = Product.objects.values('category')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n//3 + ceil((n/3) - (n//3))
        allProds.append([prod, range(1, nslides)])
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def search(request):
    allProds_query = []
    query = request.GET.get('query')
    params_noresult = {'query': query, 'lengthy_query': query}
    if len(query) > 20:
        messages.warning(request, "Invalid Request!")
        return render(request, 'shop/noresult.html', params_noresult)
    prodNames_query = Product.objects.filter(product_name__icontains=query)
    prodCats_query = Product.objects.filter(category__icontains=query)
    prodSubcats_query = Product.objects.filter(subcategory__icontains=query)
    prodNames_combined = prodNames_query.union(prodCats_query, prodSubcats_query)
    n = len(prodNames_combined)
    if n == 0:
        messages.warning(request, "Invalid Request!")
        return render(request, 'shop/noresult.html', params_noresult)
    nslides = n//3 + ceil((n/3) - (n//3))
    allProds_query.append([prodNames_combined, range(1, nslides), query])
    params = {'allProds_query': allProds_query}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contacts(request):
    return HttpResponse("We are at contacts")


def tracker(request):
    return HttpResponse("We are at tracker")


def productView(request):
    return HttpResponse("We are at prodView")


def checkout(request):
    return HttpResponse("We are at checkout")
