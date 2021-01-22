from django.urls    import path
from .views         import SignUpView, LoginView, SocialLoginView


urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/login', LoginView.as_view()),
    path('/login/social', SocialLoginView.as_view())
]
