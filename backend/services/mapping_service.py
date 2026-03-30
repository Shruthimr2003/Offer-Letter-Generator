from config.mapping import FIELD_MAPPING
from utils.number_to_words import convert_to_words_indian


def map_record(record: dict):
    mapped = {}

    # Normalize keys
    normalized_record = {
        k.strip().lower(): v for k, v in record.items()
    }

    for template_key, excel_key in FIELD_MAPPING.items():
        key = excel_key.strip().lower()
        value = normalized_record.get(key, None)

        # ==============================
        # 📅 Date handling
        # ==============================
        if hasattr(value, "strftime"):
            value = value.strftime("%d-%m-%Y")

        # ==============================
        # 💰 PROPOSED CTC (UPDATED)
        # ==============================
        if key == "proposed ctc":
            raw_value = value

            if raw_value in ["", None]:
                mapped["Proposed_CTC"] = ""
                mapped["Proposed_CTC_Words"] = ""
            else:
                try:
                    formatted, words = convert_to_words_indian(raw_value)

                    mapped["Proposed_CTC"] = formatted
                    mapped["Proposed_CTC_Words"] = words

                except Exception as e:
                    print("CTC ERROR:", e, raw_value)
                    mapped["Proposed_CTC"] = str(raw_value)
                    mapped["Proposed_CTC_Words"] = ""

            continue

        # ==============================
        # 💰 JOINING BONUS (UPDATED)
        # ==============================
        if key == "joining bonus":
            raw_value = value

            if raw_value in ["", None, 0, "0"]:
                mapped["Joining_Bonus"] = None
                mapped["Joining_Bonus_Words"] = None
            else:
                try:
                    formatted, words = convert_to_words_indian(raw_value)

                    mapped["Joining_Bonus"] = formatted
                    mapped["Joining_Bonus_Words"] = words

                except Exception as e:
                    print("BONUS ERROR:", e, raw_value)
                    mapped["Joining_Bonus"] = str(raw_value)
                    mapped["Joining_Bonus_Words"] = ""

            continue

        # ==============================
        # 🔢 DEFAULT NUMBER FORMAT
        # ==============================
        if isinstance(value, (int, float)):
            value = f"{int(value):,}"

        mapped[template_key] = str(value).strip() if value else ""

    print("MAPPED DATA:", mapped)

    return mapped