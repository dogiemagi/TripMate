import logging
from typing import Dict, Any, List
from app.models.schemas import PhrasebookQuery

logger = logging.getLogger("voyage.phrasebook")

PHRASEBOOK_DATA = {
    "hindi": [
        {"category": "Greetings", "english": "Hello / Greetings", "foreign": "नमस्ते", "romanized": "Namaste", "audio_text": "नमस्ते"},
        {"category": "Greetings", "english": "Good morning", "foreign": "शुभ प्रभात", "romanized": "Shubh Prabhaat", "audio_text": "शुभ प्रभात"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "बहुत बहुत धन्यवाद", "romanized": "Bahut bahut dhanyavaad", "audio_text": "बहुत बहुत धन्यवाद"},
        {"category": "Greetings", "english": "How are you?", "foreign": "आप कैसे हैं?", "romanized": "Aap kaise hain?", "audio_text": "आप कैसे हैं?"},
        {"category": "Greetings", "english": "I am doing well, thank you", "foreign": "मैं ठीक हूँ, धन्यवाद", "romanized": "Main theek hoon, dhanyavaad", "audio_text": "मैं ठीक हूँ धन्यवाद"},
        {"category": "Greetings", "english": "See you again / Goodbye", "foreign": "फिर मिलेंगे", "romanized": "Phir milenge", "audio_text": "फिर मिलेंगे"},
        {"category": "Dining", "english": "How much does this cost?", "foreign": "यह कितने का है?", "romanized": "Yeh kitne ka hai?", "audio_text": "यह कितने का है?"},
        {"category": "Dining", "english": "Please bring the bill / check", "foreign": "कृपया बिल ले आइए", "romanized": "Kripya bill le aaiye", "audio_text": "कृपया बिल ले आइए"},
        {"category": "Dining", "english": "The food is very delicious", "foreign": "खाना बहुत स्वादिष्ट है", "romanized": "Khaana bahut swaadisht hai", "audio_text": "खाना बहुत स्वादिष्ट है"},
        {"category": "Dining", "english": "Is this dish vegetarian?", "foreign": "क्या यह शाकाहारी खाना है?", "romanized": "Kya yeh shakahari khana hai?", "audio_text": "क्या यह शाकाहारी खाना है?"},
        {"category": "Dining", "english": "Please make it less spicy", "foreign": "कृपया कम तीखा बनाइए", "romanized": "Kripya kam teekha banaiye", "audio_text": "कृपया कम तीखा बनाइए"},
        {"category": "Dining", "english": "Please give me drinking water", "foreign": "कृपया पीने का पानी दीजिए", "romanized": "Kripya peene ka paani dijiye", "audio_text": "कृपया पीने का पानी दीजिए"},
        {"category": "Dining", "english": "Can I have one cup of tea?", "foreign": "एक कप चाय मिलेगी?", "romanized": "Ek cup chai milegi?", "audio_text": "एक कप चाय मिलेगी?"},
        {"category": "Transport", "english": "Where is the railway station / bus stand?", "foreign": "रेलवे स्टेशन कहाँ है?", "romanized": "Railway station kahan hai?", "audio_text": "रेलवे स्टेशन कहाँ है?"},
        {"category": "Transport", "english": "Please turn on the taxi meter", "foreign": "कृपया मीटर चालू कीजिए", "romanized": "Kripya meter chaaloo kijiye", "audio_text": "कृपया मीटर चालू कीजिए"},
        {"category": "Transport", "english": "I want to go to this address", "foreign": "मुझे इस पते पर जाना है", "romanized": "Mujhe is pate par jaana hai", "audio_text": "मुझे इस पते पर जाना है"},
        {"category": "Transport", "english": "How far is the airport?", "foreign": "हवाई अड्डा कितनी दूर है?", "romanized": "Hawai adda kitni door hai?", "audio_text": "हवाई अड्डा कितनी दूर है?"},
        {"category": "Transport", "english": "Please stop the car here", "foreign": "गाड़ी यहाँ रोक दीजिए", "romanized": "Gaadi yahan rok dijiye", "audio_text": "गाड़ी यहाँ रोक दीजिए"},
        {"category": "Shopping", "english": "Can you give a discount?", "foreign": "क्या थोड़ा कम हो सकता है?", "romanized": "Kya thoda kam ho sakta hai?", "audio_text": "क्या थोड़ा कम हो सकता है?"},
        {"category": "Shopping", "english": "Do you accept card or UPI?", "foreign": "क्या आप कार्ड या यूपीआई लेते हैं?", "romanized": "Kya aap card ya UPI lete hain?", "audio_text": "क्या आप कार्ड या यूपीआई लेते हैं?"},
        {"category": "Shopping", "english": "Can you show me another color or size?", "foreign": "क्या आप दूसरा साइज़ दिखा सकते हैं?", "romanized": "Kya aap doosra size dikha sakte hain?", "audio_text": "क्या आप दूसरा साइज़ दिखा सकते हैं?"},
        {"category": "Shopping", "english": "I will buy this one", "foreign": "मैं यह वाला लूँगा", "romanized": "Main yeh waala loonga", "audio_text": "मैं यह वाला लूँगा"},
        {"category": "Emergency", "english": "Please help me", "foreign": "कृपया मेरी मदद कीजिए", "romanized": "Kripya meri madad kijiye", "audio_text": "कृपया मेरी मदद कीजिए"},
        {"category": "Emergency", "english": "I need a doctor or hospital", "foreign": "मुझे डॉक्टर की ज़रूरत है", "romanized": "Mujhe doctor ki zaroorat hai", "audio_text": "मुझे डॉक्टर की ज़रूरत है"},
        {"category": "Emergency", "english": "Call the police immediately", "foreign": "तुरंत पुलिस को बुलाइए", "romanized": "Turant police ko bulaiye", "audio_text": "तुरंत पुलिस को बुलाइए"},
        {"category": "Emergency", "english": "I lost my passport and bag", "foreign": "मेरा पासपोर्ट खो गया है", "romanized": "Mera passport kho gaya hai", "audio_text": "मेरा पासपोर्ट खो गया है"},
        {"category": "Directions", "english": "Where is the nearest ATM / pharmacy?", "foreign": "पास में एटीएम कहाँ है?", "romanized": "Paas mein ATM kahan hai?", "audio_text": "पास में एटीएम कहाँ है?"},
        {"category": "Directions", "english": "Go straight and turn left", "foreign": "सीधे जाइए और बाएँ मुड़िए", "romanized": "Seedhe jaiye aur baayein mudiye", "audio_text": "सीधे जाइए और बाएँ मुड़िए"}
    ],
    "tamil": [
        {"category": "Greetings", "english": "Hello / Greetings", "foreign": "வணக்கம்", "romanized": "Vanakkam", "audio_text": "வணக்கம்"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "மிக்க நன்றி", "romanized": "Mikka Nandri", "audio_text": "மிக்க நன்றி"},
        {"category": "Greetings", "english": "Good morning", "foreign": "காலை வணக்கம்", "romanized": "Kaalai Vanakkam", "audio_text": "காலை வணக்கம்"},
        {"category": "Greetings", "english": "How are you?", "foreign": "நீங்கள் எப்படி இருக்கிறீர்கள்?", "romanized": "Neengal eppadi irukkireergal?", "audio_text": "நீங்கள் எப்படி இருக்கிறீர்கள்?"},
        {"category": "Greetings", "english": "I am fine, thank you", "foreign": "நான் நலமாக இருக்கிறேன்", "romanized": "Naan nalamaaga irukkiren", "audio_text": "நான் நலமாக இருக்கிறேன்"},
        {"category": "Greetings", "english": "See you again", "foreign": "மீண்டும் சந்திப்போம்", "romanized": "Meendum sandhippom", "audio_text": "மீண்டும் சந்திப்போம்"},
        {"category": "Dining", "english": "The food is very tasty", "foreign": "சாப்பாடு மிகவும் சுவையாக இருக்கிறது", "romanized": "Saapaadu migavum suvaiyaaga irukkiradhu", "audio_text": "சாப்பாடு மிகவும் சுவையாக இருக்கிறது"},
        {"category": "Dining", "english": "Please bring the bill", "foreign": "பில் கொண்டு வாருங்கள்", "romanized": "Bill kondu vaarungal", "audio_text": "பில் கொண்டு வாருங்கள்"},
        {"category": "Dining", "english": "Please give me one filter coffee", "foreign": "ஒரு பில்டர் காபி கொடுங்கள்", "romanized": "Oru filter coffee kodungal", "audio_text": "ஒரு பில்டர் காபி கொடுங்கள்"},
        {"category": "Dining", "english": "Is this vegetarian?", "foreign": "இது சைவ உணவா?", "romanized": "Idhu saiva unavaa?", "audio_text": "இது சைவ உணவா?"},
        {"category": "Dining", "english": "Make it less spicy, please", "foreign": "காரத்தை குறைவாக போடுங்கள்", "romanized": "Kaarathai kuraivaaga podungal", "audio_text": "காரத்தை குறைவாக போடுங்கள்"},
        {"category": "Dining", "english": "Please give drinking water", "foreign": "குடிநீர் தாருங்கள்", "romanized": "Kudineer thaarungal", "audio_text": "குடிநீர் தாருங்கள்"},
        {"category": "Transport", "english": "Where is the bus stand / railway station?", "foreign": "பேருந்து நிலையம் எங்கே உள்ளது?", "romanized": "Perundhu nilayam engae ulladhu?", "audio_text": "பேருந்து நிலையம் எங்கே உள்ளது?"},
        {"category": "Transport", "english": "I want to go to Central Station", "foreign": "சென்ட்ரல் ரயில் நிலையத்திற்கு செல்ல வேண்டும்", "romanized": "Central railway nilayathirku sella vendum", "audio_text": "சென்ட்ரல் ரயில் நிலையத்திற்கு செல்ல வேண்டும்"},
        {"category": "Transport", "english": "Please turn on the auto meter", "foreign": "தயவுசெய்து மீட்டர் போடுங்கள்", "romanized": "Dhayavuseidhu meter podungal", "audio_text": "தயவுசெய்து மீட்டர் போடுங்கள்"},
        {"category": "Transport", "english": "Please stop the vehicle here", "foreign": "வண்டியை இங்கே நிறுத்துங்கள்", "romanized": "Vandiyai ingae niruthungal", "audio_text": "வண்டியை இங்கே நிறுத்துங்கள்"},
        {"category": "Shopping", "english": "How much is this?", "foreign": "இதன் விலை என்ன?", "romanized": "Idhan vilai enna?", "audio_text": "இதன் விலை என்ன?"},
        {"category": "Shopping", "english": "Can you reduce the price a bit?", "foreign": "விலையை கொஞ்சம் குறைக்க முடியுமா?", "romanized": "Vilaiyai konjam kuraikka mudiyumaa?", "audio_text": "விலையை கொஞ்சம் குறைக்க முடியுமா?"},
        {"category": "Shopping", "english": "Do you accept UPI / Google Pay?", "foreign": "கூகிள் பே அல்லது கார்டு ஏற்கப்படுகிறதா?", "romanized": "Google Pay alladhu card erkappadugiradhaa?", "audio_text": "கூகிள் பே ஏற்கப்படுகிறதா?"},
        {"category": "Emergency", "english": "Please help me", "foreign": "தயவுசெய்து எனக்கு உதவுங்கள்", "romanized": "Dhayavuseidhu enakku udhavungal", "audio_text": "தயவுசெய்து எனக்கு உதவுங்கள்"},
        {"category": "Emergency", "english": "I need a doctor immediately", "foreign": "எனக்கு உடனடியாக மருத்துவர் தேவை", "romanized": "Enakku udanadiyaaga maruthuvar thevai", "audio_text": "எனக்கு உடனடியாக மருத்துவர் தேவை"},
        {"category": "Emergency", "english": "Call the police", "foreign": "காவல்துறையை அழையுங்கள்", "romanized": "Kaavalthuraiyai azhaiyungal", "audio_text": "காவல்துறையை அழையுங்கள்"},
        {"category": "Directions", "english": "Where is the temple / beach?", "foreign": "கோவில் அல்லது கடற்கரை எங்கே உள்ளது?", "romanized": "Kovil alladhu kadarkarai engae ulladhu?", "audio_text": "கோவில் எங்கே உள்ளது?"},
        {"category": "Directions", "english": "Go straight and turn right", "foreign": "நேராக சென்று வலதுபுறம் திரும்புங்கள்", "romanized": "Neraaga sendru valadhu puram thirumbungal", "audio_text": "நேராக சென்று வலதுபுறம் திரும்புங்கள்"}
    ],
    "telugu": [
        {"category": "Greetings", "english": "Hello / Greetings", "foreign": "నమస్కారం", "romanized": "Namaskaram", "audio_text": "నమస్కారం"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "చాలా ధన్యవాదాలు", "romanized": "Chaala Dhanyavaadaalu", "audio_text": "చాలా ధన్యవాదాలు"},
        {"category": "Greetings", "english": "Good morning", "foreign": "శుభోదయం", "romanized": "Shubhodhayam", "audio_text": "శుభోదయం"},
        {"category": "Greetings", "english": "How are you?", "foreign": "మీరు ఎలా ఉన్నారు?", "romanized": "Meeru ela unnaaru?", "audio_text": "మీరు ఎలా ఉన్నారు?"},
        {"category": "Greetings", "english": "I am fine", "foreign": "నేను బాగున్నాను", "romanized": "Nenu baagunnanu", "audio_text": "నేను బాగున్నాను"},
        {"category": "Dining", "english": "The food is very good", "foreign": "భోజనం చాలా బాగుంది", "romanized": "Bhojanam chaala baagundi", "audio_text": "భోజనం చాలా బాగుంది"},
        {"category": "Dining", "english": "Please bring the bill", "foreign": "దయచేసి బిల్ ఇవ్వండి", "romanized": "Dayachesi bill ivvandi", "audio_text": "దయచేసి బిల్ ఇవ్వండి"},
        {"category": "Dining", "english": "Please give drinking water", "foreign": "దయచేసి తాగే నీరు ఇవ్వండి", "romanized": "Dayachesi thaage neeru ivvandi", "audio_text": "దయచేసి తాగే నీరు ఇవ్వండి"},
        {"category": "Dining", "english": "Is this vegetarian?", "foreign": "ఇది శాకాహార భోజనమా?", "romanized": "Idi shaakaahaara bhojanamaa?", "audio_text": "ఇది శాకాహార భోజనమా?"},
        {"category": "Dining", "english": "Make it less spicy", "foreign": "కారం తక్కువ వేయండి", "romanized": "Kaaram thakkuva veyandi", "audio_text": "కారం తక్కువ వేయండి"},
        {"category": "Transport", "english": "Where is the station / bus stop?", "foreign": "స్టేషన్ ఎక్కడ ఉంది?", "romanized": "Station ekkada undi?", "audio_text": "స్టేషన్ ఎక్కడ ఉంది?"},
        {"category": "Transport", "english": "Please turn on the meter", "foreign": "దయచేసి మీటర్ వేయండి", "romanized": "Dayachesi meter veyandi", "audio_text": "దయచేసి మీటర్ వేయండి"},
        {"category": "Transport", "english": "Please stop here", "foreign": "ఇక్కడ బండి ఆపండి", "romanized": "Ikkada bandi aapandi", "audio_text": "ఇక్కడ బండి ఆపండి"},
        {"category": "Shopping", "english": "How much does this cost?", "foreign": "ఇది ఎంత?", "romanized": "Idi entha?", "audio_text": "ఇది ఎంత?"},
        {"category": "Shopping", "english": "Can you reduce the price a bit?", "foreign": "కొంచెం ధర తగ్గించగలరా?", "romanized": "Konchem dhara thagginchagalaraa?", "audio_text": "కొంచెం ధర తగ్గించగలరా?"},
        {"category": "Emergency", "english": "Please help me", "foreign": "దయచేసి నాకు సహాయం చేయండి", "romanized": "Dayachesi naaku sahaayam cheyandi", "audio_text": "దయచేసి నాకు సహాయం చేయండి"},
        {"category": "Emergency", "english": "I need a doctor immediately", "foreign": "నాకు వెంటనే డాక్టర్ కావాలి", "romanized": "Naaku ventane doctor kaavaali", "audio_text": "నాకు వెంటనే డాక్టర్ కావాలి"},
        {"category": "Emergency", "english": "Call the police", "foreign": "పోలీసులకు ఫోన్ చేయండి", "romanized": "Police-laku phone cheyandi", "audio_text": "పోలీసులకు ఫోన్ చేయండి"},
        {"category": "Directions", "english": "Where is the nearest ATM?", "foreign": "దగ్గర్లో ఏటీఎం ఎక్కడ ఉంది?", "romanized": "Daggarlo ATM ekkada undi?", "audio_text": "దగ్గర్లో ఏటీఎం ఎక్కడ ఉంది?"},
        {"category": "Directions", "english": "Turn left / Turn right", "foreign": "ఎడమవైపు తిరగండి / కుడివైపు తిరగండి", "romanized": "Edamavaipu thiragandi / Kudivaipu thiragandi", "audio_text": "ఎడమవైపు తిరగండి"}
    ],
    "bengali": [
        {"category": "Greetings", "english": "Hello / Greetings", "foreign": "নমস্কার", "romanized": "Nomoshkar", "audio_text": "নমস্কার"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "অনেক ধন্যবাদ", "romanized": "Onek Dhonnobad", "audio_text": "অনেক ধন্যবাদ"},
        {"category": "Greetings", "english": "Good morning", "foreign": "সুপ্রভাত", "romanized": "Suprobhat", "audio_text": "সুপ্রভাত"},
        {"category": "Greetings", "english": "How are you?", "foreign": "আপনি কেমন আছেন?", "romanized": "Aapni kemon aachen?", "audio_text": "আপনি কেমন আছেন?"},
        {"category": "Greetings", "english": "I am fine", "foreign": "আমি ভালো আছি", "romanized": "Aami bhaalo aachi", "audio_text": "আমি ভালো আছি"},
        {"category": "Dining", "english": "The food is very tasty", "foreign": "খাবারটা খুব সুস্বাদু", "romanized": "Khabarta khub shushwadu", "audio_text": "খাবারটা খুব সুস্বাদু"},
        {"category": "Dining", "english": "Please bring the bill", "foreign": "বিলটা নিয়ে আসুন", "romanized": "Bill-ta niye aashun", "audio_text": "বিলটা নিয়ে আসুন"},
        {"category": "Dining", "english": "Give me one cup of tea", "foreign": "এক কাপ চা দিন", "romanized": "Ek cup chaa din", "audio_text": "এক কাপ চা দিন"},
        {"category": "Dining", "english": "Please give drinking water", "foreign": "আমাকে খাওয়ার জল দিন", "romanized": "Aamake khaowar jol din", "audio_text": "আমাকে খাওয়ার জল দিন"},
        {"category": "Transport", "english": "Where is the station / bus stand?", "foreign": "স্টেশনটি কোথায়?", "romanized": "Station-ti kothay?", "audio_text": "স্টেশনটি কোথায়?"},
        {"category": "Transport", "english": "Please stop the taxi here", "foreign": "এখানে ট্যাক্সিটা থামান", "romanized": "Ekhane taxi-ta thaamaan", "audio_text": "এখানে ট্যাক্সিটা থামান"},
        {"category": "Shopping", "english": "What is the price of this?", "foreign": "এটার দাম কত?", "romanized": "Etar daam koto?", "audio_text": "এটার দাম কত?"},
        {"category": "Shopping", "english": "Can you lower the price?", "foreign": "একটু কম রাখা যাবে?", "romanized": "Ektu kom raakha jaabe?", "audio_text": "একটু কম রাখা যাবে?"},
        {"category": "Emergency", "english": "Please help me", "foreign": "দয়া করে আমাকে সাহায্য করুন", "romanized": "Doya kore amake sahajjo korun", "audio_text": "দয়া করে আমাকে সাহায্য করুন"},
        {"category": "Emergency", "english": "I need a doctor", "foreign": "আমার একজন ডাক্তার প্রয়োজন", "romanized": "Aamar ekjon doctor proyojon", "audio_text": "আমার একজন ডাক্তার প্রয়োজন"},
        {"category": "Directions", "english": "Where is the nearest medical shop?", "foreign": "কাছের ওষুধের দোকান কোথায়?", "romanized": "Kaacher oushodher dokan kothay?", "audio_text": "কাছের ওষুধের দোকান কোথায়?"}
    ],
    "marathi": [
        {"category": "Greetings", "english": "Hello / Greetings", "foreign": "नमस्कार", "romanized": "Namaskar", "audio_text": "नमस्कार"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "खूप खूप धन्यवाद", "romanized": "Khoop khoop dhanyavaad", "audio_text": "खूप खूप धन्यवाद"},
        {"category": "Greetings", "english": "Good morning", "foreign": "शुभ सकाळ", "romanized": "Shubh Sakaal", "audio_text": "शुभ सकाळ"},
        {"category": "Greetings", "english": "How are you?", "foreign": "तुम्ही कसे आहात?", "romanized": "Tumhi kase aahaat?", "audio_text": "तुम्ही कसे आहात?"},
        {"category": "Greetings", "english": "I am fine", "foreign": "मी ठीक आहे", "romanized": "Mee theek aahe", "audio_text": "मी ठीक आहे"},
        {"category": "Dining", "english": "Food is very delicious", "foreign": "जेवण खूप छान आहे", "romanized": "Jevan khoop chhaan aahe", "audio_text": "जेवण खूप छान आहे"},
        {"category": "Dining", "english": "Please bring the bill", "foreign": "कृपया बिल आणा", "romanized": "Kripya bill aana", "audio_text": "कृपया बिल आणा"},
        {"category": "Dining", "english": "Give me one Vada Pav / Misal", "foreign": "एक वडा पाव किंवा मिसळ द्या", "romanized": "Ek Vada Pav kivha Misal dyaa", "audio_text": "एक वडा पाव द्या"},
        {"category": "Dining", "english": "Please give drinking water", "foreign": "पिण्याचे पाणी द्या", "romanized": "Pinyache paani dyaa", "audio_text": "पिण्याचे पाणी द्या"},
        {"category": "Transport", "english": "Where is the railway station?", "foreign": "स्टेशन कुठे आहे?", "romanized": "Station kuthe aahe?", "audio_text": "स्टेशन कुठे आहे?"},
        {"category": "Transport", "english": "Please turn on the meter", "foreign": "कृपया मीटर चालू करा", "romanized": "Kripya meter chaaloo karaa", "audio_text": "कृपया मीटर चालू करा"},
        {"category": "Transport", "english": "Stop the vehicle here", "foreign": "गाडी इथे थांबवा", "romanized": "Gaadi ithe thaambvaa", "audio_text": "गाडी इथे थांबवा"},
        {"category": "Shopping", "english": "How much for this?", "foreign": "याची किंमत काय आहे?", "romanized": "Yaachi kimmat kaay aahe?", "audio_text": "याची किंमत काय आहे?"},
        {"category": "Shopping", "english": "Can you give a discount?", "foreign": "काही कमी होईल का?", "romanized": "Kaahi kamee hoeel kaa?", "audio_text": "काही कमी होईल का?"},
        {"category": "Emergency", "english": "Please help me", "foreign": "कृपया मला मदत करा", "romanized": "Kripya mala madat kara", "audio_text": "कृपया मला मदत करा"},
        {"category": "Emergency", "english": "Call the police immediately", "foreign": "लगेच पोलिसांना बोलवा", "romanized": "Lagech police-aana bolvaa", "audio_text": "लगेच पोलिसांना बोलवा"}
    ],
    "urdu": [
        {"category": "Greetings", "english": "Hello / Peace be upon you", "foreign": "السلام علیکم", "romanized": "Assalam-o-Alaikum", "audio_text": "السلام علیکم"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "بہت بہت شکریہ", "romanized": "Bahut bahut shukriya", "audio_text": "بہت بہت شکریہ"},
        {"category": "Greetings", "english": "Good morning", "foreign": "صبح بخیر", "romanized": "Subah bakhair", "audio_text": "صبح بخیر"},
        {"category": "Greetings", "english": "How are you?", "foreign": "آپ کیسے ہیں؟", "romanized": "Aap kaise hain?", "audio_text": "آپ کیسے ہیں؟"},
        {"category": "Dining", "english": "The food is extremely delicious", "foreign": "کھانا بہت لذیذ ہے", "romanized": "Khaana bahut lazeez hai", "audio_text": "کھانا بہت لذیذ ہے"},
        {"category": "Dining", "english": "Please bring the bill", "foreign": "براہ کرم بل لائیں", "romanized": "Barahe-karam bill laayen", "audio_text": "براہ کرم بل لائیں"},
        {"category": "Dining", "english": "Please give drinking water", "foreign": "پینے کا پانی دیجیے", "romanized": "Peene ka paani dijiye", "audio_text": "پینے کا پانی دیجیے"},
        {"category": "Transport", "english": "Where is the station?", "foreign": "اسٹیشن کہاں ہے؟", "romanized": "Station kahan hai?", "audio_text": "اسٹیشن کہاں ہے؟"},
        {"category": "Transport", "english": "Please stop the car here", "foreign": "گاڑی یہاں روکیں", "romanized": "Gaadi yahan rokein", "audio_text": "گاڑی یہاں روکیں"},
        {"category": "Shopping", "english": "What is the price of this?", "foreign": "اس کی قیمت کیا ہے؟", "romanized": "Is ki qeemat kya hai?", "audio_text": "اس کی قیمت کیا ہے؟"},
        {"category": "Shopping", "english": "Can you reduce the price?", "foreign": "کیا کچھ رعایت مل سکتی ہے؟", "romanized": "Kya kuch riaayat mil sakti hai?", "audio_text": "کیا کچھ رعایت مل سکتی ہے؟"},
        {"category": "Emergency", "english": "Please help me", "foreign": "براہ کرم میری مدد کریں", "romanized": "Barahe-karam meri madad karen", "audio_text": "براہ کرم میری مدد کریں"},
        {"category": "Emergency", "english": "I need a doctor", "foreign": "مجھے ڈاکٹر کی ضرورت ہے", "romanized": "Mujhe doctor ki zaroorat hai", "audio_text": "مجھے ڈاکٹر کی ضرورت ہے"}
    ],
    "japanese": [
        {"category": "Greetings", "english": "Hello / Good day", "foreign": "こんにちは", "romanized": "Konnichiwa", "audio_text": "こんにちは"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "ありがとうございます", "romanized": "Arigatou gozaimasu", "audio_text": "ありがとうございます"},
        {"category": "Greetings", "english": "Good morning", "foreign": "おはようございます", "romanized": "Ohayou gozaimasu", "audio_text": "おはようございます"},
        {"category": "Greetings", "english": "Excuse me / Pardon", "foreign": "すみません", "romanized": "Sumimasen", "audio_text": "すみません"},
        {"category": "Dining", "english": "Check please", "foreign": "お会計をお願いします", "romanized": "Okaikei o onegaishimasu", "audio_text": "お会計をお願いします"},
        {"category": "Dining", "english": "Delicious! (compliment to chef)", "foreign": "とても美味しいです！", "romanized": "Totemo oishii desu!", "audio_text": "とても美味しいです"},
        {"category": "Dining", "english": "Water, please", "foreign": "お水をお願いします", "romanized": "Omizu o onegaishimasu", "audio_text": "お水をお願いします"},
        {"category": "Transport", "english": "Where is the train station?", "foreign": "駅はどこですか？", "romanized": "Eki wa doko desu ka?", "audio_text": "駅はどこですか"},
        {"category": "Transport", "english": "To Tokyo Station, please", "foreign": "東京駅までお願いします", "romanized": "Tokyo eki made onegaishimasu", "audio_text": "東京駅までお願いします"},
        {"category": "Shopping", "english": "How much is this?", "foreign": "これはいくらですか？", "romanized": "Kore wa ikura desu ka?", "audio_text": "これはいくらですか"},
        {"category": "Emergency", "english": "Please help me", "foreign": "助けてください", "romanized": "Tasukete kudasai", "audio_text": "助けてください"}
    ],
    "french": [
        {"category": "Greetings", "english": "Hello / Good day", "foreign": "Bonjour", "romanized": "Bon-ZHOOR", "audio_text": "Bonjour"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "Merci beaucoup", "romanized": "Mair-SEE boh-KOO", "audio_text": "Merci beaucoup"},
        {"category": "Greetings", "english": "Good evening", "foreign": "Bonsoir", "romanized": "Bohn-SWAHR", "audio_text": "Bonsoir"},
        {"category": "Greetings", "english": "Please", "foreign": "S'il vous plaît", "romanized": "Seel voo pleh", "audio_text": "S'il vous plaît"},
        {"category": "Dining", "english": "The menu, please", "foreign": "La carte, s'il vous plaît", "romanized": "Lah kart, seel voo pleh", "audio_text": "La carte, s'il vous plaît"},
        {"category": "Dining", "english": "The check, please", "foreign": "L'addition, s'il vous plaît", "romanized": "Lah-dee-SYOHN, seel voo pleh", "audio_text": "L'addition, s'il vous plaît"},
        {"category": "Transport", "english": "Where is the metro / train?", "foreign": "Où est le métro ?", "romanized": "Oo eh luh meh-troh?", "audio_text": "Où est le métro"},
        {"category": "Shopping", "english": "How much does this cost?", "foreign": "Combien ça coûte ?", "romanized": "Kohm-byen sah koot?", "audio_text": "Combien ça coûte"},
        {"category": "Emergency", "english": "Help!", "foreign": "Au secours !", "romanized": "Oh suh-KOOR!", "audio_text": "Au secours"}
    ],
    "spanish": [
        {"category": "Greetings", "english": "Hello / Good day", "foreign": "¡Hola! Buenos días", "romanized": "OH-lah! BWEH-nohs DEE-ahs", "audio_text": "Hola! Buenos días"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "Muchas gracias", "romanized": "MOO-chahs GRAH-syahs", "audio_text": "Muchas gracias"},
        {"category": "Greetings", "english": "Please", "foreign": "Por favor", "romanized": "Por fah-VOR", "audio_text": "Por favor"},
        {"category": "Dining", "english": "The bill, please", "foreign": "La cuenta, por favor", "romanized": "Lah KWEN-tah, por fah-VOR", "audio_text": "La cuenta, por favor"},
        {"category": "Dining", "english": "Do you have vegetarian food?", "foreign": "¿Tiene comida vegetariana?", "romanized": "TYEH-neh koh-MEE-dah veh-heh-tah-RYAH-nah?", "audio_text": "Tiene comida vegetariana"},
        {"category": "Transport", "english": "Where is the station?", "foreign": "¿Dónde está la estación?", "romanized": "DOHN-deh ehs-TAH lah ehs-tah-SYOHN?", "audio_text": "Dónde está la estación"},
        {"category": "Shopping", "english": "How much does this cost?", "foreign": "¿Cuánto cuesta esto?", "romanized": "KWAHN-toh KWEHS-tah EHS-toh?", "audio_text": "Cuánto cuesta esto"},
        {"category": "Emergency", "english": "Help me, please", "foreign": "Ayúdeme, por favor", "romanized": "ah-YOO-deh-meh, por fah-VOR", "audio_text": "Ayúdeme, por favor"}
    ],
    "italian": [
        {"category": "Greetings", "english": "Good morning / Hello", "foreign": "Buongiorno", "romanized": "Bwon-JOR-noh", "audio_text": "Buongiorno"},
        {"category": "Greetings", "english": "Thank you so much", "foreign": "Grazie mille", "romanized": "GRAHT-syeh MEE-leh", "audio_text": "Grazie mille"},
        {"category": "Greetings", "english": "Please", "foreign": "Per favore", "romanized": "Pair fah-VOH-reh", "audio_text": "Per favore"},
        {"category": "Dining", "english": "A table for two, please", "foreign": "Un tavolo per due, per favore", "romanized": "Oon TAH-voh-loh pair DOO-eh, pair fah-VOH-reh", "audio_text": "Un tavolo per due, per favore"},
        {"category": "Dining", "english": "The bill, please", "foreign": "Il conto, per favore", "romanized": "Eel KOHN-toh, pair fah-VOH-reh", "audio_text": "Il conto, per favore"},
        {"category": "Transport", "english": "Where is the station?", "foreign": "Dov'è la stazione?", "romanized": "Doh-VEH lah stah-TSYOH-neh?", "audio_text": "Dov'è la stazione"},
        {"category": "Shopping", "english": "How much is this?", "foreign": "Quanto costa questo?", "romanized": "KWAHN-toh KOHS-tah KWEHS-toh?", "audio_text": "Quanto costa questo"},
        {"category": "Emergency", "english": "I need a doctor", "foreign": "Ho bisogno di un medico", "romanized": "Oh bee-ZOHN-yoh dee oon MEH-dee-koh", "audio_text": "Ho bisogno di un medico"}
    ],
    "german": [
        {"category": "Greetings", "english": "Hello / Good day", "foreign": "Guten Tag", "romanized": "GOO-ten tahk", "audio_text": "Guten Tag"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "Vielen Dank", "romanized": "FEE-len dahnk", "audio_text": "Vielen Dank"},
        {"category": "Greetings", "english": "Please", "foreign": "Bitte", "romanized": "BIH-tuh", "audio_text": "Bitte"},
        {"category": "Dining", "english": "The bill, please", "foreign": "Die Rechnung, bitte", "romanized": "Dee REKH-noong, BIH-tuh", "audio_text": "Die Rechnung, bitte"},
        {"category": "Dining", "english": "Water, please", "foreign": "Wasser, bitte", "romanized": "VAH-ser, BIH-tuh", "audio_text": "Wasser, bitte"},
        {"category": "Transport", "english": "Where is the station?", "foreign": "Wo ist der Bahnhof?", "romanized": "Voh ist der BAHN-hohf?", "audio_text": "Wo ist der Bahnhof"},
        {"category": "Shopping", "english": "How much is that?", "foreign": "Wie viel kostet das?", "romanized": "Vee feel KOHS-tet dahs?", "audio_text": "Wie viel kostet das"},
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
