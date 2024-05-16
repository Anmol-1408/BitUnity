from django.urls import path
from .import views

urlpatterns = [
    path("",views.landing,name = 'landing'),
    path("login/",views.userLogin,name = 'login'),
    path("signup/",views.signup,name = 'signup'),
    path('logout/', views.userLogout, name="logout"),
]