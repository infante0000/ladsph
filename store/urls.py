from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('menu/', views.menu, name="menu"),
    path('about/', views.about, name="about_us"),
    path('contact/', views.contact, name="contact_us"),

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name='logout'),
]
