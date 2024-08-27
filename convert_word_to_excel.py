import re
import pandas as pd
from docx import Document
from docx.shared import Pt 

def is_code(paragraph):
    """
    Determines if a paragraph contains a code based on the structure.
    """
    # Loosen the regex to accommodate variations like 'XD5GF6', 'LD50.02', 'LB12', 'LB12.1'
    return bool(re.match(r'^[A-Za-z0-9\-\.]+$', paragraph.strip()))


def process_word_document(doc_path):
    try:
        document = Document(doc_path)
    except Exception as e:
        print(f"Failed to open the document. Error: {e}")
        return []

    data = []
    code, title, description, inclusion = None, None, '', ''
    
    for para in document.paragraphs:
        text = para.text.strip()
        
        if not text:  # Skip empty paragraphs
            continue
        
        if is_code(text):
            if code and title:
                data.append({
                    'Code': code,
                    'Title': title,
                    'Description': description.strip(),
                    'Inclusion': inclusion.strip()
                })
            code, title = text.split(maxsplit=1) if ' ' in text else (text, '')
            description, inclusion = '', ''
        elif text.startswith("Inclusions:"):
            inclusion = text.replace("Inclusions:", "").strip()
        else:
            description += ' ' + text

    if code and title:
        data.append({
            'Code': code,
            'Title': title,
            'Description': description.strip(),
            'Inclusion': inclusion.strip()
        })
    
    print(f'data: {data}')
    return data


def save_to_excel(data, excel_path):
    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False)

def convert_word_to_excel(word_path, excel_path):
    data = process_word_document(word_path)
    print(
        f"Document processed. Data saved to Excel file: {excel_path}"
    )
    print(
        f"Total number of codes: {len(data)}"
    )
    if data:  # Only save to Excel if data is successfully extracted
        save_to_excel(data, excel_path)
        print(f"Data successfully saved to {excel_path}")
    else:
        print("No data was extracted.")



word_file_path = 'Foundation_MMS-en.docx'
excel_file_path = '/mnt/data/output_excel_file.xlsx'
convert_word_to_excel(word_file_path, excel_file_path)