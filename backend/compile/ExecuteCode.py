import subprocess
import tempfile
import os
from abc import ABC, abstractmethod
from typing import Any

class ExecuteCode(ABC):
    @abstractmethod
    def Execute(self,total_code,file_name) -> dict[str, Any]:
        pass

class ExecuteInPython(ExecuteCode):
    def Execute(self,total_code,file_name):
        with tempfile.TemporaryDirectory()as temp_dir:
            path_dir=os.path.join(temp_dir,file_name)
            with open(path_dir,'w') as code_file_handler:
                code_file_handler.write(total_code)
                code_file_handler.flush()
            code_file_handler.close()
            process_output=subprocess.run(["python",path_dir],
                                          capture_output=True,
                                          text=True,
                                          universal_newlines=True
                                          )
        return{"message":" your code received!!",
               "filename":file_name,"output":process_output.stdout.strip(),
               "errors":process_output.stderr.strip()
               }


class ExecuteInCpp(ExecuteCode):
    def Execute(self,total_code, file_name):
        with tempfile.TemporaryDirectory()as temp_dir:
            path_dir=os.path.join(temp_dir,file_name)+".cpp"
            with open(path_dir,'w') as code_file_handler:
                code_file_handler.write(total_code)
                code_file_handler.flush()
            code_file_handler.close()
            CompiledFileRunCommad=[f"./{file_name}.exe"]
                
            compiled_process_output=subprocess.run(["g++",path_dir,"-o",f'{file_name}.exe'],
                                                   capture_output=True,
                                                   text=True,
                                                   universal_newlines=True
                                                   )
            if(compiled_process_output.returncode!=0):
                return{"message":"Compilation Error",
                       "filename":file_name,
                       "output":"",
                       "errors":compiled_process_output.stderr.strip()
                       }
            run_process_output=subprocess.run(CompiledFileRunCommad,
                                              capture_output=True,
                                              text=True,
                                              universal_newlines=True
                                              )
            return{"message":" your code received!!",
                   "filename":file_name,
                   "output":run_process_output.stdout.strip(),
                   "errors":run_process_output.stderr.strip()
                   } 


                   
                             
     
class CodeExecutionFactory:
    @classmethod
    def get_executor(cls,language):
        if language.lower()=="python":
            return ExecuteInPython()
        elif language.lower()=="cpp":
            return ExecuteInCpp()
        else:
            raise ValueError(f"Unsupported language: {language}")