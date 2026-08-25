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
    # -------------------------------------------------------------
    # 1. Telugu (Native & Romanized)
    # -------------------------------------------------------------
    {
        "text": "నమస్కారం",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Telugu",
        "expected_is_romanized": False,
        "expected_standard": "None",
        "desc": "Telugu native script greeting -> English"
    },
    {
        "text": "మీరు ఎలా ఉన్నారు?",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Telugu",
        "expected_is_romanized": False,
        "expected_standard": "None",
        "desc": "Telugu native script phrase -> English"
    },
    {
        "text": "meeru ela unnaru",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Telugu",
        "expected_is_romanized": True,
        "expected_standard": "ISO 15919 (Indic)",
        "desc": "Telugu Romanized phrase -> English"
    },
    {
        "text": "namaskaram",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Telugu",
        "expected_is_romanized": True,
        "expected_standard": "ISO 15919 (Indic)",
        "desc": "Telugu Romanized greeting -> English"
    },

    # -------------------------------------------------------------
    # 2. Hindi & Urdu (Native & Romanized)
    # -------------------------------------------------------------
    {
        "text": "नमस्ते",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Hindi",
        "expected_is_romanized": False,
        "expected_standard": "None",
        "desc": "Hindi Devanagari script greeting -> English"
    },
    {
        "text": "क्या हाल है",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Hindi",
        "expected_is_romanized": False,
        "expected_standard": "None",
        "desc": "Hindi Devanagari script phrase -> English"
    },
    {
        "text": "namaste",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Hindi",
        "expected_is_romanized": True,
        "expected_standard": "ISO 15919 (Indic)",
        "desc": "Hindi Romanized greeting -> English"
    },
    {
        "text": "kya haal hai",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Hindi",
        "expected_is_romanized": True,
        "expected_standard": "ISO 15919 (Indic)",
        "desc": "Hindi Romanized phrase -> English"
    },

    # -------------------------------------------------------------
    # 3. Tamil (Native & Romanized)
    # -------------------------------------------------------------
    {
        "text": "வணக்கம்",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Tamil",
        "expected_is_romanized": False,
        "expected_standard": "None",
        "desc": "Tamil native script greeting -> English"
    },
    {
        "text": "நீங்கள் எப்படி இருக்கிறீர்கள்?",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Tamil",
        "expected_is_romanized": False,
        "expected_standard": "None",
        "desc": "Tamil native script phrase -> English"
    },
    {
        "text": "vanakkam",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Tamil",
        "expected_is_romanized": True,
        "expected_standard": "ISO 15919 (Indic)",
        "desc": "Tamil Romanized greeting -> English"
    },
    {
        "text": "eppadi irukkeenga",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Tamil",
        "expected_is_romanized": True,
        "expected_standard": "ISO 15919 (Indic)",
        "desc": "Tamil Romanized phrase -> English"
    },

    # -------------------------------------------------------------
    # 4. Kannada & Malayalam
    # -------------------------------------------------------------
    {
        "text": "ನಮಸ್ಕಾರ",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Kannada",
        "expected_is_romanized": False,
        "expected_standard": "None",
        "desc": "Kannada native script greeting -> English"
    },
    {
        "text": "hegiddira",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Kannada",
        "expected_is_romanized": True,
        "expected_standard": "ISO 15919 (Indic)",
        "desc": "Kannada Romanized phrase -> English"
    },
    {
        "text": "സുഖമാണോ?",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Malayalam",
        "expected_is_romanized": False,
        "expected_standard": "None",
        "desc": "Malayalam native script phrase -> English"
    },
    {
        "text": "sukhamano",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Malayalam",
        "expected_is_romanized": True,
        "expected_standard": "ISO 15919 (Indic)",
        "desc": "Malayalam Romanized phrase -> English"
    },

    # -------------------------------------------------------------
    # 5. Gujarati, Punjabi, Bengali
    # -------------------------------------------------------------
    {
        "text": "કેમ છો?",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Gujarati",
        "expected_is_romanized": False,
        "expected_standard": "None",
        "desc": "Gujarati native script phrase -> English"
    },
    {
        "text": "kem cho",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Gujarati",
        "expected_is_romanized": True,
        "expected_standard": "ISO 15919 (Indic)",
        "desc": "Gujarati Romanized phrase -> English"
    },
    {
        "text": "sat sri akaal",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Punjabi",
        "expected_is_romanized": True,
        "expected_standard": "ISO 15919 (Indic)",
        "desc": "Punjabi Romanized greeting -> English"
    },
    {
        "text": "kemon achen",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Bengali",
        "expected_is_romanized": True,
        "expected_standard": "ISO 15919 (Indic)",
        "desc": "Bengali Romanized phrase -> English"
    },

    # -------------------------------------------------------------
    # 6. Global Languages: Mandarin, Japanese, Korean, Arabic, Russian
    # -------------------------------------------------------------
    {
        "text": "你好",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Mandarin Chinese",
        "expected_is_romanized": False,
        "expected_standard": "None",
        "desc": "Mandarin Hanzi native greeting -> English"
    },
    {
        "text": "ni hao",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Mandarin Chinese",
        "expected_is_romanized": True,
        "expected_standard": "Hanyu Pinyin",
        "desc": "Mandarin Pinyin greeting -> English"
    },
    {
        "text": "こんにちは",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Japanese",
        "expected_is_romanized": False,
        "expected_standard": "None",
        "desc": "Japanese Kana native greeting -> English"
    },
    {
        "text": "arigatou gozaimasu",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Japanese",
        "expected_is_romanized": True,
        "expected_standard": "Hepburn Romaji",
        "desc": "Japanese Romaji greeting -> English"
    },
    {
        "text": "안녕하세요",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Korean",
        "expected_is_romanized": False,
        "expected_standard": "None",
        "desc": "Korean Hangul native greeting -> English"
    },
    {
        "text": "annyeonghaseyo",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Korean",
        "expected_is_romanized": True,
        "expected_standard": "Revised Romanization (RR)",
        "desc": "Korean Revised Romanization greeting -> English"
    },
    {
        "text": "شكرا",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Arabic",
        "expected_is_romanized": False,
        "expected_standard": "None",
        "desc": "Arabic script native greeting -> English"
    },
    {
        "text": "shukran jazilan",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Arabic",
        "expected_is_romanized": True,
        "expected_standard": "Arabizi / ALA-LC",
        "desc": "Arabic Arabizi phrase -> English"
    },
    {
        "text": "Привет",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Russian",
        "expected_is_romanized": False,
        "expected_standard": "None",
        "desc": "Russian Cyrillic native greeting -> English"
    },
    {
        "text": "spasibo",
        "source": "auto",
        "target": "English",
        "expected_detected_lang": "Russian",
        "expected_is_romanized": True,
        "expected_standard": "Cyrillic Translit (BGN/PCGN)",
        "desc": "Russian Translit greeting -> English"
    },

    # -------------------------------------------------------------
    # 7. Authentic English Sentences (Must Never be misidentified as Indic)
    # -------------------------------------------------------------
    {
        "text": "Where is the train station?",
        "source": "auto",
        "target": "Telugu",
        "expected_detected_lang": "English",
        "expected_is_romanized": False,
        "expected_standard": "None",
        "desc": "English input sentence -> Telugu translation"
    },
    {
        "text": "Please bring the bill and drinking water",
        "source": "auto",
        "target": "Hindi",
        "expected_detected_lang": "English",
        "expected_is_romanized": False,
        "expected_standard": "None",
        "desc": "English sentence with stopwords -> Hindi translation"
    },

    # -------------------------------------------------------------
    # 8. Cross-Language & Bidirectional Pairs
    # -------------------------------------------------------------
    {
        "text": "namaskaram",
        "source": "auto",
        "target": "Tamil",
        "expected_detected_lang": "Telugu",
        "expected_is_romanized": True,
        "expected_standard": "ISO 15919 (Indic)",
        "desc": "Cross-Indic: Romanized Telugu -> Tamil"
    },
    {
        "text": "kya haal hai",
        "source": "auto",
        "target": "Telugu",
        "expected_detected_lang": "Hindi",
        "expected_is_romanized": True,
        "expected_standard": "ISO 15919 (Indic)",
        "desc": "Cross-Indic: Romanized Hindi -> Telugu"
    },
    {
        "text": "Where is the nearest hospital?",
        "source": "English",
        "target": "Japanese",
        "expected_detected_lang": "English",
        "expected_is_romanized": False,
        "expected_standard": "None",
        "desc": "English input -> Japanese translation"
    }
]

