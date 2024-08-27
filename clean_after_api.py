import json
from utils import fetch_diseases_by_codes

# Define the path to the input and output files
input_file_path = 'data_icd_en.json'
output_file_path = 'cleaned_icd_results_en.json'

# Function to retain only specific fields
def retain_fields(input_file, output_file):
    # Read the JSON file with UTF-8 encoding
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    
    filtered_data = []
    for item in data:
        filtered_item = {
            "code": item.get("code"),
            "title": item.get("title"),
            "definition": item.get("definition"),
            "exclusion": item.get("exclusion"),
            "inclusion": item.get("inclusion"),
            "longDefinition": item.get("longDefinition"),
            "indexTerm": item.get("indexTerm")
        }
        filtered_data.append(filtered_item)
    
    # Write the JSON file with UTF-8 encoding
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump({"data": filtered_data}, outfile, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    retain_fields(input_file_path, output_file_path)
    print(
        'The results have been written in the desired output file.'
    )


    