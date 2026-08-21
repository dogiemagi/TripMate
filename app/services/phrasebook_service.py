import logging
from typing import Dict, Any, List
from app.models.schemas import PhrasebookQuery

logger = logging.getLogger("voyage.phrasebook")

PHRASEBOOK_DATA = {
    "japanese": [
        {"category": "Greetings", "english": "Hello / Good day", "foreign": "こんにちは", "romanized": "Konnichiwa", "audio_text": "こんにちは"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "ありがとうございます", "romanized": "Arigatou gozaimasu", "audio_text": "ありがとうございます"},
        {"category": "Dining", "english": "Excuse me / Server please", "foreign": "すみません", "romanized": "Sumimasen", "audio_text": "すみません"},
        {"category": "Dining", "english": "Check please", "foreign": "お会計をお願いします", "romanized": "Okaikei o onegaishimasu", "audio_text": "お会計をお願いします"},
        {"category": "Dining", "english": "Delicious! (compliment to chef)", "foreign": "とても美味しいです！", "romanized": "Totemo oishii desu!", "audio_text": "とても美味しいです"},
        {"category": "Transport", "english": "Where is the train station?", "foreign": "駅はどこですか？", "romanized": "Eki wa doko desu ka?", "audio_text": "駅はどこですか"},
        {"category": "Emergency", "english": "Please help me", "foreign": "助けてください", "romanized": "Tasukete kudasai", "audio_text": "助けてください"}
    ],
    "italian": [
        {"category": "Greetings", "english": "Good morning / Hello", "foreign": "Buongiorno", "romanized": "Bwon-JOR-noh", "audio_text": "Buongiorno"},
        {"category": "Greetings", "english": "Thank you so much", "foreign": "Grazie mille", "romanized": "GRAHT-syeh MEE-leh", "audio_text": "Grazie mille"},
        {"category": "Dining", "english": "A table for two, please", "foreign": "Un tavolo per due, per favore", "romanized": "Oon TAH-voh-loh pair DOO-eh, pair fah-VOH-reh", "audio_text": "Un tavolo per due, per favore"},
        {"category": "Dining", "english": "The bill, please", "foreign": "Il conto, per favore", "romanized": "Eel KOHN-toh, pair fah-VOH-reh", "audio_text": "Il conto, per favore"},
        {"category": "Transport", "english": "Where is the subway/station?", "foreign": "Dov'è la stazione?", "romanized": "Doh-VEH lah stah-TSYOH-neh?", "audio_text": "Dov'è la stazione"},
        {"category": "Emergency", "english": "I need a doctor", "foreign": "Ho bisogno di un medico", "romanized": "Oh bee-ZOHN-yoh dee oon MEH-dee-koh", "audio_text": "Ho bisogno di un medico"}
    ],
    "french": [
        {"category": "Greetings", "english": "Hello / Good day", "foreign": "Bonjour", "romanized": "Bon-ZHOOR", "audio_text": "Bonjour"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "Merci beaucoup", "romanized": "Mair-SEE boh-KOO", "audio_text": "Merci beaucoup"},
        {"category": "Dining", "english": "The menu, please", "foreign": "La carte, s'il vous plaît", "romanized": "Lah kart, seel voo pleh", "audio_text": "La carte, s'il vous plaît"},
        {"category": "Dining", "english": "The check, please", "foreign": "L'addition, s'il vous plaît", "romanized": "Lah-dee-SYOHN, seel voo pleh", "audio_text": "L'addition, s'il vous plaît"},
        {"category": "Transport", "english": "Where is the metro?", "foreign": "Où est le métro ?", "romanized": "Oo eh luh meh-troh?", "audio_text": "Où est le métro"},
        {"category": "Emergency", "english": "Help!", "foreign": "Au secours !", "romanized": "Oh suh-KOOR!", "audio_text": "Au secours"}
    ],
    "spanish": [
        {"category": "Greetings", "english": "Hello / Good afternoon", "foreign": "¡Hola! Buenas tardes", "romanized": "OH-lah! BWEH-nahs TAR-des", "audio_text": "Hola! Buenas tardes"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "Muchas gracias", "romanized": "MOO-chahs GRAH-syahs", "audio_text": "Muchas gracias"},
        {"category": "Dining", "english": "The bill, please", "foreign": "La cuenta, por favor", "romanized": "Lah KWEN-tah, por fah-VOR", "audio_text": "La cuenta, por favor"},
        {"category": "Dining", "english": "Do you have vegetarian options?", "foreign": "¿Tienen opciones vegetarianas?", "romanized": "TYEH-nen op-SYOH-nes veh-heh-tah-RYAH-nahs?", "audio_text": "Tienen opciones vegetarianas"},
        {"category": "Transport", "english": "How much does it cost to get to...?", "foreign": "¿Cuánto cuesta ir a...?", "romanized": "KWAN-toh KWES-tah eer ah...?", "audio_text": "Cuánto cuesta ir a"},
        {"category": "Emergency", "english": "Help me, please", "foreign": "Ayúdeme, por favor", "romanized": "ah-YOO-deh-meh, por fah-VOR", "audio_text": "Ayúdeme, por favor"}
    ]
}

LANGUAGE_CODES = {
    "japanese": "ja-JP",
    "italian": "it-IT",
    "french": "fr-FR",
    "spanish": "es-ES",
    "german": "de-DE",
    "hindi": "hi-IN",
    "arabic": "ar-SA"
}

class PhrasebookService:
    @staticmethod
    def get_phrases(query: PhrasebookQuery) -> Dict[str, Any]:
        lang_key = query.language.strip().lower()
        phrases = PHRASEBOOK_DATA.get(lang_key, PHRASEBOOK_DATA["japanese"])

        if query.category and query.category.lower() != "all":
            cat_filter = query.category.strip().lower()
            phrases = [p for p in phrases if p["category"].lower() == cat_filter]

        return {
            "status": "success",
            "language": query.language.title(),
            "speech_lang_code": LANGUAGE_CODES.get(lang_key, "en-US"),
            "total_phrases": len(phrases),
            "phrases": phrases
        }