async def run_tests():
    print("=" * 80)
    print("  VOYAGE UNIVERSAL MULTILINGUAL & TRANSLITERATION TEST SUITE")
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
        std = res.get("transliteration_standard", "None")
        conf = res.get("confidence", 0.0)
        cands = res.get("candidates", [])
        
        det_ok = (det_lang.lower() == tc["expected_detected_lang"].lower())
        rom_ok = (is_rom == tc["expected_is_romanized"])
        std_ok = (std == tc["expected_standard"])
        trans_ok = bool(trans and (trans != tc["text"] or tc["source"].lower() == tc["target"].lower()))
        
        is_success = (status == "success") and det_ok and rom_ok and std_ok and trans_ok
        
        mark = "PASS" if is_success else "WARN/FAIL"
        if is_success:
            passed += 1
            
        print(f"\nTest {i:02d}/{total:02d}: [{mark}] {tc['desc']}")
        print(f"  Input:            '{tc['text']}' (Hint: '{tc['source']}') -> Target: '{tc['target']}'")
        print(f"  Detected Source:  '{det_lang}' (is_romanized={is_rom}, std='{std}', conf={conf})")
        print(f"  Expected:         '{tc['expected_detected_lang']}' (is_romanized={tc['expected_is_romanized']}, std='{tc['expected_standard']}')")
        print(f"  Translated Text:  '{trans}'")
        print(f"  Pronunciation:    '{roman}'")
        print(f"  Speech Code:      '{res.get('speech_lang_code')}'")
        if res.get("is_ambiguous"):
            print(f"  Ambiguity Notice: Candidates = {[c['language'] for c in cands]}")

    print("\n" + "=" * 80)
    print(f"  RESULTS: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    print("=" * 80)
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(run_tests())
    sys.exit(0 if success else 1)
