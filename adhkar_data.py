
import json
with open('app/data/hadith_qudsi.json', encoding='utf-8') as f:
    data = json.load(f)
with open('app/data/hadith_qudsi_pretty.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
