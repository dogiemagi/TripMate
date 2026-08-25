import sys
import httpx

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

tests = [
    ('Meeru ela unnaaru', 'Telugu (తెలుగు)', 'English'),
    ('Eppadi irukkeenga', 'Tamil (தமிழ்)', 'English'),
    ('Aap kaise hain', 'Hindi (हिन्दी)', 'English'),
    ('Where is the station?', 'English', 'Telugu (తెలుగు)')
]

for text, src, tgt in tests:
    r = httpx.post('http://localhost:8000/api/v1/phrasebook/translate', json={'text': text, 'source_language': src, 'target_language': tgt})
    d = r.json()
    trans_esc = d.get('translated_text', '').encode('unicode_escape').decode('utf-8')
    print(f"[{src} -> {tgt}] '{text}'")
    print(f"  => Translated: '{trans_esc}'")
    print(f"  => Romanized:  '{d.get('romanized')}'")
    print("-" * 40)
