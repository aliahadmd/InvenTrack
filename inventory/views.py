# views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Count, Sum, F
from django.http import JsonResponse
from .models import Product, Category, StockMovement
from .forms import ProductForm, StockMovementForm
from django.db.models import Q
from django.contrib.auth.views import LoginView


from .models import CustomUser
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter




class CustomLoginView(LoginView):
    template_name = 'inventory/login.html'

class UserRegistrationView(UserPassesTestMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'inventory/register.html'
    success_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'admin'

class UserListView(UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'inventory/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['admin', 'manager']

def export_products_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="products.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)
    p.drawString(100, 750, "Product Inventory Report")

    y = 700
    for product in Product.objects.all():
        p.drawString(100, y, f"{product.name} - Quantity: {product.stock_quantity}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 750

    p.showPage()
    p.save()
    return response

class ProductListView(LoginRequiredMixin, ListView):
       model = Product
       template_name = 'inventory/product_list.html'
       context_object_name = 'products'
       paginate_by = 10

       def get_queryset(self):
           queryset = super().get_queryset()
           search_query = self.request.GET.get('search')
           category = self.request.GET.get('category')
           min_price = self.request.GET.get('min_price')
           max_price = self.request.GET.get('max_price')
           stock_status = self.request.GET.get('stock_status')
           
           if search_query:
               queryset = queryset.filter(
                   Q(name__icontains=search_query) | 
                   Q(description__icontains=search_query) |
                   Q(sku__icontains=search_query)
               )
           if category:
               queryset = queryset.filter(category_id=category)
           if min_price:
               queryset = queryset.filter(price__gte=min_price)
           if max_price:
               queryset = queryset.filter(price__lte=max_price)
           if stock_status:
               if stock_status == 'low':
                   queryset = queryset.filter(stock_quantity__lte=F('reorder_level'))
               elif stock_status == 'out':
                   queryset = queryset.filter(stock_quantity=0)
           
           return queryset

       def get_context_data(self, **kwargs):
           context = super().get_context_data(**kwargs)
           context['categories'] = Category.objects.all()
           return context

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'inventory/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product-list')

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product-list')

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'inventory/product_confirm_delete.html'
    success_url = reverse_lazy('product-list')

    def test_func(self):
        return self.request.user.has_perm('inventory.delete_product')

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Data for the chart
        categories = Category.objects.annotate(product_count=Count('product'))
        context['chart_labels'] = [category.name for category in categories]
        context['chart_data'] = [category.product_count for category in categories]
        
        # Other dashboard data
        context['low_stock_products'] = Product.objects.filter(stock_quantity__lte=F('reorder_level'))
        context['total_products'] = Product.objects.count()
        context['total_stock_value'] = Product.objects.aggregate(
            total_value=Sum(F('stock_quantity') * F('price'))
        )['total_value']
        context['recent_movements'] = StockMovement.objects.order_by('-timestamp')[:5]
        
        return context

class StockMovementCreateView(LoginRequiredMixin, CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = 'inventory/stock_movement_form.html'
    success_url = reverse_lazy('product-list')

def get_stock_updates(request):
    last_update = request.GET.get('last_update')
    products = Product.objects.filter(updated_at__gt=last_update)
    data = [{
        'id': p.id,
        'name': p.name,
        'stock_quantity': p.stock_quantity,
        'updated_at': p.updated_at.isoformat()
    } for p in products]
    return JsonResponse(data, safe=False)