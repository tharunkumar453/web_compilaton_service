from .DriverCode import CDriverCode, PythonDriverCode, CppDriverCode
from .ExecuteCode import ExecuteInPython, ExecuteInCpp, ExecuteInC


class DriverCodeMiddleware:
    @classmethod
    def DrivercodeLanguage(cls,language):
        if language.lower() == "python":
            return PythonDriverCode()
        elif language.lower() == "cpp":
            return CppDriverCode()
        elif language.lower() == "c":
            return CDriverCode()
        else:
            raise ValueError(f"Unsupported language: {language}")  
        

class ExecuteCodeFactory:
    @classmethod
    def CodeExecution(cls,language):
        if language.lower()=="python":
            return ExecuteInPython()
        elif language.lower()=="cpp":
            return ExecuteInCpp()
        elif language.lower()=="c":
            return ExecuteInC()
        else:
            raise ValueError(f"Unsupported language: {language}")

        

    