import csv

def load_cefr_frequency_data(csv_path: str = "data/merged_cefr_frequency.csv") -> dict:
    data = {}
    try:
        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                word = row["Word"].strip().lower()
                data[word] = {
                    "cefr": row.get("CEFR", "").strip().upper(),
                    "frequency": row.get("Frequency", "").strip(),
                }
    except Exception:
        # If file is missing or invalid, just return empty dict
        return {}
    return data

CEFR_FREQUENCY_DATA = load_cefr_frequency_data() 