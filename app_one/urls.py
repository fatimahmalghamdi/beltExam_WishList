from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.mainPage),
    path('registeration', views.registeration),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboardPage),
    path('wish_items/create', views.wish_items_create),
    path('delete/<int:product_id>', views.deleteItem),
    path('removeItem/<int:product_id>', views.removeItem),
    path('add_to_list/<int:product_id>', views.add_to_list),
    path('wish_items/<int:product_id>', views.display_item_users)
]