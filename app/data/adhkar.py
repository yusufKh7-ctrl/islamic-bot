import json
from pathlib import Path
import random


ADKAR_FILE = Path(__file__).parent / "adhkar.json"

with open(ADKAR_FILE, encoding="utf-8") as f:
    _adkar_data = json.load(f)

def format_adhkar_list(duas: list, title: str) -> str:
    parts = [title]
    for i, dua in enumerate(duas, start=1):
        arabic = dua["arabic"]
        repeat = dua["repeat"]
        repeat_text = f" ({repeat}x)" if repeat > 1 else ""
        parts.append(f"\n\n{i}. ﴿ {arabic} ﴾{repeat_text}")
    return "\n\n".join(parts)


def morning_adhkar():
    duas = _adkar_data["data"]["morning"]
    title = "🌅 *أذكار الصباح:*"
    return format_adhkar_list(duas, title)


def evening_adhkar():
    duas = _adkar_data["data"]["evening"]
    title = "🌃 *أذكار المساء:*"
    return format_adhkar_list(duas, title)


def general_adhkar():
    zikr_list =  _adkar_data["data"]["general"]
    zikr = random.choice(zikr_list)

    arabic = zikr["arabic"]
    repeat = zikr["repeat"]
    
    repeat_text = f"\n ({repeat}x)" if repeat > 1 else ""
    desc = zikr["description"]
    desc_text = f"\n\n- {desc}" if desc else ""

    return f"﴿ {arabic} ﴾ {repeat_text} {desc_text}"
