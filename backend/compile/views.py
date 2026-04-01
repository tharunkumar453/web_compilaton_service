from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import uuid
from .models import problem_table,UserBoard,submission
from .serializers import UserDashboardSerializer    
from django.db.models import Count,Max
from django.core.cache import cache
from celery.result import AsyncResult
from .Task import execute_code_task
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.parsers import FormParser,MultiPartParser       

class submit(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser,MultiPartParser]

    def post(self, request):
        user_email=request.user.email
        name=request.data.get("name")
        user_codefile=request.FILES["file"]
        problem_id=request.data.get("problem_id")
        language=request.data.get("language")
        is_private=request.data.get("is_private", False)
        has_problem_in_cache = cache.get(f"problem_id:{problem_id}")

        if has_problem_in_cache:test_case_file=has_problem_in_cache
        else:
            test_case_file=problem_table.objects.get(problem_id=problem_id)
            cache.set(f"problem_id:{problem_id}", test_case_file, timeout=30*30)  
        
            
        if is_private:
            has_previously_correct=UserBoard.objects.filter(email=user_email,problem=test_case_file,has_done=True)
            if has_previously_correct.exists():
                return Response("you alredy submitt this oone correctluy this submission not ")


        user_codefile=submission.objects.create(
            email=user_email,
            submission_id=str(uuid.uuid4()),
            problem=test_case_file,
            language_used=language,
            code_file=user_codefile
        )

        
        retrun_code_output=execute_code_task.delay(user_email,
                          test_case_file.problem_id,
                          language,
                          user_codefile.submission_id,
                          name,
                          is_private)



        return Response({
            "task_id":retrun_code_output.id, 
            "status":retrun_code_output.status,
            "submission_id":user_codefile.submission_id
        })  


# User Dashboard APIs
class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]
   
    def get(self, request):
        user_email = request.user.email
        if not user_email:
            return Response({"detail": "please Register"}, status=status.HTTP_400_BAD_REQUEST)

        if not cache.get(f"user_dashboard:{user_email}"):
            user = UserBoard.objects.filter(email=user_email,has_done=True)
            serializer = UserDashboardSerializer(user,many=True)
            data=serializer.data
            cache.set(f"user_dashboard:{user_email}", data, timeout=30*60)  # Cache for 30 minutes
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(cache.get(f"user_dashboard:{user_email}"), status=status.HTTP_200_OK)
 

class TotalSubmissions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user_email=request.user.email
        if not user_email:
            return Response({"detail": "please Register"}, status=status.HTTP_400_BAD_REQUEST)
        count=UserBoard.objects.filter(email=user_email).count()
        return Response(count,status=status.HTTP_200_OK)
    

class LeaderBoard(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
            leaderboard = list(UserBoard.objects.filter(has_done=True).values('email').annotate(solved=Count('problem', distinct=True),last_sumbission=Max(('time_of_submission'))).order_by('-solved','last_sumbission'))
    
            return Response(leaderboard, status=status.HTTP_200_OK)


class check_status(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, task_id):
        try:
            status_result = AsyncResult(task_id)
            return Response({
                "status": status_result.status,
                "result": status_result.result if status_result.status == 'SUCCESS' else None,
            })
        except Exception as exc:
            return Response(
               {"detail": "please check the code. compile and submit again", "error": str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

