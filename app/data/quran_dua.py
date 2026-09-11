import random
import json
from pathlib import Path 


DUAS_FILE = Path(__file__).parent / "quran_dua.json"

with open(DUAS_FILE, encoding="utf-8") as f:
    _duas_data = json.load(f)

def get_random_dua():
    dua_list = _duas_data["quranic_duas"]
    dua = random.choice(dua_list)

    ayah = dua["arabic"]
    surah = dua["surah"]
    ayah_number = str(dua["ayah"])

    format_text = f"﴿ {ayah} ﴾ \n\n- {surah} ({ayah_number})"
    return format_text