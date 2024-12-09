
import subprocess
import os
import tempfile

def run_cpp_code(cpp_code):
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        cpp_file = os.path.join(temp_dir, "code.cpp")
        exe_file = os.path.join(temp_dir, "code.exe")  # Or just "code" on Linux/Mac

        # Write the C++ code to a file
        with open(cpp_file, "w") as f:
            f.write(cpp_code)

        try:
            # Compile the C++ code
            compile_result = subprocess.run(
                ["g++", cpp_file, "-o", exe_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if compile_result.returncode != 0:
                return f"Compilation failed:\n{compile_result.stderr}"

            # Run the compiled executable
            run_result = subprocess.run(
                [exe_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if run_result.returncode != 0:
                return f"Execution failed:\n{run_result.stderr}"

            # Return the program's output
            return run_result.stdout
        except FileNotFoundError:
            return "Error: g++ compiler is not installed or not in PATH."


def run_js_code(js_code):
    with tempfile.TemporaryDirectory() as temp_dir:
        js_file = os.path.join(temp_dir, "script.js")

        # Save JavaScript code to a file
        with open(js_file, "w") as f:
            f.write(js_code)

        try:
            # Run the JavaScript code using Node.js
            run_result = subprocess.run(
                ["node", js_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True  # Ensure it raises an exception on non-zero return code
            )

            # Return the program's output (stdout and stderr combined)
            return run_result.stdout + "\n" + run_result.stderr if run_result.stderr else run_result.stdout
        except subprocess.CalledProcessError as e:
            # Handle the error and print both stdout and stderr
            return f"Execution failed with error code {e.returncode}:\n{e.stderr}\n{e.stdout}"
        except FileNotFoundError:
            return "Error: node.js is not installed or not in PATH."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"


def run_java_code(java_code):
    with tempfile.TemporaryDirectory() as temp_dir:
        java_file = os.path.join(temp_dir, "Main.java")

        # Save Java code to a file
        with open(java_file, "w") as f:
            f.write(java_code)

        try:
            # Compile the Java code using javac
            compile_result = subprocess.run(
                ["javac", java_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Check for compilation errors
            if compile_result.returncode != 0:
                return f"Compilation failed:\n{compile_result.stderr}"

            # Run the compiled Java program
            class_name = "Main"  # Adjust if the class name differs
            run_result = subprocess.run(
                ["java", "-ea","-cp", temp_dir, class_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(run_result)
            # Check for runtime errors
            if run_result.returncode != 0:
                return f"Execution failed:\n{run_result.stderr}"

            # Return the program's output
            return run_result.stdout

        except FileNotFoundError as e:
            return f"Error: javac or java is not installed or not in PATH. {e}"

        except Exception as e:
            return f"An unexpected error occurred: {e}"


def python_rate(code , list_of_asserts):
  exec(code)
  totalTestCases = len(list_of_asserts)
  success_rate = 0
  for i in list_of_asserts:
    try:
      exec(i)
      success_rate += 1
    except:
      success_rate += 0
      
  success_rate = success_rate/totalTestCases
  return success_rate



def cpp_rate(code , list_of_asserts):
  totalTestCases = len(list_of_asserts)
  success_rate = 0
  for i in list_of_asserts:
      #create cpp template
      test_case = f'''
      #include <cassert>
      {code}
      \n
      int main() {{
          {i}
      }}
      '''
      #print(test_case)
      res=run_cpp_code(test_case)
      if "failed" in res or "Error" in res:
        continue
      else :
        success_rate += 1
  success_rate = success_rate/totalTestCases
  return success_rate


def javascript_rate(code , list_of_asserts):
    totalTestCases = len(list_of_asserts)
    success_rate = 0
    
    for i in list_of_asserts:
        test_case = f'''
        {code}


        {i}
        '''
        #print(test_case)
        res = run_js_code(test_case)
        # Check if the assertion was successful
        if "failed" in res or "Error" in res:
            continue
        else:
            success_rate += 1
    
    success_rate = success_rate / totalTestCases
    return success_rate


def java_rate(code, list_of_asserts):
    totalTestCases = len(list_of_asserts)
    success_rate = 0
    
    for i in list_of_asserts:
        test_case = f'''
        public class Main {{
            public static void main(String[] args) {{
                // Test cases
                {i}
            }}

            {code}
        }}
        '''
        
        res = run_java_code(test_case)
        
        # Check if the assertion was successful
        if "failed" in res or "Error" in res:
            continue
        else:
            success_rate += 1
    
    success_rate = success_rate / totalTestCases
    return success_rate
