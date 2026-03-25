import os
from docxtpl import DocxTemplate
from services.mapping_service import map_record
from services.table_service import replace_ctc_table
import pandas as pd

TEMP_DIR = "temp"

def generate_docx(data, template_path, salary_path, doc_no):
    generated = []
    
    df = pd.read_excel(salary_path)
    df = df.fillna("")

    for record in data:
        doc = DocxTemplate(template_path)

        mapped_data = map_record(record)
        
        mapped_data["DocNo"] = doc_no

        doc.render(mapped_data)

        safe_name = mapped_data.get("Candidate_Name", "Unknown").replace(" ", "_")
        filename = f"{safe_name}_OfferLetter.docx"
        path = os.path.join(TEMP_DIR, filename)

        doc.save(path)
        
        replace_ctc_table(path, df)

        generated.append({
            "candidate": mapped_data.get("Candidate_Name"),
            "docx_path": path,
            "filename": filename 
        })

    return generated