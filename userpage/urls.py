from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('library/', views.index, name='library'), 
    path('library/blog/<uuid:uid>/', views.blog_detail, name='blog_detail'),
    path('library/add-comment/<uuid:uid>/', views.add_comment, name='add_comment'),
    path('library/blogs/load/', views.blog_list_partial, name='blog_list_partial'),
]
