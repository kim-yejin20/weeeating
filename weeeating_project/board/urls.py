from django.urls import path
from .views import BoardView, BoardDetailView

urlpatterns = [
    path('', BoardView.as_view()), #조회,작성 
    path('/detail/<int:board_id>', BoardDetailView.as_view()) #상세페이지 조회
]
