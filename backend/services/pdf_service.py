
import os
from docx2pdf import convert

OUTPUT_DIR = "outputs"

def convert_to_pdf(docx_records):
    results = []

    for item in docx_records:
        docx_path = item["docx_path"]

        candidate = (item.get("candidate") or "Unknown").replace(" ", "_")

        pdf_filename = f"{candidate}_OfferLetter.pdf"
        pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)

        convert(docx_path, pdf_path)

        results.append({
            "candidate": item.get("candidate"),
            "filename": pdf_filename
        })

    return results