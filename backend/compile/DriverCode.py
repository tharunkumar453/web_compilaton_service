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
        print(x)
        return x

class DriverCode(ABC): 
    @abstractmethod
    def DriverCodeGenerator(self,file,test_casess) -> str:
        pass


 # Driver code for python   
class PythonDriverCode(DriverCode):
    def DriverCodeGenerator(self,file,test_casess):
        inputs=[tc["input"] for tc in test_casess['cases']]
        ans=[tc["output"] for tc in test_casess['cases']]
        method=test_casess["method_name"]
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
       
        if(out!=exp):
            print("error at test case",i+1)
            return
    print("Accepted")
driver_code()
'''   
        return TotalCodeCombiner.combineUsercodewithDriverCode(file,driver_code)
        
# Driver code for C++
class CppDriverCode(DriverCode):


    def DriverCodeGenerator(self,file,test_casess):
        dump_json=json.dumps(test_casess,indent=2)
        argument_declarations = []
        argument_names = []
        for i, type in enumerate(test_casess["signature"]):
            argument_declarations.append(f'{type} arg_{i} = cases[i]["input"][{i}].get<{type}>();')    
            argument_names.append(f'arg_{i}')

        argument_declarations_code = "\n".join(argument_declarations)
        arg_call = ", ".join(argument_names)
        driver_code=f'''

#include "/app/backend/jsonhpp/json.hpp"
using json = nlohmann::json;
using namespace std;ss
void driver_code() {{
    Solution a;
    json data = R"({dump_json})"_json;
    auto cases = data["cases"];
    for (int i = 0; i < cases.size(); i++) {{
         
        {argument_declarations_code}// code inject in to the cpp wafer
        
        auto expected = cases[i]["output"].get<{test_casess["return_type"]}>();
        auto output = a.{test_casess["method_name"]}({arg_call});// call with multiple argments
        if (output != expected) {{
            cout << "Error at test case " << i + 1 << endl;
            return;
            }}
        }}
        cout << "Accepted" << endl;
    }}

int main() {{
    driver_code();
    return 0;
}}
''' 
        return TotalCodeCombiner.combineUsercodewithDriverCode(file,driver_code)
    

# Driver code for C
class CDriverCode(DriverCode):

    def DriverCodeGenerator(self, file, test_casess):
        inputs = [tc["input"] for tc in test_casess['cases']]
        ans = [tc["output"] for tc in test_casess['cases']]
        method = test_casess["method_name"]
        if test_casess["return_type"] == "string":test_casess["return_type"] = "char*"
        if test_casess["return_type"] == "vector<int>":test_casess["return_type"] = "int*"
        def arg_formatter(arg):
            if isinstance(arg, str):
                return f'"{arg}"'
            elif isinstance(arg, list):
                return "{" + ", ".join(map(str, arg)) + "}"
            else:
                return str(arg)
        driver_code = f'''
int main() {{
'''
        for i, (x, y) in enumerate(zip(inputs, ans)):
            formatted_args = ", ".join(arg_formatter(arg) for arg in x)
            formatted_expected = arg_formatter(y)
            driver_code += f'''
    {test_casess["return_type"]} output = {method}({formatted_args});
    if (output != {formatted_expected}) {{
        printf("Error at test case {i + 1}\\n");
        return 1;
    }} 
'''
        driver_code += '''
    printf("Accepted\\n");
    return 0;
}
'''
        return TotalCodeCombiner.combineUsercodewithDriverCode(file, driver_code) 
