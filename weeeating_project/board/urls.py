from django.urls import path
from .views import BoardView, BoardDetailView,BoardCommentView

urlpatterns = [
    path('', BoardView.as_view()), #조회,작성 
    path('/<int:board_id>', BoardDetailView.as_view()), #상세페이지 조회
    path('/<int:board_id>/comment', BoardCommentView.as_view())
]
