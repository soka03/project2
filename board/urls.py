from django.urls import path
from .views import *
app_name = 'board'

urlpatterns = [
    path('', BoardList.as_view()),
    path('<int:pk>/', BoardDetail.as_view()),
    path('<int:pk>/comment/', CommentPost.as_view()),
    path('<int:post_id>/comment/<int:comment_id>/', CommentDetail.as_view()),
]