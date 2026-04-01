from abc import ABC, abstractmethod
import json

# total code combiner to combine user code with driver code
class TotalCodeCombiner:
    @staticmethod
    def combineUsercodewithDriverCode(user_code,Driver_code):
        x=f'''
{user_code}  
{Driver_code}
'''     
        print(x) # for debugging
        return x
    

class DriverCode(ABC): 
    @abstractmethod
    def DriverCodeGenerator(self,file,test_casess,is_private) -> str:
        pass



    
 # Driver code for python   
class PythonDriverCode(DriverCode):
    def DriverCodeGenerator(self,file,test_casess,is_private):
        inputs=[tc["input"] for tc in test_casess[ "private_cases" if is_private else "public_cases"]]
        ans=[tc["output"] for tc in test_casess[ "private_cases" if is_private else "public_cases"]]
        method=test_casess["method_name"]
        if is_private:
            verify_code='''
        if(out!=exp):
            print("error at test case",i+1)
            return
    print("Accepted")
'''     
        else:
            verify_code='''
        print(f"Test case {i+1}: Output: {out}, Expected: {exp}") 
        if(out!=exp): 
            print("error at test case",i+1)
            return
'''
        driver_code=f'''
def parse(x):
    if isinstance(x,list):
        return[parse(v) for v in x]
    if isinstance(x,dict):
        return {{ k: parse(v) for k,v in x.items()}}
    return x
def driver_code():
    a=Solution()
    func=getattr(a,'{method}')
    for  i,(x,y) in enumerate(zip{inputs,ans}):
        args=parse(x)
        out=func(*args)
        exp=parse(y)
        {verify_code}
driver_code()
'''   
        return TotalCodeCombiner.combineUsercodewithDriverCode(file,driver_code)
        
# Driver code for C++
class CppDriverCode(DriverCode):

    def DriverCodeGenerator(self, file, test_casess, is_private):

        dump_json = json.dumps(test_casess, indent=2)

        argument_declarations = []
        argument_names = []

        cases_key = "private_cases" if is_private else "public_cases"

        if is_private:
            verify_code = '''
        if (output != expected) {
            cout << "Error at test case " << i + 1 << endl;
            return;
        }
'''
        else:
            verify_code = '''
        cout << "Test case " << i + 1 << ": Output: " << output << ", Expected: " << expected << endl;
        if (output != expected) {
            cout << "Error at test case " << i + 1 << endl;
            return;
        }
'''

        for i, type in enumerate(test_casess["signature"]):
            argument_declarations.append(
                f'{type} arg_{i} = cases[i]["input"][{i}].get<{type}>();'
            )
            argument_names.append(f'arg_{i}')

        argument_declarations_code = "\n        ".join(argument_declarations)
        arg_call = ", ".join(argument_names)

        driver_code = f'''

#include "/app/backend/jsonhpp/json.hpp"
using json = nlohmann::json;
using namespace std;

void driver_code() {{
    Solution a;
    json data = R"({dump_json})"_json;
    auto cases = data["{cases_key}"];

    for (int i = 0; i < cases.size(); i++) {{

        {argument_declarations_code}

        auto expected = cases[i]["output"].get<{test_casess["return_type"]}>();
        auto output = a.{test_casess["method_name"]}({arg_call});

        {verify_code}
    }}
'''

        if is_private:
            driver_code += '''
    cout << "Accepted" << endl;
'''

        driver_code += '''
}

int main() {
    driver_code();
    return 0;
}
'''

        return TotalCodeCombiner.combineUsercodewithDriverCode(file, driver_code)
