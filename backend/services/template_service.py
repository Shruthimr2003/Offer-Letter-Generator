import os
import pandas as pd
from docxtpl import DocxTemplate
from docx import Document

from services.mapping_service import map_record
from services.table_service import replace_ctc_table_dynamic

TEMP_DIR = "temp"


def generate_docx(data, template_path, salary_path, doc_no):
    generated = []

    # ==============================
    # 📊 READ EXCEL (MULTI-SHEET)
    # ==============================
    excel_file = pd.ExcelFile(salary_path)
    sheet_names = excel_file.sheet_names

    df_initial = None
    df_revised = None
    print("SHEETS FOUND:", sheet_names)
    for sheet in sheet_names:
        name = sheet.lower().strip()

        # ✅ 1. Detect REVISED FIRST
        if "revised" in name:
            df_revised = pd.read_excel(excel_file, sheet_name=sheet).fillna("")
            print(f"Detected Revised Sheet: {sheet}")

        # ✅ 2. Then detect INITIAL
        elif name == "ctc":
            df_initial = pd.read_excel(excel_file, sheet_name=sheet).fillna("")
            print(f"Detected Initial Sheet: {sheet}")

        

    if df_initial is None:
        raise Exception("CTC sheet not found in Excel")

    # ==============================
    # 📄 GENERATE DOCUMENTS
    # ==============================
    for record in data:
        doc = DocxTemplate(template_path)

        mapped_data = map_record(record)

        mapped_data["DocNo"] = doc_no

        # ✅ IMPORTANT FLAG (controls 2nd page)
        mapped_data["has_revised_ctc"] = df_revised is not None and not df_revised.empty

        # Render template
        doc.render(mapped_data)

        safe_name = mapped_data.get("Candidate_Name", "Unknown").replace(" ", "_")
        filename = f"{safe_name}_OfferLetter.docx"
        path = os.path.join(TEMP_DIR, filename)

        doc.save(path)

        # ==============================
        # 🧾 TABLE REPLACEMENT
        # ==============================
        docx = Document(path)

        # Initial CTC
        replace_ctc_table_dynamic(docx, df_initial, section="initial")

        # Revised CTC (ONLY if exists)
        if mapped_data["has_revised_ctc"]:
            replace_ctc_table_dynamic(docx, df_revised, section="revised")

        docx.save(path)

        generated.append({
            "candidate": mapped_data.get("Candidate_Name"),
            "docx_path": path,
            "filename": filename
        })

    return generated