import asyncio
import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from app.models.schemas import TranslationRequest
from app.services.phrasebook_service import PhrasebookService


test_cases = [
    # 1. Telugu in Telugu Script -> English
    {
        "text": "నమస్కారం",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Telugu",
        "expected_is_romanized": False,
        "desc": "Telugu native script greeting -> English"
    },
    {
        "text": "మీరు ఎలా ఉన్నారు?",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Telugu",
        "expected_is_romanized": False,
        "desc": "Telugu native script phrase -> English"
    },
    # 2. Telugu in Romanized English -> English
    {
        "text": "namaskaram",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Telugu",
        "expected_is_romanized": True,
        "desc": "Telugu Romanized greeting -> English"
    },
    {
        "text": "meeru ela unnaru",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Telugu",
        "expected_is_romanized": True,
        "desc": "Telugu Romanized phrase -> English"
    },
    # 3. Hindi in Devanagari Script -> English
    {
        "text": "नमस्ते",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Hindi",
        "expected_is_romanized": False,
        "desc": "Hindi Devanagari script greeting -> English"
    },
    {
        "text": "क्या हाल है",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Hindi",
        "expected_is_romanized": False,
        "desc": "Hindi Devanagari script phrase -> English"
    },
    # 4. Hindi in Romanized English -> English
    {
        "text": "namaste",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Hindi",
        "expected_is_romanized": True,
        "desc": "Hindi Romanized greeting -> English"
    },
    {
        "text": "kya haal hai",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Hindi",
        "expected_is_romanized": True,
        "desc": "Hindi Romanized phrase -> English"
    },
    # 5. Tamil in Tamil Script -> English
    {
        "text": "வணக்கம்",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Tamil",
        "expected_is_romanized": False,
        "desc": "Tamil native script greeting -> English"
    },
    {
        "text": "நீங்கள் எப்படி இருக்கிறீர்கள்?",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Tamil",
        "expected_is_romanized": False,
        "desc": "Tamil native script phrase -> English"
    },
    # 6. Tamil in Romanized English -> English
    {
        "text": "vanakkam",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Tamil",
        "expected_is_romanized": True,
        "desc": "Tamil Romanized greeting -> English"
    },
    {
        "text": "eppadi irukkeenga",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Tamil",
        "expected_is_romanized": True,
        "desc": "Tamil Romanized phrase -> English"
    },
    # 7. English -> Telugu
    {
        "text": "Where is the train station?",
        "source": "English",
        "target": "Telugu",
        "expected_detected_lang": "English",
        "expected_is_romanized": False,
        "desc": "English input -> Telugu translation"
    },
    # 8. Cross-Indic: Romanized Telugu -> Tamil
    {
        "text": "namaskaram",
        "source": "auto",
        "target": "Tamil",
        "expected_detected_lang": "Telugu",
        "expected_is_romanized": True,
        "desc": "Romanized Telugu -> Tamil"
    },
    # 9. Cross-Indic: Romanized Hindi -> Telugu
    {
        "text": "kya haal hai",
        "source": "auto",
        "target": "Telugu",
        "expected_detected_lang": "Hindi",
        "expected_is_romanized": True,
        "desc": "Romanized Hindi -> Telugu"
    }
]

async def run_tests():
    print("=" * 80)
    print("  VOYAGE BILINGUAL & ROMANIZED TRANSLATION TEST SUITE")
    print("=" * 80)
    
    passed = 0
    total = len(test_cases)
    
    for i, tc in enumerate(test_cases, 1):
        req = TranslationRequest(
            text=tc["text"],
            source_language=tc["source"],
            target_language=tc["target"]
        )
        res = await PhrasebookService.translate_phrase(req)
        
        status = res.get("status")
        trans = res.get("translated_text", "")
        roman = res.get("romanized", "")
        det_lang = res.get("detected_source_lang", "")
        is_rom = res.get("is_romanized", False)
        
        det_ok = (det_lang.lower() == tc["expected_detected_lang"].lower())
        rom_ok = (is_rom == tc["expected_is_romanized"])
        trans_ok = bool(trans and trans != tc["text"]) or (tc["source"] == "English" and bool(trans))
        
        is_success = (status == "success") and det_ok and rom_ok and bool(trans)
        
        mark = "PASS" if is_success else "WARN/FAIL"
        if is_success:
            passed += 1
            
        print(f"\nTest {i}/{total}: [{mark}] {tc['desc']}")
        print(f"  Input:            '{tc['text']}' (Hint: '{tc['source']}') -> Target: '{tc['target']}'")
        print(f"  Detected Source:  '{det_lang}' (is_romanized={is_rom}) [Expected: '{tc['expected_detected_lang']}', rom={tc['expected_is_romanized']}]")
        print(f"  Translated Text:  '{trans}'")
        print(f"  Phonetic Pronunc: '{roman}'")
        print(f"  Speech Code:      '{res.get('speech_lang_code')}'")

    print("\n" + "=" * 80)
    print(f"  RESULTS: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(run_tests())
