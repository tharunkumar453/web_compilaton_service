from django.contrib import admin
from .models import problem_table,UserBoard,submission
admin.site.register(problem_table)
admin.site.register(UserBoard)
admin.site.register(submission)


