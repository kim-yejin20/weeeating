from django.urls import path
from .views import StoreListView, StoreDetailView, LikeStoreView, StoreCommentView

urlpatterns = [
    path('/list', StoreListView.as_view()),
    path('/like/<int:store_id>', LikeStoreView.as_view()),
    path('/detail/<int:store_id>', StoreDetailView.as_view()), # 상세페이지 조회(댓글포함) 
    path('/detail/<int:store_id>/comment', StoreCommentView.as_view()), # 댓글 생성,조회
    path('/detail/<int:store_id>/<int:comment_id>', StoreCommentView.as_view()) #댓글 삭제, 수정 
]
