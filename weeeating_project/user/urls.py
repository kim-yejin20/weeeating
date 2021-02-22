from django.urls    import path
from .views         import SignUpView, LoginView, SocialLoginView, GoogleInfoView


urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signup/google', GoogleInfoView.as_view()), 
    path('/login', LoginView.as_view()),
    path('/login/social', SocialLoginView.as_view())
]
