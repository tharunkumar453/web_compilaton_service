from .DriverCode import PythonDriverCode, CppDriverCode
from .ExecuteCode import ExecuteInPython, ExecuteInCpp


class DriverCodeMiddleware:
    @classmethod
    def DrivercodeLanguage(cls,language):
        if language.lower() == "python":
            return PythonDriverCode()
        elif language.lower() == "cpp":
            return CppDriverCode()
        else:
            raise ValueError(f"Unsupported language: {language}")  
        

class ExecuteCodeFactory:
    @classmethod
    def CodeExecution(cls,language):
        if language.lower()=="python":
            return ExecuteInPython()
        elif language.lower()=="cpp":
            return ExecuteInCpp()
        else:
            raise ValueError(f"Unsupported language: {language}")

        

    