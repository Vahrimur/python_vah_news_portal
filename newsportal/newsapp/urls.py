from django.urls import path
from .views import PostsList, PostDetail, PostsSearch, NWCreate, NWUpdate, NWDelete, ARCreate, ARUpdate, ARDelete, \
    author_now

urlpatterns = [
    # Путь '' - для работы со всеми постами: новостями и статьями
    path('', PostsList.as_view(), name='posts_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search', PostsSearch.as_view(), name='posts_search'),
    # Путь 'news/' - для работы только с новостями
    path('news/create/', NWCreate.as_view(), name='nw_create'),
    path('news/<int:pk>/update/', NWUpdate.as_view(), name='nw_update'),
    path('news/<int:pk>/delete/', NWDelete.as_view(), name='nw_delete'),
    # Путь 'articles/' - для работы только со статьями
    path('articles/create/', ARCreate.as_view(), name='ar_create'),
    path('articles/<int:pk>/update/', ARUpdate.as_view(), name='ar_update'),
    path('articles/<int:pk>/delete/', ARDelete.as_view(), name='ar_delete'),
    path('author_now/', author_now, name='author_now'),
]
