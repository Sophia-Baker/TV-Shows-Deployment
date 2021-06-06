from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    path('dashboard', views.dashboard),
    path('new', views.new),
    path('create', views.create),
    path('<int:show_id>', views.summary),
    path('<int:show_id>/edit', views.edit),
    path('<int:show_id>/update', views.update),
    path('<int:show_id>/delete', views.delete)
]