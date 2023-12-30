from django.urls import path
from .views import (PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CommentCreateView,
                    CommentUpdateView, PrivateListView, PrivateDetailView, private_delete_comment_view,
                    private_accept_comment_view)

urlpatterns = [
    path('', PostListView.as_view(), name="home"),
    path('<int:pk>/', PostDetailView.as_view(), name="post"),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name="post_update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post_delete"),
    path('comment/create/parent', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_update'),
    path('private/', PrivateListView.as_view(), name='private'),
    path('private/<int:pk>/', PrivateDetailView.as_view(), name='private_post'),
    path('comment_accept/<int:pk>/', private_accept_comment_view, name='comment_accept'),
    path('comment_delete/<int:pk>/', private_delete_comment_view, name='comment_delete'),
]
