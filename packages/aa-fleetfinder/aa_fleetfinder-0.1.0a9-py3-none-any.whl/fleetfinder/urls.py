"""
URL config
"""

# Django
from django.urls import path

# AA Fleet Finder
from fleetfinder import views

app_name: str = "fleetfinder"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("create/", views.create_fleet, name="create_fleet"),
    path("save/", views.save_fleet, name="save_fleet"),
    path("join/<int:fleet_id>/", views.join_fleet, name="join_fleet"),
    path("details/<int:fleet_id>/", views.fleet_details, name="fleet_details"),
    path("edit/<int:fleet_id>/", views.edit_fleet, name="edit_fleet"),
    # ajax calls
    path("call/dashboard/", views.ajax_dashboard, name="ajax_dashboard"),
    path(
        "call/details/<int:fleet_id>/",
        views.ajax_fleet_details,
        name="ajax_fleet_details",
    ),
]
