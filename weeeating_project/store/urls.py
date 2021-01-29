from django.urls import path
from .views import StoreListView, StoreDetailView, LikeStoreView

urlpatterns = [
    path('/list', StoreListView.as_view()),
    path('/like/<int:store_id>', LikeStoreView.as_view()),
    path('/detail/<int:store_id>', StoreDetailView.as_view())
]
