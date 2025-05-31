import xlwings as xw
import os
import re
import shutil
import pandas as pd
import json

# ------------------------- Export & Convert Multiple Sheets -------------------------
print(f"\nConverting the sheets from Vocabulary.xlsx to html files...")

def convert_to_utf8(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    try:
        with open(file_path, 'r', encoding='windows-1252') as f:
            content = f.read()
    except UnicodeDecodeError as e:
        print(f"Cannot decode {file_path} with windows-1252: {e}")
        return

    # Ensure UTF-8 meta tag
    content = re.sub(
        r'<meta[^>]+charset=[^>]+>',
        '<meta charset="UTF-8">',
        content,
        flags=re.IGNORECASE
    )

    if '<meta charset="UTF-8">' not in content:
        content = content.replace("<head>", "<head>\n<meta charset=\"UTF-8\">", 1)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Converted to UTF-8: {file_path}")

# Function to fix the frameset rows in *_table.html before its creation
def fix_frameset_rows(html_path):
    if not os.path.exists(html_path):
        print(f"File not found for frameset fix: {html_path}")
        return
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Replace <frameset rows="*,39" with <frameset rows="*"
    content = content.replace('<frameset rows="*,39"', '<frameset rows="*"')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed frameset rows in: {html_path}")

# Sheets to export (mapping of sheet name -> output filename)
sheets_to_export = {
    "Grammatik": "grammatik_table.html",
    "Vokabular": "vokabular_table.html",
    "Maschinenbau": "maschinenbau_table.html",
    "Führerschein": "fuehrerschein_table.html",
}

# Create output directory
output_dir = os.path.join(os.getcwd(), "Extracted_htmls")
os.makedirs(output_dir, exist_ok=True)

# Open workbook once
app = xw.App(visible=False)
wb = app.books.open("Vocabulary.xlsx")

for sheet_name, html_filename in sheets_to_export.items():
    print(f"\nProcessing sheet: {sheet_name}")

    # Prepare output paths inside Extracted_htmls
    html_file_path = os.path.join(output_dir, html_filename)
    support_folder = os.path.join(output_dir, os.path.splitext(html_filename)[0] + "-Dateien")

    # Delete previous HTML file if exists
    if os.path.exists(html_file_path):
        os.remove(html_file_path)

    # Delete previous support folder if exists
    if os.path.exists(support_folder):
        shutil.rmtree(support_folder)

    # Export sheet to new workbook then HTML
    new_wb = xw.Book()
    wb.sheets[sheet_name].api.Copy(Before=new_wb.sheets[0].api)
    new_wb.sheets[1].delete()
    new_wb.api.SaveAs(html_file_path, FileFormat=44)
    new_wb.close()

    # Convert encoding and cleanup
    convert_to_utf8(html_file_path)

    # Remove tabstrip frame
    with open(html_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'<frame[^>]+src=["\'].*tabstrip\.html["\'][^>]*>', '', content, flags=re.IGNORECASE)
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    # Fix frameset rows attribute
    fix_frameset_rows(html_file_path)

    # Convert subfiles in support folder
    if os.path.exists(support_folder):
        for root, _, files in os.walk(support_folder):
            for name in files:
                if name.endswith('.html'):
                    convert_to_utf8(os.path.join(root, name))
    else:
        print("Supporting folder not found")

wb.close()
app.quit()

print(f"\nAll selected sheets exported and saved as UTF-8 HTML inside 'Extracted_htmls' folder in {output_dir}")

# ------------------------- Export Excel to JSONs -------------------------

# Load all sheets from the Excel file
excel_file = "Vocabulary.xlsx"

# Mapping sheet names to lowercase filenames (with umlaut replacement)
sheet_name_map = {
    "Vokabular": "vokabular",
    "Grammatik": "grammatik",
    "Maschinenbau": "maschinenbau",
    "Führerschein": "fuehrerschein"
}

# Read all sheets
all_sheets = pd.read_excel(excel_file, sheet_name=None, dtype=str)

print(f"\nConverting the sheets from Vocabulary.xlsx to JSON files...")

# ✅ Only convert the sheets listed in `sheet_name_map`
for sheet_name in sheet_name_map:
    df = all_sheets.get(sheet_name)
    if df is None:
        print(f"Warning: Sheet '{sheet_name}' not found in the Excel file.")
        continue

    print(f"\nProcessing sheet: {sheet_name}")
    df = df.fillna("")  # Replace NaN with empty strings
    data = df.to_dict(orient="records")

    file_name = sheet_name_map[sheet_name]
    json_path = os.path.join(output_dir, f"{file_name}.json")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Exported '{sheet_name}' to: {json_path}")