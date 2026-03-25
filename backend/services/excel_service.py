import pandas as pd

def parse_excel(file_path: str):
    df = pd.read_excel(file_path)

    df.columns = df.columns.str.strip().str.lower()

    df = df.fillna("")

    if "year" not in df.columns:
        df["year"] = "2026"

    return df.to_dict(orient="records")