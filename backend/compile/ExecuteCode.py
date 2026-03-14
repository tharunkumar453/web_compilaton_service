import subprocess
import tempfile
import os
import json
from abc import ABC, abstractmethod
from typing import Any

_TESTCASES_FILENAME = "testcases.json"

def write_testcases_json(temp_dir: str, test_cases: dict, filename: str = _TESTCASES_FILENAME) -> str:
    """Write test_cases dict as JSON into temp_dir and return the file path."""
    json_path = os.path.join(temp_dir, filename)
    with open(json_path, "w") as f:
        json.dump(test_cases, f)
    return json_path

class ExecuteCode(ABC):
    @abstractmethod
    def Execute(self,total_code,file_name,test_cases=None) -> dict[str, Any]:
        pass

class ExecuteInPython(ExecuteCode):
    def Execute(self,total_code,file_name,test_cases=None):
        with tempfile.TemporaryDirectory()as temp_dir:
            if test_cases is not None:
                write_testcases_json(temp_dir, test_cases)
            path_dir=os.path.join(temp_dir,file_name)
            with open(path_dir,'w') as code_file_handler:
                code_file_handler.write(total_code)
                code_file_handler.flush()
            code_file_handler.close()
            process_output=subprocess.run(["python",path_dir],
                                          capture_output=True,
                                          text=True,
                                          universal_newlines=True,
                                          cwd=temp_dir
                                          )
        return{"message":" your code received!!",
               "filename":file_name,"output":process_output.stdout.strip(),
               "errors":process_output.stderr.strip()
               }


class ExecuteInCpp(ExecuteCode):
    def Execute(self,total_code, file_name,test_cases=None):
        with tempfile.TemporaryDirectory()as temp_dir:
            if test_cases is not None:
                write_testcases_json(temp_dir, test_cases)
            src_path=os.path.join(temp_dir,file_name)+".cpp"
            exe_path=os.path.join(temp_dir,file_name)+".exe"
            with open(src_path,'w') as code_file_handler:
                code_file_handler.write(total_code)
                code_file_handler.flush()
            code_file_handler.close()
                
            compiled_process_output=subprocess.run(["g++",src_path,"-o",exe_path],
                                                   capture_output=True,
                                                   text=True,
                                                   universal_newlines=True,
                                                   cwd=temp_dir
                                                   )
            if(compiled_process_output.returncode!=0):
                return{"message":"Compilation Error",
                       "filename":file_name,
                       "output":"",
                       "errors":compiled_process_output.stderr.strip()
                       }
            run_process_output=subprocess.run([exe_path],
                                              capture_output=True,
                                              text=True,
                                              universal_newlines=True,
                                              cwd=temp_dir
                                              )
            return{"message":" your code received!!",
                   "filename":file_name,
                   "output":run_process_output.stdout.strip(),
                   "errors":run_process_output.stderr.strip()
                   } 
        
        
class ExecuteInC(ExecuteCode):
    def Execute(self,total_code, file_name,test_cases=None):
        with tempfile.TemporaryDirectory()as temp_dir:
            src_path=os.path.join(temp_dir,file_name)+".c"
            exe_path=os.path.join(temp_dir,file_name)+".exe"
            with open(src_path,'w') as code_file_handler:
                code_file_handler.write(total_code)
                code_file_handler.flush()
            code_file_handler.close()
                
            compiled_process_output=subprocess.run(["gcc",src_path,"-o",exe_path],
                                                   capture_output=True,
                                                   text=True,
                                                   universal_newlines=True,
                                                   cwd=temp_dir
                                                   )
            if(compiled_process_output.returncode!=0):
                return{"message":"Compilation Error",
                       "filename":file_name,
                       "output":"",
                       "errors":compiled_process_output.stderr.strip()
                       }
            run_process_output=subprocess.run([exe_path],
                                              capture_output=True,
                                              text=True,
                                              universal_newlines=True,
                                              cwd=temp_dir
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
        elif language.lower()=="c":
            return ExecuteInC()
        else:
            raise ValueError(f"Unsupported language: {language}")