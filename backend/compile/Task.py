from typing import Any

from celery import shared_task
from .MiiddleWare import DriverCodeMiddleware,ExecuteCodeFactory
from .models import UserBoard
from .workers import WriteInFile,codefilehandler
from .models import submission,problem_table,UserBoard
from .ExecuteCode import _TESTCASES_FILENAME
from django.core.cache import cache
class ExecutionHandler:
    def handle_execution(self,email,problem_id,language,user_codefile_id,name):

        submission_obj = submission.objects.get(submission_id=user_codefile_id)
        problem_obj = problem_table.objects.get(problem_id=problem_id)
        testcases = WriteInFile.write_in_file(problem_obj)
        code_content = codefilehandler.write_code_in_file(submission_obj)
    

        driver_code_instance=DriverCodeMiddleware.DrivercodeLanguage(language)
        Combined_code=driver_code_instance.DriverCodeGenerator(code_content,testcases,_TESTCASES_FILENAME)
        print("Combined code is ",Combined_code)
        ExecutioncodeInstance=ExecuteCodeFactory.CodeExecution(language)
        code_output=ExecutioncodeInstance.Execute(Combined_code,name,testcases)

        has_done=True if code_output["output"]=="Accepted" else False
        if has_done:
            cache.delete("leaderboard_data")
            cache.delete(f"user_dashboard:{email}")
        UserBoard.objects.create(
        email=email,
        problem_id=problem_id,
        has_done=has_done,
        language_used=language
        )
        return {"output": code_output["output"],
                "errors": code_output["errors"]
                }


   
@shared_task
def execute_code_task(email,problemid,language,user_codefile_id,name) ->Any:
    execution_handler=ExecutionHandler().handle_execution(email,problemid,language,user_codefile_id,name)
    return execution_handler 

