
from django.urls import path , include
from .views import *

urlpatterns = [
    path('question', questions_view, name="question"),
    path('question/<int:id>/', question_detail, name='question_detail_view'),
    path('questions/<int:question_id>/choices/', choices_view, name='choices_view'),
    path('questions/<int:question_id>/vote/', vote_view, name='vote_view'),
    path('questions/<int:question_id>/result/', question_result_view, name='question_result_view')

]
