# -*- coding: utf-8 -*-
"""llms_test_case_generation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Kf9SuY_FchpiMuOGXFdS5tL8HrAGR_9Q
"""

from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import AutoTokenizer, AutoModel,AutoModelForCausalLM
import torch

"""# Few Shots Prompt Example

based on llms as test case geneartors research paper
"""

code = """
def subtract(a, b):
    return a - b
"""

prompt = f"""
As a Python tester, your task is to create comprehensive test cases for the function given the
function body.These test cases should encompass Basic and Edge scenarios to ensure the
code's robustness and reliability. Write each test case with a single line of assert statement.

examples :
Function :
def find_max(arr):
  return max(arr)

Test Cases :
assert find_max([1, 2, 3]) == 3
assert find_max([-1, -2, -3]) == -1
assert find_max([5, 5, 5, 5]) == 5


Function :
{code}

Test Cases :

"""

"""# Code_T5

"""

def Code_T5(code,prompt):
 # Load the CodeT5 model and tokenizer
 model_name = "Salesforce/codet5-base"
 tokenizer = AutoTokenizer.from_pretrained(model_name)
 model = T5ForConditionalGeneration.from_pretrained(model_name)

 #Input for generation
 inputs = tokenizer.encode(prompt, return_tensors="pt")

 # Print the input for debugging
 print("Input text:", prompt)


 # Generate the output
 outputs = model.generate(inputs, max_length=8000, num_beams=20, early_stopping=True)


 # Decode and print the generated text
 generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
 print("Generated text:", generated_text)

"""# Qwen"""

def Qwen(code,prompt):
 model_name = "Qwen/Qwen2.5-Coder-7B-Instruct"

 model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
 tokenizer = AutoTokenizer.from_pretrained(model_name)

 messages = [
    {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a software testing expert your role is to generate test cases for a given function"},
    {"role": "user", "content": prompt}
]
 text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
 model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

 generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=8000
)
 generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

 response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
 test_cases = []
 for line in response.split('\n'):
    if line.strip().startswith("assert"):
        test_cases.append(line.strip())


 print("Response : ", response)
 return test_cases , code

"""# Graph_Code_Bert"""

def graph_code_bert(code,prompt):

 # Load the pre-trained Graph Code BERT model and tokenizer
 model_name = "microsoft/graphcodebert-base"
 tokenizer = AutoTokenizer.from_pretrained(model_name)
 model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

 # Check if GPU is available and set the device
 device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
 model.to(device)

 inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
 inputs = {key: value.to(device) for key, value in inputs.items()}  # Move inputs to the same device as the model
 outputs = model.generate(**inputs, max_length=512, num_return_sequences=1)
 response = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
 print(response)
#  test_cases = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
#  return test_cases

"""# For Understanding Only"""

from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen2.5-Coder-7B-Instruct"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)
code = """
def subtract(a, b):
    return a - b
"""

prompt = f"""
As a Python tester, your task is to create comprehensive test cases for the function given the
function body.These test cases should encompass Basic and Edge scenarios to ensure the
code's robustness and reliability. Write each test case with a single line of assert statement.

examples :
Function :
def find_max(arr):
  return max(arr)

Test Cases :
assert find_max([1, 2, 3]) == 3
assert find_max([-1, -2, -3]) == -1
assert find_max([5, 5, 5, 5]) == 5


Function :
{code}

Test Cases :

"""


messages = [
    {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a software testing expert your role is to generate test cases for a given function"},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

print(response)

from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import AutoTokenizer, AutoModel
# Load the CodeT5 model and tokenizer
model_name = "Salesforce/codet5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Define the code and prompt
code = """
def subtract(a, b):
    return a - b
"""

prompt =f"""
As a Python tester, your task is to create comprehensive test cases for the function given the
function body.These test cases should encompass Basic and Edge scenarios to ensure the
code's robustness and reliability. Write each test case with a single line of assert statement.

examples :
Function :
def find_max(arr):
  return max(arr)

Test Cases :
assert find_max([1, 2, 3]) == 3
assert find_max([-1, -2, -3]) == -1
assert find_max([5, 5, 5, 5]) == 5


Function :
{code}

Test Cases :

"""



#input_text = f"{prompt}/{code}"
inputs = tokenizer.encode(prompt, return_tensors="pt")

# Print the input for debugging
print("Input text:", prompt)
print("Encoded input:", inputs)

# Generate the output
outputs = model.generate(inputs, max_length=8000, num_beams=20, early_stopping=True)

# Print the raw outputs for debugging
print("Raw outputs:", outputs)

# Decode and print the generated text
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Generated text:", generated_text)