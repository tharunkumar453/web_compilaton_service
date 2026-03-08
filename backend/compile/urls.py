from django.templatetags.static import static
from django.urls import path
from .views import submit, UserDashboardView, TotalSubmissions, LeaderBoard,check_status
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path("submit/", submit.as_view(), name="submit"),
    path("dashboard/", UserDashboardView.as_view(), name="dashboard-list"),
    path("total/",TotalSubmissions.as_view(),name="count"),
    path("Leaderboard/", LeaderBoard.as_view(), name="leaderboard"),

    path("check_status/<str:task_id>/", check_status.as_view(), name="check_status"),
 
   
]

