from config.mapping import FIELD_MAPPING

def map_record(record: dict):
    mapped = {}

    normalized_record = {
        k.strip().lower(): v for k, v in record.items()
    }

    for template_key, excel_key in FIELD_MAPPING.items():
        key = excel_key.strip().lower()

        value = normalized_record.get(key, None)

        if hasattr(value, "strftime"):
            value = value.strftime("%d-%m-%Y")

        if template_key == "Joining_Bonus":
            raw_value = normalized_record.get("joining bonus", None)

            if raw_value in ["", None, 0, "0"]:
                mapped["Joining_Bonus"] = None  
            else:
                try:
                    mapped["Joining_Bonus"] = f"{int(raw_value):,}"
                except:
                    mapped["Joining_Bonus"] = str(raw_value)

            continue 

        if isinstance(value, (int, float)):
            value = f"{int(value):,}"

        mapped[template_key] = str(value).strip() if value else ""

    print("MAPPED DATA:", mapped)  

    return mapped