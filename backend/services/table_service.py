from docx import Document
import re
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
 
def replace_ctc_table(docx_path, df):
    if df.empty:
        print(" Salary Excel is empty")
        return
 
    doc = Document(docx_path)
 
    ctc_data = []
    retirals_data = []
 
    def clean_text(text):
        text = str(text).lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
 
    def clean_value(val):
        if str(val).lower() == "nan" or val == "":
            return ""
        try:
            num = float(val)
            return str(int(round(num)))  
        except ValueError:
            return str(val).strip()
 
    ctc_keywords = [
        "basic salary", "hra", "special allowance", "lta", "food allowance",
        "mobile", "broadband", "gym", "technical books", "employee s provident fund",
        "annual gross salary"
    ]
 
    retirals_keywords = [
        "medical insurance", "term life insurance", "provident fund",
        "gratuity", "ctc amount"
    ]
 
    for _, row in df.iterrows():
        values = [clean_value(v) for v in row]
 
        if all(v == "" for v in values):
            continue
 
        row_text = clean_text(" ".join(values))
        print("ROW:", row_text)
 
        if any(key in row_text for key in ctc_keywords):
            ctc_data.append(values)
            continue

        if any(key in row_text for key in retirals_keywords):
            amount = 0
            try:
                amount = float(values[1])
            except:
                pass
            if amount == 0:
                continue
            retirals_data.append([values[0], clean_value(values[1])])
            continue
 
    print("CTC DATA:", ctc_data)
    print("RETIRALS DATA:", retirals_data)
 
    ctc_table = None
    retirals_table = None
 
    for table in doc.tables:
        table_text = " ".join(
            clean_text(cell.text)
            for row in table.rows
            for cell in row.cells
        )
 
        if "annual ctc" in table_text and ctc_table is None:
            ctc_table = table
        elif ("retiral" in table_text or "benefit" in table_text) and retirals_table is None:
            retirals_table = table

    def fill_table(table, data, label, remove_header=False, is_retiral=False):
        if not table:
            print(f" {label} table not found")
            return
        if not data:
            print(f" No data for {label}")
            return
 
        if remove_header:
            while len(table.rows) > 0:
                table._element.remove(table.rows[0]._element)
        else:
            while len(table.rows) > 1:
                table._element.remove(table.rows[1]._element)
 
  
        for idx, row in enumerate(data):
            new_cells = table.add_row().cells
            for i in range(len(new_cells)):
                value = row[i] if i < len(row) else ""
                new_cells[i].text = value
 
            if not is_retiral:
                if len(new_cells) > 0:
                    for paragraph in new_cells[0].paragraphs:
                        for run in paragraph.runs:
                            run.font.bold = True
                row_text = " ".join([str(cell) for cell in row]).lower()
                if "annual gross salary" in row_text:
                    for cell in new_cells:
                        shading_elm = OxmlElement('w:shd')
                        shading_elm.set(qn('w:fill'), '808080')  
                        cell._tc.get_or_add_tcPr().append(shading_elm)
                        for paragraph in cell.paragraphs:
                            for run in paragraph.runs:
                                run.font.bold = True
 
            if is_retiral:
                if len(new_cells) > 0:
                    for paragraph in new_cells[0].paragraphs:
                        for run in paragraph.runs:
                            run.font.bold = True
                if idx == len(data) - 1:
                    for cell in new_cells:
                        shading_elm = OxmlElement('w:shd')
                        shading_elm.set(qn('w:fill'), '808080')  
                        cell._tc.get_or_add_tcPr().append(shading_elm)
                        for paragraph in cell.paragraphs:
                            for run in paragraph.runs:
                                run.font.bold = True
 
    fill_table(ctc_table, ctc_data, "CTC", remove_header=False, is_retiral=False)
    fill_table(retirals_table, retirals_data, "Retirals", remove_header=True, is_retiral=True)
 
    doc.save(docx_path)
    print("Both tables updated successfully!")