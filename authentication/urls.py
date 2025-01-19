from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import LoginView, Profile, LogoutView, SignUpView,GoogleLoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login/google/', GoogleLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('token/refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name='token_refresh', ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', Profile.as_view({'get': 'list',
                                      'patch': 'partial_update'}), name='profile'),
]
