from django.urls import path
from .import views
# from .views import PostEditView

urlpatterns = [
    path("",views.projectList,name = 'project-list'),
    path("create/",views.createProject,name = 'create-project'),
    path("project-detail/<int:pk>/",views.projectDetail,name = 'project-detail'),
    path("edit/<int:pk>/",views.projectEdit,name = 'project-edit'),
    path('delete/<int:pk>/', views.projectDelete, name='project-delete'),
    path('comment/delete/<int:pk>/', views.commentDelete, name='comment-delete'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    
    path('profile/<int:pk>/edit/', views.profileEdit, name='profile-edit'),
    path('profile/<int:pk>/followers/add', views.addFollower, name='add-follower'),
    path('profile/<int:pk>/followers/remove', views.removeFollower, name='remove-follower'),
    path('project/<int:pk>/like/', views.addLike, name='add-like'),
    
    path('search/', views.search, name="search"),
]