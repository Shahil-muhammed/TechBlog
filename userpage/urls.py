from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/<uuid:uid>/', views.blog_detail, name='blog_detail'),
    path('add-comment/<uuid:uid>/', views.add_comment, name='add_comment'),
    path('blogs/load/', views.blog_list_partial, name='blog_list_partial'),
]
