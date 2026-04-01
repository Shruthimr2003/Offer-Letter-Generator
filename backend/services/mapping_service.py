from config.mapping import FIELD_MAPPING
from utils.number_to_words import convert_to_words_indian


BONUS_FIELDS = [
    "Joining_Bonus",
    "One_Time_Bonus",
    "Variable_Pay",
    "Notice_Period_Buyout",
    "Relocation",
]


def map_record(record: dict):
    mapped = {}

    # Normalize keys
    normalized_record = {
        k.strip().lower(): v for k, v in record.items()
    }

    for template_key, excel_key in FIELD_MAPPING.items():
        key = excel_key.strip().lower()
        raw_value = normalized_record.get(key, None)

        # ==============================
        # 📅 Date formatting
        # ==============================
        if hasattr(raw_value, "strftime"):
            raw_value = raw_value.strftime("%d-%m-%Y")

        # ==============================
        # 💰 PROPOSED CTC (NUMBER + WORDS)
        # ==============================
        if key == "proposed ctc":
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
        # 💰 JOINING BONUS (EXPLICIT HANDLING)
        # ==============================
        if key == "joining bonus":
            if raw_value in ["", None, 0, "0"]:
                mapped["Joining_Bonus"] = None
                mapped["Joining_Bonus_Words"] = None
            else:
                try:
                    formatted, words = convert_to_words_indian(raw_value)

                    mapped["Joining_Bonus"] = formatted
                    mapped["Joining_Bonus_Words"] = words

                except Exception as e:
                    print("JOINING BONUS ERROR:", e, raw_value)
                    mapped["Joining_Bonus"] = str(raw_value)
                    mapped["Joining_Bonus_Words"] = ""
            continue

        # ==============================
        # 💰 GENERIC BONUS FIELDS
        # ==============================
        if template_key in BONUS_FIELDS:
            if raw_value in ["", None, 0, "0"]:
                mapped[template_key] = None
                mapped[f"{template_key}_Words"] = None
            else:
                try:
                    formatted, words = convert_to_words_indian(raw_value)

                    mapped[template_key] = formatted
                    mapped[f"{template_key}_Words"] = words

                except Exception as e:
                    print(f"{template_key} ERROR:", e, raw_value)
                    mapped[template_key] = str(raw_value)
                    mapped[f"{template_key}_Words"] = ""
            continue

        # ==============================
        # 🔢 DEFAULT NUMBER FORMAT
        # ==============================
        if isinstance(raw_value, (int, float)):
            try:
                formatted, _ = convert_to_words_indian(raw_value)
                raw_value = formatted
            except:
                raw_value = str(raw_value)

        mapped[template_key] = str(raw_value).strip() if raw_value else ""

    # =========================================================
    # 💥 MULTIPLE RETENTION BONUS (6 MONTHS, 12 MONTHS)
    # =========================================================

    retention_list = []

    # 6 Months
    bonus_6 = normalized_record.get("retention bonus 6 months", None)
    if bonus_6 not in ["", None, 0, "0"]:
        try:
            formatted, words = convert_to_words_indian(bonus_6)

            retention_list.append({
                "amount": formatted,
                "words": words,
                "duration": "Six working months"
            })

        except Exception as e:
            print("Retention 6 ERROR:", e)

    # 12 Months
    bonus_12 = normalized_record.get("retention bonus 12 months", None)
    if bonus_12 not in ["", None, 0, "0"]:
        try:
            formatted, words = convert_to_words_indian(bonus_12)

            retention_list.append({
                "amount": formatted,
                "words": words,
                "duration": "Twelve working months"
            })

        except Exception as e:
            print("Retention 12 ERROR:", e)

    # Add to mapped
    mapped["Retention_Bonuses"] = retention_list

    print("MAPPED DATA:", mapped)

    return mapped