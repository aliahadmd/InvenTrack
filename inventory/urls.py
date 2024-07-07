from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('stock-movement/create/', views.StockMovementCreateView.as_view(), name='stock-movement-create'),
    path('api/stock-updates/', views.get_stock_updates, name='stock-updates'),
    path('accounts/login/', views.CustomLoginView.as_view(next_page='dashboard'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='dashboard'), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('export-pdf/', views.export_products_pdf, name='export-pdf'),
]