import subprocess

# Path to your Python or other supported language file
input_file = "python_example8.py"
output_file = "code2flowflowchart.png"

# Run code2flow as a subprocess
subprocess.run(["code2flow", input_file, "-o", output_file])

print(f"Flowchart saved as {output_file}")
