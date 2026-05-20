from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import LoginView, SignUpView, MeView, CheckEmailView, CheckDocumentView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('me/', MeView.as_view(), name='me'),
    path("check-email/", CheckEmailView.as_view(), name="check-email"),
    path("check-document/", CheckDocumentView.as_view(), name="check-document"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
]
