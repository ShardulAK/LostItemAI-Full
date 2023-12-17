
from django.urls import path


from . import views

# app_name = 'main'

"""
when requested to particural view it calls a function from views.py eg 'found/' calls found fun defined in views.py
"""
urlpatterns = [
    path('', views.home, name='home'),
    path('found/', views.found, name='found'),
    path('lost/', views.lost, name='lost'),
    path('login/',  views.user_login, name='login'),
    path('logout/',  views.logout, name='logout'),
    path('register/', views.register, name='register'),
]

