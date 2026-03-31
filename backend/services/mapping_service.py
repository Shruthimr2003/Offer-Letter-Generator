
from config.mapping import FIELD_MAPPING

BONUS_FIELDS = [
    "Joining_Bonus",
    "Retention_Bonus",
    "One_Time_Bonus",
    "Variable_Pay",
    "Notice_Period_Buyout",
    "Relocation",
]

def map_record(record: dict):
    mapped = {}

    normalized_record = {
        k.strip().lower(): v for k, v in record.items()
    }

    for template_key, excel_key in FIELD_MAPPING.items():
        key = excel_key.strip().lower()
        raw_value = normalized_record.get(key, None)

        # Format date
        if hasattr(raw_value, "strftime"):
            raw_value = raw_value.strftime("%d-%m-%Y")

        # Handle all bonus-type fields
        if template_key in BONUS_FIELDS:
            if raw_value in ["", None, 0, "0"]:
                mapped[template_key] = None
            else:
                try:
                    mapped[template_key] = f"{int(raw_value):,}"
                except:
                    mapped[template_key] = str(raw_value)
            continue

        # Default number formatting
        if isinstance(raw_value, (int, float)):
            raw_value = f"{int(raw_value):,}"

        mapped[template_key] = str(raw_value).strip() if raw_value else ""

    print("MAPPED DATA:", mapped)

    return mapped