import random
from pathlib import Path
import re
import json
from app.core.logger import setup_logger

logger = setup_logger()

BUKHARI_HADITHS = Path(__file__).parent / "hadiths" / "bukhari.json"
MUSLIM_HADITHS = Path(__file__).parent / "hadiths" / "muslim.json"
QUDSI_HADITHS = Path(__file__).parent / "hadiths" / "hadith_qudsi.json"


def clean_hadith_text(text: str): # To use later, now the format is good :)
    text = text.replace("\u200f", "")
    text = text.replace('"',"")
    text = text.replace('"', "").replace("\u200f", "").replace("\u200e", "")
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def _load_book(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    return {
        "hadiths": data["hadiths"],
        "chapters_map": {ch["id"]: ch["arabic"] for ch in data["chapters"]},
        "book_name": data["metadata"]["arabic"]["title"]
    }


_books = {
    "bukhari": _load_book(BUKHARI_HADITHS),
    "muslim": _load_book(MUSLIM_HADITHS)
}


def get_random_hadith():
    try:
        book_key = random.choice(list(_books.keys()))
        book_data = _books[book_key]

        hadith = random.choice(book_data["hadiths"])
        arabic_text = hadith["arabic"]
        chapter_name = book_data["chapters_map"].get(hadith["chapterId"], "")

        parts = [f"﴿ {arabic_text} ﴾"]
        if chapter_name:
            parts.append(f"📖 {chapter_name}")
        parts.append(f"{book_data["book_name"]} - رقم الحديث: {hadith["idInBook"]}")
        return "\n\n".join(parts)

    except Exception as e:
        logger.error(f"Error occurred while retrieving Hadith: {e}")
        return "عذراً، حدث خطأ بجلب الحديث، حاول مرة أخرى 🙏"


with open(QUDSI_HADITHS, encoding="utf-8") as f:
    _qudsi_hadith = json.load(f)

book_name = _qudsi_hadith["metadata"]["arabic"]["title"]
hadiths_list = _qudsi_hadith["hadiths"]
async def get_random_hadith_qudsi():
    hadith = random.choice(hadiths_list)
    arabic_text = hadith["arabic"]
    hadith_num = hadith["idInBook"]

    return f"﴿ {arabic_text} ﴾ \n\n - {book_name} - رقم الحديث: {hadith_num}"