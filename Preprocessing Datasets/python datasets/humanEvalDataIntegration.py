from HandelingcornerCases import FixDataSeries
import pandas as pd
import json
import re

def read_jsonl_to_dataframe(file_path):
    """
    Reads a JSONL file and converts it into a Pandas DataFrame.

    Args:
        file_path (str): Path to the JSONL file.

    Returns:
        pd.DataFrame: DataFrame containing the JSONL data.
    """
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
    
humanEvalDataFrame = read_jsonl_to_dataframe('human-eval-v2-20210705.jsonl')

signatures = []
descriptions = []

for field in humanEvalDataFrame['prompt']:

    # every signature in python start with def keyword
    start_index = field.find('def')

    if(start_index == -1):
        raise Exception("there's no signature at this entry!")
    
    # and every siginature ends with : and then breaks to a new line if the file is formated correctly!
    end_chars = r':\n'

    separation = re.split(end_chars,field[start_index:], 1)

    signatures.append(separation[0] + ':\n')
    descriptions.append(separation[1])

humanEvalDataFrame['code'] = pd.Series([sig + body for sig, body in zip(signatures, humanEvalDataFrame['canonical_solution'])])
humanEvalDataFrame['text'] = pd.Series(descriptions)

humanEvalDataFrame.drop('prompt', axis=1,inplace=True)
humanEvalDataFrame.drop('canonical_solution', axis=1,inplace=True)

humanEvalDataFrame['task_id'] = humanEvalDataFrame['task_id'].apply(lambda x: x[len("HumanEval/"):])

test_list = []
for row_index in range(humanEvalDataFrame.shape[0]):
    matches = re.findall(r'assert.*\n',humanEvalDataFrame['test'][row_index])

    for i, match in enumerate(matches):
        matches[i] = re.sub('candidate',humanEvalDataFrame['entry_point'][row_index],match)
    test_list.append(matches)
humanEvalDataFrame['test_list'] = pd.Series(test_list)
humanEvalDataFrame.drop('entry_point',axis=1,inplace=True)
humanEvalDataFrame.drop('test',axis=1,inplace=True)


FixDataSeries(humanEvalDataFrame, 'test_list')


def RemoveBreakLines(list):
    for i, element in enumerate(list): 
        list[i] = element.replace('\n', '')
    return list

humanEvalDataFrame['test_list'] = humanEvalDataFrame['test_list'].apply(lambda asserts: RemoveBreakLines(asserts))
for i in range(humanEvalDataFrame.shape[0]):
    humanEvalDataFrame['test_list'][i] = RemoveBreakLines(humanEvalDataFrame['test_list'][i])

humanEvalDataFrame.to_csv('final_output.csv')