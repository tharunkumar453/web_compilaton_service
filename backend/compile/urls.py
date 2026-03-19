from django.templatetags.static import static
from django.urls import path
from .views import submit, UserDashboardView, TotalSubmissions, LeaderBoard,check_status
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path("Submit/", submit.as_view(), name="submit"),
    path("comoile/" submit.as_view(), name="compilation"),
    path("Dashboard/", UserDashboardView.as_view(), name="dashboard-list"),
    path("TotalSubmissions/",TotalSubmissions.as_view(),name="count"),
    path("Leaderboard/", LeaderBoard.as_view(), name="leaderboard"),

    path("Check_status/<str:task_id>/", check_status.as_view(), name="check_status"),
 
   
]

