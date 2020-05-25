from django.urls import path
from loginmodule.views import auth_view
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.conf.urls.static import static
from .views import *

urlpatterns = [
	path('auth', auth_view),
	path('do_register/', doRegister),
	path('register/', register)
]
