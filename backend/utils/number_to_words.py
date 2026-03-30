from num2words import num2words


def format_indian_number(num):
    num = int(num)
    s = str(num)

    last3 = s[-3:]
    rest = s[:-3]

    if rest != "":
        rest = rest[::-1]
        parts = [rest[i:i+2] for i in range(0, len(rest), 2)]
        rest = ",".join(parts)[::-1]
        return rest + "," + last3
    else:
        return last3


def convert_to_words_indian(number):
    try:
        # ✅ Clean input (handles "10,00,000")
        clean_value = str(number).replace(",", "").strip()
        num = int(float(clean_value))

        # ✅ Format number (Indian format)
        formatted_number = format_indian_number(num)

        # ✅ Convert to words
        words = num2words(num, lang='en_IN')
        words = words.replace(",", "").strip()

        # ✅ Fix plural
        words = words.replace("lakh", "lakhs").replace("crore", "crores")

        words = "Rupees " + words.title() + " Only"

        return formatted_number, words

    except Exception as e:
        print("CONVERSION ERROR:", e)
        return "", ""