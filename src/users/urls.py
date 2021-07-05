from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('token/', views.TokenView.as_view()),
    path('token/refresh/', views.RefreshTokenView.as_view()),
    path('token/revoke/', views.RevokeTokenView.as_view())
]
