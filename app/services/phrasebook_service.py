import logging
from typing import Dict, Any, List
from app.models.schemas import PhrasebookQuery

logger = logging.getLogger("voyage.phrasebook")

PHRASEBOOK_DATA = {
    "hindi": [
        {"category": "Greetings", "english": "Hello / Greetings", "foreign": "नमस्ते", "romanized": "Namaste", "audio_text": "नमस्ते"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "बहुत बहुत धन्यवाद", "romanized": "Bahut bahut dhanyavaad", "audio_text": "बहुत बहुत धन्यवाद"},
        {"category": "Dining", "english": "How much does this cost?", "foreign": "यह कितने का है?", "romanized": "Yeh kitne ka hai?", "audio_text": "यह कितने का है?"},
        {"category": "Dining", "english": "Please bring the food / bill", "foreign": "कृपया बिल ले आइए", "romanized": "Kripya bill le aaiye", "audio_text": "कृपया बिल ले आइए"},
        {"category": "Dining", "english": "The food is very delicious", "foreign": "खाना बहुत स्वादिष्ट है", "romanized": "Khaana bahut swaadisht hai", "audio_text": "खाना बहुत स्वादिष्ट है"},
        {"category": "Transport", "english": "Where is the railway station / bus stand?", "foreign": "रेलवे स्टेशन कहाँ है?", "romanized": "Railway station kahan hai?", "audio_text": "रेलवे स्टेशन कहाँ है?"},
        {"category": "Emergency", "english": "Please help me", "foreign": "कृपया मेरी मदद कीजिए", "romanized": "Kripya meri madad kijiye", "audio_text": "कृपया मेरी मदद कीजिए"},
        {"category": "Shopping", "english": "Can you give a discount?", "foreign": "क्या थोड़ा कम हो सकता है?", "romanized": "Kya thoda kam ho sakta hai?", "audio_text": "क्या थोड़ा कम हो सकता है?"}
    ],
    "tamil": [
        {"category": "Greetings", "english": "Hello / Greetings", "foreign": "வணக்கம்", "romanized": "Vanakkam", "audio_text": "வணக்கம்"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "மிக்க நன்றி", "romanized": "Mikka Nandri", "audio_text": "மிக்க நன்றி"},
        {"category": "Dining", "english": "The food is very tasty", "foreign": "சாப்பாடு மிகவும் சுவையாக இருக்கிறது", "romanized": "Saapaadu migavum suvaiyaaga irukkiradhu", "audio_text": "சாப்பாடு மிகவும் சுவையாக இருக்கிறது"},
        {"category": "Dining", "english": "Please bring the bill", "foreign": "பில் கொண்டு வாருங்கள்", "romanized": "Bill kondu vaarungal", "audio_text": "பில் கொண்டு வாருங்கள்"},
        {"category": "Transport", "english": "Where is the bus stand / station?", "foreign": "பேருந்து நிலையம் எங்கே உள்ளது?", "romanized": "Perundhu nilayam engae ulladhu?", "audio_text": "பேருந்து நிலையம் எங்கே உள்ளது?"},
        {"category": "Emergency", "english": "Please help me", "foreign": "தயவுசெய்து எனக்கு உதவுங்கள்", "romanized": "Dhayavuseidhu enakku udhavungal", "audio_text": "தயவுசெய்து எனக்கு உதவுங்கள்"},
        {"category": "Shopping", "english": "How much is this?", "foreign": "இதன் விலை என்ன?", "romanized": "Idhan vilai enna?", "audio_text": "இதன் விலை என்ன?"}
    ],
    "telugu": [
        {"category": "Greetings", "english": "Hello / Greetings", "foreign": "నమస్కారం", "romanized": "Namaskaram", "audio_text": "నమస్కారం"},
        {"category": "Greetings", "english": "Thank you", "foreign": "చాలా ధన్యవాదాలు", "romanized": "Chaala Dhanyavaadaalu", "audio_text": "చాలా ధన్యవాదాలు"},
        {"category": "Dining", "english": "The food is very good", "foreign": "భోజనం చాలా బాగుంది", "romanized": "Bhojanam chaala baagundi", "audio_text": "భోజనం చాలా బాగుంది"},
        {"category": "Dining", "english": "Please bring water / bill", "foreign": "దయచేసి బిల్ ఇవ్వండి", "romanized": "Dayachesi bill ivvandi", "audio_text": "దయచేసి బిల్ ఇవ్వండి"},
        {"category": "Transport", "english": "Where is the station / road?", "foreign": "స్టేషన్ ఎక్కడ ఉంది?", "romanized": "Station ekkada undi?", "audio_text": "స్టేషన్ ఎక్కడ ఉంది?"},
        {"category": "Emergency", "english": "Please help me", "foreign": "దయచేసి నాకు సహాయం చేయండి", "romanized": "Dayachesi naaku sahaayam cheyandi", "audio_text": "దయచేసి నాకు సహాయం చేయండి"},
        {"category": "Shopping", "english": "How much does this cost?", "foreign": "ఇది ఎంత?", "romanized": "Idi entha?", "audio_text": "ఇది ఎంత?"}
    ],
    "urdu": [
        {"category": "Greetings", "english": "Hello / Peace be upon you", "foreign": "السلام علیکم", "romanized": "Assalam-o-Alaikum", "audio_text": "السلام علیکم"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "بہت بہت شکریہ", "romanized": "Bahut bahut shukriya", "audio_text": "بہت بہت شکریہ"},
        {"category": "Dining", "english": "The food is extremely delicious", "foreign": "کھانا بہت لذیذ ہے", "romanized": "Khaana bahut lazeez hai", "audio_text": "کھانا بہت لذیذ ہے"},
        {"category": "Dining", "english": "Please bring the bill", "foreign": "براہ کرم بل لائیں", "romanized": "Barahe-karam bill laayen", "audio_text": "براہ کرم بل لائیں"},
        {"category": "Transport", "english": "Where is the station?", "foreign": "اسٹیشن کہاں ہے؟", "romanized": "Station kahan hai?", "audio_text": "اسٹیشن کہاں ہے؟"},
        {"category": "Emergency", "english": "Please help me", "foreign": "براہ کرم میری مدد کریں", "romanized": "Barahe-karam meri madad karen", "audio_text": "براہ کرم میری مدد کریں"},
        {"category": "Shopping", "english": "What is the price of this?", "foreign": "اس کی قیمت کیا ہے؟", "romanized": "Is ki qeemat kya hai?", "audio_text": "اس کی قیمت کیا ہے؟"}
    ],
    "bengali": [
        {"category": "Greetings", "english": "Hello / Greetings", "foreign": "নমস্কার", "romanized": "Nomoshkar", "audio_text": "নমস্কার"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "অনেক ধন্যবাদ", "romanized": "Onek Dhonnobad", "audio_text": "অনেক ধন্যবাদ"},
        {"category": "Dining", "english": "The food is very tasty", "foreign": "খাবারটা খুব সুস্বাদু", "romanized": "Khabarta khub shushwadu", "audio_text": "খাবারটা খুব সুস্বাদু"},
        {"category": "Transport", "english": "Where is the station / stop?", "foreign": "স্টেশনটি কোথায়?", "romanized": "Station-ti kothay?", "audio_text": "স্টেশনটি কোথায়?"},
        {"category": "Emergency", "english": "Please help me", "foreign": "দয়া করে আমাকে সাহায্য করুন", "romanized": "Doya kore amake sahajjo korun", "audio_text": "দয়া করে আমাকে সাহায্য করুন"},
        {"category": "Shopping", "english": "What is the price?", "foreign": "এটার দাম কত?", "romanized": "Etar daam koto?", "audio_text": "এটার দাম কত?"}
    ],
    "marathi": [
        {"category": "Greetings", "english": "Hello / Greetings", "foreign": "नमस्कार", "romanized": "Namaskar", "audio_text": "नमस्कार"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "खूप खूप धन्यवाद", "romanized": "Khoop khoop dhanyavaad", "audio_text": "खूप खूप धन्यवाद"},
        {"category": "Dining", "english": "Food is very delicious", "foreign": "जेवण खूप छान आहे", "romanized": "Jevan khoop chhaan aahe", "audio_text": "जेवण खूप छान आहे"},
        {"category": "Transport", "english": "Where is the station?", "foreign": "स्टेशन कुठे आहे?", "romanized": "Station kuthe aahe?", "audio_text": "स्टेशन कुठे आहे?"},
        {"category": "Emergency", "english": "Please help me", "foreign": "कृपया मला मदत करा", "romanized": "Kripya mala madat kara", "audio_text": "कृपया मला मदत करा"},
        {"category": "Shopping", "english": "How much for this?", "foreign": "याची किंमत काय आहे?", "romanized": "Yaachi kimmat kaay aahe?", "audio_text": "याची किंमत काय आहे?"}
    ],
    "japanese": [
        {"category": "Greetings", "english": "Hello / Good day", "foreign": "こんにちは", "romanized": "Konnichiwa", "audio_text": "こんにちは"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "ありがとうございます", "romanized": "Arigatou gozaimasu", "audio_text": "ありがとうございます"},
        {"category": "Dining", "english": "Excuse me / Server please", "foreign": "すみません", "romanized": "Sumimasen", "audio_text": "すみません"},
        {"category": "Dining", "english": "Check please", "foreign": "お会計をお願いします", "romanized": "Okaikei o onegaishimasu", "audio_text": "お会計をお願いします"},
        {"category": "Dining", "english": "Delicious! (compliment to chef)", "foreign": "とても美味しいです！", "romanized": "Totemo oishii desu!", "audio_text": "とても美味しいです"},
        {"category": "Transport", "english": "Where is the train station?", "foreign": "駅はどこですか？", "romanized": "Eki wa doko desu ka?", "audio_text": "駅はどこですか"},
        {"category": "Emergency", "english": "Please help me", "foreign": "助けてください", "romanized": "Tasukete kudasai", "audio_text": "助けてください"}
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
        {"category": "Transport", "english": "Where is the station?", "foreign": "¿Dónde está la estación?", "romanized": "DOHN-deh ehs-TAH lah ehs-tah-SYOHN?", "audio_text": "Dónde está la estación"},
        {"category": "Emergency", "english": "Help me, please", "foreign": "Ayúdeme, por favor", "romanized": "ah-YOO-deh-meh, por fah-VOR", "audio_text": "Ayúdeme, por favor"}
    ],
    "italian": [
        {"category": "Greetings", "english": "Good morning / Hello", "foreign": "Buongiorno", "romanized": "Bwon-JOR-noh", "audio_text": "Buongiorno"},
        {"category": "Greetings", "english": "Thank you so much", "foreign": "Grazie mille", "romanized": "GRAHT-syeh MEE-leh", "audio_text": "Grazie mille"},
        {"category": "Dining", "english": "A table for two, please", "foreign": "Un tavolo per due, per favore", "romanized": "Oon TAH-voh-loh pair DOO-eh, pair fah-VOH-reh", "audio_text": "Un tavolo per due, per favore"},
        {"category": "Dining", "english": "The bill, please", "foreign": "Il conto, per favore", "romanized": "Eel KOHN-toh, pair fah-VOH-reh", "audio_text": "Il conto, per favore"},
        {"category": "Transport", "english": "Where is the station?", "foreign": "Dov'è la stazione?", "romanized": "Doh-VEH lah stah-TSYOH-neh?", "audio_text": "Dov'è la stazione"},
        {"category": "Emergency", "english": "I need a doctor", "foreign": "Ho bisogno di un medico", "romanized": "Oh bee-ZOHN-yoh dee oon MEH-dee-koh", "audio_text": "Ho bisogno di un medico"}
    ],
    "german": [
        {"category": "Greetings", "english": "Hello / Good day", "foreign": "Guten Tag", "romanized": "GOO-ten tahk", "audio_text": "Guten Tag"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "Vielen Dank", "romanized": "FEE-len dahnk", "audio_text": "Vielen Dank"},
        {"category": "Dining", "english": "The bill, please", "foreign": "Die Rechnung, bitte", "romanized": "Dee REKH-noong, BIH-tuh", "audio_text": "Die Rechnung, bitte"},
        {"category": "Transport", "english": "Where is the station?", "foreign": "Wo ist der Bahnhof?", "romanized": "Voh ist der BAHN-hohf?", "audio_text": "Wo ist der Bahnhof"},
        {"category": "Emergency", "english": "Help, please!", "foreign": "Hilfe, bitte!", "romanized": "HIL-fuh, BIH-tuh!", "audio_text": "Hilfe, bitte"}
    ]
}

LANGUAGE_CODES = {
    "hindi": "hi-IN",
    "tamil": "ta-IN",
    "telugu": "te-IN",
    "urdu": "ur-IN",
    "bengali": "bn-IN",
    "marathi": "mr-IN",
    "japanese": "ja-JP",
    "italian": "it-IT",
    "french": "fr-FR",
    "spanish": "es-ES",
    "german": "de-DE",
    "arabic": "ar-SA"
}

class PhrasebookService:
    @staticmethod
    def get_phrases(query: PhrasebookQuery) -> Dict[str, Any]:
        lang_key = query.language.strip().lower()
        phrases = PHRASEBOOK_DATA.get(lang_key, PHRASEBOOK_DATA["hindi"])

        if query.category and query.category.lower() != "all":
            cat_filter = query.category.strip().lower()
            phrases = [p for p in phrases if p["category"].lower() == cat_filter]

        return {
            "status": "success",
            "language": query.language.title(),
            "speech_lang_code": LANGUAGE_CODES.get(lang_key, "hi-IN"),
            "total_phrases": len(phrases),
            "phrases": phrases
        }
