from django.urls import path 
from .views import views


urlpatterns = [
    path('', views.main, name='main_menu'),
    path('create_order/', views.create_order, name='create_order'),
    path('get_all_orders/', views.get_all_orders, name='all_orders'),
    path('search_order/', views.search_order, name='search_order'),
    path('edit_order/', views.render_order_for_edit, name='edit_order'),
    path('edit_order_status/', views.edit_order_status, name='edit_order_status'),
    path('delete_order/', views.render_delete_order_item, name='render_delete_order_item'),
    path('delete_order_page/', views.delete_order, name='delete_order'),
    path("get_revenue/", views.get_revenue, name="get_revenue"),
]
