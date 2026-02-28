import json
class WriteInFile:
    @staticmethod
    def write_in_file(test_case_file):
        with test_case_file.test_cases.open("r") as json_file:
            testcaseJson=json.load(json_file)
            return testcaseJson
class codefilehandler:
    @staticmethod
    def write_code_in_file(submission_obj):
        with submission_obj.code_file.open("r") as code:
            return code.read()
