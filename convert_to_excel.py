import json
import pandas as pd
from illegal_char_cleaner import clean_text
# Define the path to the input and output files
input_file_path = 'cleaned_icd_results_en.json'
output_file_path = 'en_icd_results.xlsx'


# Function to process JSON data and convert to a DataFrame
def process_json_to_dataframe(input_file):
    # Read the JSON file
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    # Extract relevant information
    rows = []
    for item in data['data']:
        code = clean_text(item.get('code', ''))
        title_value = clean_text(item.get('title', {}).get('@value', ''))

        # Handle 'definition'
        definition = item.get('definition')
        definition_value = clean_text(definition.get('@value', '') if definition else '')

        # Handle 'longDefinition'
        long_definition = item.get('longDefinition')
        long_definition_value = clean_text(long_definition.get('@value', '') if long_definition else '')

        # Handle 'inclusions'
        inclusions = item.get('inclusion', [])
        inclusion_list = []
        if isinstance(inclusions, list):
            for inclusion in inclusions:
                label = inclusion.get('label', {})
                inclusion_list.append(clean_text(label.get('@value', '')))
        elif isinstance(inclusions, dict):
            label = inclusions.get('label', {})
            inclusion_list.append(clean_text(label.get('@value', '')))
        inclusion_str = '; '.join(inclusion_list)

        # Handle 'exclusions'
        exclusions = item.get('exclusion', [])
        exclusion_list = []
        if isinstance(exclusions, list):
            for exclusion in exclusions:
                label = exclusion.get('label', {})
                exclusion_list.append(clean_text(label.get('@value', '')))
        elif isinstance(exclusions, dict):
            label = exclusions.get('label', {})
            exclusion_list.append(clean_text(label.get('@value', '')))
        exclusion_str = '; '.join(exclusion_list)

        # Handle 'indexTerm'
        index_terms = item.get('indexTerm', [])
        index_terms_values = []
        if isinstance(index_terms, list):
            for term in index_terms:
                label = term.get('label', {})
                index_terms_values.append(clean_text(label.get('@value', '')))
        elif isinstance(index_terms, dict):
            label = index_terms.get('label', {})
            index_terms_values.append(clean_text(label.get('@value', '')))
        index_terms_str = '; '.join(index_terms_values)

        # Append row to the list
        rows.append({
            'Code': code,
            'Title': title_value,
            'Definition': definition_value,
            'LongDefinition': long_definition_value,
            'Inclusion': inclusion_str,
            'Exclusion': exclusion_str,
            'IndexTerms': index_terms_str
        })

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(rows)
    return df

# Function to save DataFrame to an Excel file
def save_dataframe_to_excel(df, output_file):
    df.to_excel(output_file, index=False, engine='openpyxl')

if __name__ == "__main__":
    # Process the JSON file and convert to DataFrame
    df = process_json_to_dataframe(input_file_path)
    # Save the DataFrame to an Excel file
    save_dataframe_to_excel(df, output_file_path)
    print('The results have been written to the desired output file.')
