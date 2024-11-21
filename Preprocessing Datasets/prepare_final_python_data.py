import pandas as pd 
import json

def read_jsonl_to_dataframe(file_path):
    try:
        # Read each line of the JSONL file as a separate JSON object
        with open(file_path, 'r', encoding='utf-8') as file:
            data = [json.loads(line) for line in file]

        # Convert the list of JSON objects to a Pandas DataFrame
        df = pd.DataFrame(data)
        return df

    except Exception as e:
        print(f"Error reading the JSONL file: {e}")
        return None
    
mbbp_dataFrame = read_jsonl_to_dataframe("Preprocessing Datasets\\python datasets\\mbpp.jsonl")

mbbp_dataFrame.to_csv("Preprocessing Datasets\\python datasets\\mbpp_dataset.csv")

human_eval = pd.read_csv("Preprocessing Datasets\\python datasets\\human_eval_after_preprocessing.csv")
mbpp = pd.read_csv("Preprocessing Datasets\\python datasets\\mbpp_dataset.csv")
merged_df = pd.merge(mbpp, human_eval, on=['task_id', 'code' , 'text' ,'test_list'], how='outer')
print(merged_df.head())
print(merged_df.shape)
print(merged_df.columns)
merged_df.drop( ['Unnamed: 0','test_setup_code','challenge_test_list'], axis = 1 , inplace = True)
print(merged_df.head())
print(merged_df.shape)
print(merged_df.columns)
merged_df.to_csv("Preprocessing Datasets\\python datasets\\final_python_dataset.csv")