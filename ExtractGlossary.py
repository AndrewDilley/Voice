import pandas as pd
import json

def extract_glossary_from_excel(file_path):
    """
    Extracts glossary terms from an Excel file.
    Assumes the first column contains 'Instead of' terms and the second column contains 'Say' terms.
    """
    # Load Excel file
    df = pd.read_excel(file_path, engine="openpyxl")

    # Ensure we only take valid rows with two columns
    if df.shape[1] < 2:
        raise ValueError("Excel file must contain at least two columns!")

    # Extract first two columns and clean up text
    glossary = {
        str(row[0]).strip().lower(): str(row[1]).strip().lower()
        for row in df.iloc[:, :2].dropna().values
    }

    return glossary

# Load glossary from Excel
excel_path = "BasicsAndGlossary.xlsx"
glossary_dict = extract_glossary_from_excel(excel_path)

# Save glossary to JSON
json_path = "glossary.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(glossary_dict, f, indent=4)

print(f"✅ Glossary extracted and saved as {json_path}!")
