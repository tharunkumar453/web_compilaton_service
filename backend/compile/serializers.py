from rest_framework import serializers
from .models import problem_table,UserBoard


class ProblemTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = problem_table
        fields = ['problem_id']


class UserDashboardSerializer(serializers.ModelSerializer):
  
   
    class Meta:
        model = UserBoard
        fields = ['email', 'problem_id', 'language_used', 'time_of_submission']
        read_only_fields = ['email', 'problem_id', 'language_used', 'time_of_submission']