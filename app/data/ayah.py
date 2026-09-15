import httpx
import random

BASE_URL = "https://api.alquran.cloud/v1"

async def get_random_ayah():
    ayah_number = random.randint(1, 6236)
    url = f"{BASE_URL}/ayah/{ayah_number}/editions/quran-simple,ar.muyassar"

    try:
        async with httpx.AsyncClient(timeout=10) as clinet:
            response = await clinet.get(url)
            response.raise_for_status()
            data = response.json()["data"]
    except httpx.RequestError:
        return "⚠️ تعذّر الاتصال بمصدر الآيات، حاول مرة أخرى بعد قليل."
    except httpx.HTTPStatusError:
        return "⚠️ حدث خطأ من مصدر الآيات، حاول مرة أخرى بعد قليل."

    ayah_data = data[0]
    tafsir_data = data[1]

    surah_name = ayah_data["surah"]["name"]
    ayah_text = ayah_data["text"]
    tafsir_text = tafsir_data["text"]
    ayah_number_in_surah = ayah_data["numberInSurah"]
    return (f"﴿ {ayah_text} ﴾\n\n📖"
            f"<b>{surah_name}</b> - الآية ({ayah_number_in_surah})\n\n"
            f"<b>تفسير الميسّر:</b>\n{tafsir_text}"
        )
