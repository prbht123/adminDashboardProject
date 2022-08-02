from django.urls import path
from . import views

app_name = 'jobPortalApp'

urlpatterns = [
    path('', views.homejob, name="homejob"),
    path('userjobsprofile/', views.jobUserProfileListView.as_view(),
         name="user_job_profile"),
    path('userprofilejobcreate', views.jobUserProfileCreateView.as_view(),
         name="user_profile_job_create"),
    path('userprofilejobupdate/<slug:slug>', views.jobUserProfileUpdateView.as_view(),
         name="user_profile_job_update"),
    path('userjobsprofiledelete/<slug:slug>/', views.jobUserProfileDeleteView.as_view(),
         name="user_job_profile_delete"),
    path('userjobskillcreate', views.jobUserSkillCreateView.as_view(),
         name="user_skill_job_create"),
    path('userjobskilldelete/<slug:slug>/', views.jobUserSkillDeleteView.as_view(),
         name="user_skill_job_delete"),
    path('jobcreate', views.jobCreateView.as_view(),
         name="job_create"),
    path('joblist/', views.jobListView.as_view(),
         name="job_list"),
    path('jobupdate/<slug:slug>', views.jobUpdateView.as_view(),
         name="job_update"),
    path('jobdelete/<slug:slug>/', views.jobDeleteView.as_view(),
         name="job_delete"),
    path('jobapply/<slug:slug>', views.jobAppliedCreateView,
         name="job_apply"),
    path('jobappliedusers/<slug:slug>', views.jobAppliedUsersListView.as_view(),
         name="job_applied_users"),
    path('jobsapplieduser/', views.jobAppliedByUserListView.as_view(),
         name="job_applied_by_user"),
]
