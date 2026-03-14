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
        return_type = test_casess["return_type"]
        compare_code = ""

        if return_type == "string":
            c_return = "char*"
            compare_code = "strcmp(output, expected) != 0"

        elif return_type == "vector<int>":
            c_return = "int*"

        else:
            c_return = return_type
            compare_code = "output != expected"

        driver_code = '''
#include<stdio.h>
#include<string.h>

int main() {
'''

        for i,(x,y) in enumerate(zip(inputs,ans)):

            args=[]
            setup_code=""

            for j,arg in enumerate(x):

                if isinstance(arg,list):

                    arr_name=f"arr_{i}_{j}"
                    arr_vals=", ".join(map(str,arg))

                    setup_code+=f'''
    int {arr_name}[] = {{{arr_vals}}};
'''
                    args.append(arr_name)

                elif isinstance(arg,str):

                    args.append(f'"{arg}"')

                else:
                    args.append(str(arg))

            formatted_args=", ".join(args)

            if return_type=="vector<int>":

                expected_vals=", ".join(map(str,y))
                size=len(y)

                driver_code+=f'''
{{
                {setup_code}

    int* output = {method}({formatted_args});

    int expected[] = {{{expected_vals}}};
    int expected_size = {size};

    if(memcmp(output, expected, sizeof(int)*expected_size)!=0){{
        printf("Error at test case {i+1}\\n");
        return 1;
    }}
}}
'''

            else:

                expected = f'"{y}"' if isinstance(y,str) else y

                driver_code+=f'''

{{
                {setup_code}

                {c_return} output = {method}({formatted_args});
                {c_return} expected = {expected};

                if({compare_code}){{
                printf("Error at test case {i+1}\\n");
                    return 1;
                }}
}}
'''

        driver_code += '''
    printf("Accepted\\n");
    return 0;
}
'''

        return TotalCodeCombiner.combineUsercodewithDriverCode(file, driver_code)