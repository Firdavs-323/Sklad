from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'quantity']
    search_fields = ['name', 'sku', 'barcode']
    ordering_fields = ['name', 'price', 'quantity']

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import CategoryForm, ProductForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

@login_required
def edit_category(request, pk):
    if not request.user.is_superuser:
        profile = getattr(request.user, 'profile', None)
        if not profile or profile.role != 'admin':
            return redirect('category_list')
            
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategoriya muvaffaqiyatli tahrirlandi.')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'products/edit_category.html', {'form': form, 'category': category})

@login_required
def edit_product(request, pk):
    if not request.user.is_superuser:
        profile = getattr(request.user, 'profile', None)
        if not profile or profile.role != 'admin':
            return redirect('product_list')
            
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mahsulot muvaffaqiyatli tahrirlandi.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form, 'product': product})

@login_required
def delete_category(request, pk):
    if not request.user.is_superuser:
        profile = getattr(request.user, 'profile', None)
        if not profile or profile.role != 'admin':
            return redirect('category_list')
            
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Kategoriya muvaffaqiyatli o\'chirildi.')
        return redirect('category_list')
    return render(request, 'products/delete_category.html', {'category': category})

@login_required
def delete_product(request, pk):
    if not request.user.is_superuser:
        profile = getattr(request.user, 'profile', None)
        if not profile or profile.role != 'admin':
            return redirect('product_list')
            
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Mahsulot muvaffaqiyatli o\'chirildi.')
        return redirect('product_list')
    return render(request, 'products/delete_product.html', {'product': product})
