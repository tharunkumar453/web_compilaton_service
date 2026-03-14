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
using namespace std;
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

        inputs = [tc["input"] for tc in test_casess["cases"]]
        outputs = [tc["output"] for tc in test_casess["cases"]]

        method = test_casess["method_name"]
        return_type = test_casess["return_type"]

        if return_type == "string": return_type = "char*"
        elif return_type == "vector<int>":return_type = "int*"


        def format_arg(x):
            if isinstance(x, str):
                return f'"{x}"'
            return str(x)

        def format_expected(x):
            if isinstance(x, str):
                return f'"{x}"'
            return str(x)

        driver_code = f'''
int main() {{

    {return_type} result;

'''

        for i, (inp, out) in enumerate(zip(inputs, outputs)):

            if isinstance(inp, list):
                args = ",".join(map(format_arg, inp))
            else:
                args = format_arg(inp)

            expected = format_expected(out)

            driver_code += f'''
    result = {method}({args});
'''
 
            if return_type == "char*":
                driver_code += f'''
    if (strcmp(result, {expected}) != 0) {{
        printf("Error at test case {i+1}\\n");
        return 1;
    }}
'''
            elif return_type == "int":
                driver_code += f'''
    if (result != {expected}) {{
        printf("Error at test case {i+1}\\n");
        return 1;
    }}  

'''
            elif return_type == "int*":
                driver_code += f'''
    int expected_{i}[] = {{{",".join(map(str,out))}}};
    if (memcmp(result, expected_{i}, sizeof(expected_{i})) != 0) {{
        printf("Error at test case {i+1}\\n");
        return 1;
    }}
'''

        driver_code += '''
    printf("Accepted\\n");
    return 0;
}
'''

        return TotalCodeCombiner.combineUsercodewithDriverCode(file, driver_code)