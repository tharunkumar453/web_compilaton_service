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
        cases = test_casess.get("cases", [])
        method = test_casess["method_name"]
        signature = test_casess.get("signature", [])

        def normalize_c_type(tp):
            if tp == "string":
                return "char*"
            if tp == "vector<int>":
                return "int*"
            return tp

        return_type = normalize_c_type(test_casess["return_type"])

        def c_string_literal(value: str) -> str:
            return json.dumps(value)

        def format_scalar(value):
            if isinstance(value, bool):
                return "1" if value else "0"
            if isinstance(value, str):
                return c_string_literal(value)
            if value is None:
                return "0"
            return str(value)

        driver_code = f'''
#include <stdio.h>
#include <string.h>

int main() {{

    {return_type} result;

'''

        for i, tc in enumerate(cases):
            inp = tc.get("input", [])
            out = tc.get("output", tc.get("expected", tc.get("outputs")))

            if not isinstance(inp, list):
                inp = [inp]

            arg_values = []

            # Build call args based on signature first.
            for j, sig in enumerate(signature):
                value = inp[j] if j < len(inp) else None

                if sig == "vector<int>":
                    arr_name = f"arg_{i}_{j}"
                    arr_data = value if isinstance(value, list) else []
                    arr_init = ",".join(map(str, arr_data)) if arr_data else "0"
                    driver_code += f"    int {arr_name}[] = {{{arr_init}}};\n"
                    arg_values.append(arr_name)
                    arg_values.append(str(len(arr_data)))
                elif sig == "string":
                    s_name = f"arg_{i}_{j}"
                    s_value = value if isinstance(value, str) else ""
                    driver_code += f"    char {s_name}[] = {c_string_literal(s_value)};\n"
                    arg_values.append(s_name)
                else:
                    arg_values.append(format_scalar(value))

            # If test data has extra args beyond signature, pass them as scalars.
            for extra_idx in range(len(signature), len(inp)):
                arg_values.append(format_scalar(inp[extra_idx]))

            args = ", ".join(arg_values)
            driver_code += f"    result = {method}({args});\n"

            if return_type == "char*":
                expected = c_string_literal(out if isinstance(out, str) else "")
                driver_code += f'''
    if (strcmp(result, {expected}) != 0) {{
        printf("Error at test case {i+1}\\n");
        return 1;
    }}
'''
            elif return_type in ("int", "long long"):
                driver_code += f'''
    if (result != {format_scalar(out)}) {{
        printf("Error at test case {i+1}\\n");
        return 1;
    }}
'''
            elif return_type == "int*":
                expected_arr = out if isinstance(out, list) else []
                expected_init = ",".join(map(str, expected_arr)) if expected_arr else "0"
                expected_len = len(expected_arr)
                driver_code += f'''
    int expected_{i}[] = {{{expected_init}}};
    if (memcmp(result, expected_{i}, sizeof(int) * {expected_len}) != 0) {{
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