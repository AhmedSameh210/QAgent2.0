import subprocess
import re

class Formater:
    def CPP(code, clang_format_path="clang-format"):
        process = subprocess.Popen(
            [clang_format_path, "-style=LLVM"],
            stdin= subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate(input=code.encode())
        if stderr:
            raise RuntimeError(f"ClangFormat error: {stderr.decode()}")
        return stdout.decode()
    
    def Python(code):
        """
        Formats Python code in the input file and writes the result to the output file.

        Rules:
        1. No code after a colon (:) on the same line.
        2. Keep all initialization and closing brackets on one line.
        """
       
        formatted_lines = []
        for line in code:
            stripped = line.strip()

            # Rule 1: Split at colon and place the remaining code on the next line
            if ':' in stripped and not stripped.endswith(":"):
                parts = stripped.split(':', 1)
                formatted_lines.append(parts[0] + ':')  # Keep the part before the colon
                remaining_code = parts[1].strip()
                if remaining_code:
                    formatted_lines.append('    ' + remaining_code)  # Add indented remaining code
            # Rule 2: Place initialization and closing brackets on one line
            elif re.match(r".*=\s*\[.*", stripped) or re.match(r".*=\s*\{.*", stripped):
                formatted_lines.append(re.sub(r"\s+", " ", stripped))  # Compress everything to one line
            elif stripped.startswith(("}", "]", ")")):
                formatted_lines[-1] = formatted_lines[-1].strip() + stripped
            else:
                formatted_lines.append(line.rstrip())

        return ("\n".join(formatted_lines) + "\n")


        

cpp_code = None
with open('CPP_example.cpp','r') as f: cpp_code = f.read()
output_file = "formatted_cpp_code.cpp"
with open(output_file, "w") as file:
    file.write(Formater.CPP(cpp_code))

python_code = None
with open('python_example8.py','r') as f: python_code = f.read()
output_file = "formatted_python_code.py"
with open(output_file, "w") as file:
    file.write(Formater.CPP(python_code))

