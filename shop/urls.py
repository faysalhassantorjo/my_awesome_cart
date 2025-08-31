from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Homepage
    path("", views.index, name="ShopHome"),

    # Auth
    path("login/", views.login_view, name="login_view"),
    path("register/", views.signup_view, name="signup_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("profile/", views.profile, name="profile"),

    # Product
    


    path('buy/<int:product_id>/', views.buy_view, name='buy_view'),
    path('checkout/<int:order_id>/', views.checkout_view, name='checkout'),



    
    
    path('apply-coupon/', views.apply_coupon, name='apply-coupon'),

    # Cart
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Suggestion
    path('suggestions/', views.suggestion_page, name='suggestion_page'),
    path('suggestion/edit/<int:pk>/', views.edit_suggestion, name='edit_suggestion'),
    path('suggestion/delete/<int:pk>/', views.delete_suggestion, name='delete_suggestion'),

    # Test / Middleware route
    path('middle/', views.middleware),

    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('product_page/<int:product_id>/', views.product_details, name='product_details'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
