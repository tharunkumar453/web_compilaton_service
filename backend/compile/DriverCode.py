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
class CDriverCode(DriverCode):

    def DriverCodeGenerator(self, file, test_casess,is_private):
        
        inputs = [tc["input"] for tc in test_casess[ "private_cases" if is_private else "public_cases"]]
        ans = [tc["output"] for tc in test_casess[ "private_cases" if is_private else "public_cases"]]
        method = test_casess["method_name"]
        return_type = test_casess["return_type"]

        if return_type == "string":
            c_return = "char*"
            verify_code = VerifyCodeFactory.get_verify_code(return_type).verify_code_generator(is_private)
           

        elif return_type == "vector<int>":
            c_return = "int*"
            verify_code = VerifyCodeFactory.get_verify_code(return_type).verify_code_generator(is_private)

        else:
            c_return = return_type           
            verify_code = VerifyCodeFactory.get_verify_code(return_type).verify_code_generator(is_private)
        driver_code = '''
main() {
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

            driver_code+=f'''
    {c_return} output = {method}({formatted_args});
    {c_return} expected = {y};  
    {verify_code}
'''
        driver_code+='''
    return 0;

}
'''
        return TotalCodeCombiner.combineUsercodewithDriverCode(file, driver_code)







class verify_code(ABC):
    @abstractmethod
    def verify_code_generator(self,is_private) -> str:
        pass  
  
class string_verify(verify_code):
    def verify_code_generator(self,is_private):
        if is_private:
                verify_code = '''
            if (strcmp(output, expected) != 0) {
                printf("Error at test case %d\\n", i + 1);
                return;
            }
        }
        printf("Accepted\\n");
'''         
        else:
                verify_code = '''
            printf("Test case %d: Output: %s, Expected: %s\\n", i + 1, output, expected);
            if (strcmp(output, expected) != 0) {
                printf("Error at test case %d\\n", i + 1);
                return;
            }
        }
        printf("Accepted\\n");

'''
        return verify_code
    
class vector_int_verify(verify_code):
    def verify_code_generator(self,is_private):
        if is_private:
            verify_code = '''
if (memcmp(output, expected, expected_size * sizeof(int)) != 0) {
    printf("Error at test case %d\\n", i + 1);
    return;
}
printf("Accepted\\n");
'''        
        else:
            verify_code = '''
printf("Test case %d: Output: ", i + 1);
for (int j = 0; j < expected_size; j++) {
    printf("%d ", output[j]);
}       
printf(", Expected: ");
for (int j = 0; j < expected_size; j++) {
    printf("%d ", expected[j]);
}
printf("\\n");
if (memcmp(output, expected, expected_size * sizeof(int)) != 0) {
    printf("Error at test case %d\\n", i + 1);
    return;
}
printf("Accepted\\n");
'''
        return verify_code
    
class default_verify(verify_code):
    def verify_code_generator(self,is_private):
        if is_private:
            verify_code = '''
if (output != expected) {
    printf("Error at test case %d\\n", i + 1);
    return;
}
printf("Accepted\\n");
'''        
        else:
            verify_code = '''
printf("Test case %d: Output: %d, Expected: %d\\n", i + 1, output, expected);
if (output != expected) {
    printf("Error at test case %d\\n", i + 1);
    return;
}       
printf("Accepted\\n");
'''
        return verify_code
    
class VerifyCodeFactory:
    @staticmethod
    def get_verify_code(return_type):
        if return_type == "string":
            return string_verify()
        elif return_type == "vector<int>":
            return vector_int_verify()
        else:
            return default_verify()             
    
