from django.urls import path
from .views import BoardMainView, BoardPostView

urlpatterns = [
    path('', BoardMainView.as_view()),
    path('/posts', BoardPostView.as_view())
]
