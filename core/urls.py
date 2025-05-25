from django.urls import path
from django.conf import settings
from . import views
from core.views import custom_404_dev  # adjust if your view is elsewhere

if settings.DEBUG:
    handler404 = custom_404_dev

urlpatterns = [
    path('', views.student_dashboard, name='student_dashboard'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('profile/', views.student_profile, name='student_profile'),
    path('vote/<int:election_id>/', views.vote_page, name='vote_page'),
    path('voting results/', views.voting_results, name='vote_results'),
    path('votes/<int:candidate_id>/', views.vote_details, name='vote_details'),
    path('export-votes/csv/<int:candidate_id>/',views.export_votes_csv, name='export_votes_csv'),
    path('export-votes/pdf/<int:candidate_id>/',views.export_votes_pdf, name='export_votes_pdf'),
    path('already-voted/<int:election_id>/',views.already_voted, name='already_voted'),
    path('election/<int:election_id>/thank_you/',views.thank_you, name='thank_you'),
    path('admin/', views.admin_dashboard, name='admin_page'),
]
