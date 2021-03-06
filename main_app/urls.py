from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path("register", views.register),
    path("login", views.login),	 
    path("dashboard", views.dashboard),
    path("logout", views.logout),
    path("business/new", views.new_bus),
    path("business/process", views.process_bus),
    path("business/<int:bus_id>", views.business),
    path("business/edit/<int:bus_id>", views.edit_bus),
    path("business/update/<int:bus_id>", views.update_bus),
    path("business/delete/<int:bus_id>", views.delete_bus),
    path("organization/new", views.new_org),
    path("organization/process", views.process_org),
    path("organization/<int:org_id>", views.organization),
    path("organization/edit/<int:org_id>", views.edit_org),
    path("organization/update/<int:org_id>", views.update_org),
    path("organization/delete/<int:org_id>", views.delete_org),
    path("browse/listings", views.browse),
    path("user/<int:user_id>", views.user),


]