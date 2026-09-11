import httpx
import random

BASE_URL = "https://api.alquran.cloud/v1"

async def get_random_ayah(edition="quran-uthmani"):
    ayah_number = random.randint(1, 6236)
    url = f"{BASE_URL}/ayah/{ayah_number}/{edition}"

    try:
        async with httpx.AsyncClient(timeout=10) as clinet:
            response = await clinet.get(url)
            response.raise_for_status()
            data = response.json()["data"]
    except httpx.RequestError:
        return "⚠️ تعذّر الاتصال بمصدر الآيات، حاول مرة أخرى بعد قليل."
    except httpx.HTTPStatusError:
        return "⚠️ حدث خطأ من مصدر الآيات، حاول مرة أخرى بعد قليل."
    
    surah_name = data["surah"]["name"]
    ayah_text = data["text"]
    ayah_number_in_surah = data["numberInSurah"]
    return f"﴿ {ayah_text} ﴾\n\n📖 {surah_name} - الآية ({ayah_number_in_surah})"
