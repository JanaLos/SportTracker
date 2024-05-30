from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
# from .views import ActivityListView, ActivityDetailView, ActivityCreate, ActivityUpdate, ActivityDelete, PostDeleteView


activities_patterns = ([
    path('', ActivityListView.as_view(), name='list'),
    path('<int:pk>/<slug:slug>/', ActivityDetailView.as_view(), name='detail'),
    path('create/', ActivityCreate.as_view(), name='create'),
    path('update/<int:pk>', ActivityUpdate.as_view(), name='update'),
    path('delete/<int:pk>', ActivityDelete.as_view(), name='delete'),
    path('register/', register, name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('post/new/', PostCreateView.as_view(), name='post-create'),
    # path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
], 'activities')