import httpx
import random
import re
import html


BASE_URL = "https://ummahapi.com/api/hadith"


def clean_html(text: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    return text.strip()


async def get_random_hadith():
    url = f"{BASE_URL}/random"

    try:
            
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()["data"]
            
    except httpx.RequestError:
        return "⚠️ تعذّر الاتصال بمصدر الاحاديث حاول مرة أخرى بعد قليل"
    except httpx.HTTPStatusError:
        return "⚠️ حدث خطأ من مصدر الاحاديث حاول مرة أخرى بعد قليل"
    
    hadith = clean_html(data["arabic"])
    hadith_number = data["hadithnumber"]

    return f"{hadith} \n\n 📜 رقم الحديث - ({hadith_number})"


async def get_random_hadith_qudsi(): 
    url = f"{BASE_URL}/qudsi?limit=50"

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        response.raise_for_status()
        payload = response.json()["data"]

    hadith_list = payload["hadiths"]
    choicen = random.choice(hadith_list)
    
    hadith_text = clean_html(choicen["arabic"]) 
    hadith_number = choicen["hadithnumber"]

    return f"{hadith_text}\n\n 📜 رقم الحديث - ({hadith_number}) | حَديث قُدسي."