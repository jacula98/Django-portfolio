from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<str:pk>', views.profilePage, name='profile'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('createcard/', views.create_card, name='createcard'),
    path('confirm_delete/<int:card_id>/', views.confirm_delete_card_page, name='confirm_delete_card'),
    path('delete/<int:card_id>/', views.delete_card, name='delete_card'),
    path('subscribe/<int:card_id>/', views.subscribe_to_card, name='subscribe'),
    path('unsubscribe/<int:card_id>/', views.unsubscribe_from_card, name='unsubscribe'),
    path('user_subscriptions/', views.user_subscriptions, name='user_subscriptions'),
]

handler404 = 'accounts.views.error_404_view'