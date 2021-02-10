from django.urls import path, include
# from users.views import dashboard, register
from . import views


urlpatterns = [
    path('login/', views.user_login, name='login'),
    # path('accounts/', include("django.contrib.auth.urls")),
    # path('dashboard/', dashboard, name="dashboard"),
    # path('oauth/', include("social_django.urls")),
    # path('register/', register, name="register"),
]

