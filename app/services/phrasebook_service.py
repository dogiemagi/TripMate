import logging
from typing import Dict, Any, List
from app.models.schemas import PhrasebookQuery

logger = logging.getLogger("voyage.phrasebook")

# 10 comprehensive, authentic travel sentences for each category
PHRASEBOOK_DATA = {
    "hindi": [
        # Greetings (10)
        {"category": "Greetings", "english": "Hello / Greetings", "foreign": "नमस्ते", "romanized": "Namaste", "audio_text": "नमस्ते"},
        {"category": "Greetings", "english": "Good morning", "foreign": "शुभ प्रभात", "romanized": "Shubh Prabhaat", "audio_text": "शुभ प्रभात"},
        {"category": "Greetings", "english": "Good evening", "foreign": "शुभ संध्या", "romanized": "Shubh Sandhya", "audio_text": "शुभ संध्या"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "बहुत बहुत धन्यवाद", "romanized": "Bahut bahut dhanyavaad", "audio_text": "बहुत बहुत धन्यवाद"},
        {"category": "Greetings", "english": "You are welcome", "foreign": "आपका स्वागत है", "romanized": "Aapka swaagat hai", "audio_text": "आपका स्वागत है"},
        {"category": "Greetings", "english": "How are you?", "foreign": "आप कैसे हैं?", "romanized": "Aap kaise hain?", "audio_text": "आप कैसे हैं?"},
        {"category": "Greetings", "english": "I am fine, thank you", "foreign": "मैं ठीक हूँ, धन्यवाद", "romanized": "Main theek hoon, dhanyavaad", "audio_text": "मैं ठीक हूँ धन्यवाद"},
        {"category": "Greetings", "english": "What is your name?", "foreign": "आपका नाम क्या है?", "romanized": "Aapka naam kya hai?", "audio_text": "आपका नाम क्या है?"},
        {"category": "Greetings", "english": "Nice to meet you", "foreign": "आपसे मिलकर खुशी हुई", "romanized": "Aapse milkar khushi hui", "audio_text": "आपसे मिलकर खुशी हुई"},
        {"category": "Greetings", "english": "See you again / Goodbye", "foreign": "फिर मिलेंगे, अलविदा", "romanized": "Phir milenge, alvida", "audio_text": "फिर मिलेंगे अलविदा"},

        # Dining (10)
        {"category": "Dining", "english": "How much does this cost?", "foreign": "यह कितने का है?", "romanized": "Yeh kitne ka hai?", "audio_text": "यह कितने का है?"},
        {"category": "Dining", "english": "Please bring the bill / check", "foreign": "कृपया बिल ले आइए", "romanized": "Kripya bill le aaiye", "audio_text": "कृपया बिल ले आइए"},
        {"category": "Dining", "english": "The food is very delicious", "foreign": "खाना बहुत स्वादिष्ट है", "romanized": "Khaana bahut swaadisht hai", "audio_text": "खाना बहुत स्वादिष्ट है"},
        {"category": "Dining", "english": "Is this dish vegetarian?", "foreign": "क्या यह शाकाहारी खाना है?", "romanized": "Kya yeh shakahari khana hai?", "audio_text": "क्या यह शाकाहारी खाना है?"},
        {"category": "Dining", "english": "Please make it less spicy", "foreign": "कृपया कम तीखा बनाइए", "romanized": "Kripya kam teekha banaiye", "audio_text": "कृपया कम तीखा बनाइए"},
        {"category": "Dining", "english": "Please give me drinking water", "foreign": "कृपया पीने का पानी दीजिए", "romanized": "Kripya peene ka paani dijiye", "audio_text": "कृपया पीने का पानी दीजिए"},
        {"category": "Dining", "english": "Can I have one cup of hot tea?", "foreign": "एक कप गर्म चाय मिलेगी?", "romanized": "Ek cup garam chai milegi?", "audio_text": "एक कप गर्म चाय मिलेगी?"},
        {"category": "Dining", "english": "Can I see the food menu?", "foreign": "क्या मुझे खाने का मेनू मिल सकता है?", "romanized": "Kya mujhe khaane ka menu mil sakta hai?", "audio_text": "क्या मुझे खाने का मेनू मिल सकता है?"},
        {"category": "Dining", "english": "What is the chef special today?", "foreign": "आज का खास व्यंजन क्या है?", "romanized": "Aaj ka khaas vyanjan kya hai?", "audio_text": "आज का खास व्यंजन क्या है?"},
        {"category": "Dining", "english": "We want a table for two people", "foreign": "दो लोगों के लिए मेज चाहिए", "romanized": "Do logon ke liye mez chahiye", "audio_text": "दो लोगों के लिए मेज चाहिए"},

        # Transport (10)
        {"category": "Transport", "english": "Where is the railway station / bus stand?", "foreign": "रेलवे स्टेशन या बस स्टैंड कहाँ है?", "romanized": "Railway station ya bus stand kahan hai?", "audio_text": "रेलवे स्टेशन कहाँ है?"},
        {"category": "Transport", "english": "Please turn on the taxi meter", "foreign": "कृपया मीटर चालू कीजिए", "romanized": "Kripya meter chaaloo kijiye", "audio_text": "कृपया मीटर चालू कीजिए"},
        {"category": "Transport", "english": "I want to go to this address", "foreign": "मुझे इस पते पर जाना है", "romanized": "Mujhe is pate par jaana hai", "audio_text": "मुझे इस पते पर जाना है"},
        {"category": "Transport", "english": "How far is the airport from here?", "foreign": "हवाई अड्डा यहाँ से कितनी दूर है?", "romanized": "Hawai adda yahan se kitni door hai?", "audio_text": "हवाई अड्डा यहाँ से कितनी दूर है?"},
        {"category": "Transport", "english": "Please stop the car / auto here", "foreign": "गाड़ी यहाँ रोक दीजिए", "romanized": "Gaadi yahan rok dijiye", "audio_text": "गाड़ी यहाँ रोक दीजिए"},
        {"category": "Transport", "english": "What time does the next train arrive?", "foreign": "अगली ट्रेन कितने बजे आएगी?", "romanized": "Agli train kitne baje aayegi?", "audio_text": "अगली ट्रेन कितने बजे आएगी?"},
        {"category": "Transport", "english": "Where can I buy a ticket?", "foreign": "टिकट कहाँ से मिलेगा?", "romanized": "Ticket kahan se milega?", "audio_text": "टिकट कहाँ से मिलेगा?"},
        {"category": "Transport", "english": "Is this bus going to the city center?", "foreign": "क्या यह बस शहर के केंद्र जा रही है?", "romanized": "Kya yeh bus shahar ke kendra jaa rahi hai?", "audio_text": "क्या यह बस शहर जा रही है?"},
        {"category": "Transport", "english": "How much is the fare to the station?", "foreign": "स्टेशन तक का किराया कितना है?", "romanized": "Station tak ka kiraya kitna hai?", "audio_text": "स्टेशन तक का किराया कितना है?"},
        {"category": "Transport", "english": "Can you call a taxi for me?", "foreign": "क्या आप मेरे लिए टैक्सी बुला सकते हैं?", "romanized": "Kya aap mere liye taxi bula sakte hain?", "audio_text": "क्या आप मेरे लिए टैक्सी बुला सकते हैं?"},

        # Shopping (10)
        {"category": "Shopping", "english": "Can you give a discount on this?", "foreign": "क्या इसमें थोड़ा कम हो सकता है?", "romanized": "Kya isme thoda kam ho sakta hai?", "audio_text": "क्या थोड़ा कम हो सकता है?"},
        {"category": "Shopping", "english": "Do you accept card, Google Pay or UPI?", "foreign": "क्या आप कार्ड या यूपीआई लेते हैं?", "romanized": "Kya aap card ya UPI lete hain?", "audio_text": "क्या आप कार्ड या यूपीआई लेते हैं?"},
        {"category": "Shopping", "english": "Can you show me another color or size?", "foreign": "क्या आप दूसरा रंग या साइज़ दिखा सकते हैं?", "romanized": "Kya aap doosra rang ya size dikha sakte hain?", "audio_text": "क्या आप दूसरा साइज़ दिखा सकते हैं?"},
        {"category": "Shopping", "english": "I will buy this one", "foreign": "मैं यह वाला सामान लूँगा", "romanized": "Main yeh waala saaman loonga", "audio_text": "मैं यह वाला लूँगा"},
        {"category": "Shopping", "english": "This is too expensive", "foreign": "यह बहुत महँगा है", "romanized": "Yeh bahut mehanga hai", "audio_text": "यह बहुत महँगा है"},
        {"category": "Shopping", "english": "Can I try this on?", "foreign": "क्या मैं इसे पहनकर देख सकता हूँ?", "romanized": "Kya main ise pehankar dekh sakta hoon?", "audio_text": "क्या मैं इसे देख सकता हूँ?"},
        {"category": "Shopping", "english": "Do you have local handcrafted souvenirs?", "foreign": "क्या आपके पास स्थानीय हस्तशिल्प है?", "romanized": "Kya aapke paas sthaniya hastashilp hai?", "audio_text": "क्या आपके पास स्थानीय हस्तशिल्प है?"},
        {"category": "Shopping", "english": "Please give me the purchase receipt", "foreign": "कृपया पक्की रसीद दीजिए", "romanized": "Kripya pakki raseed dijiye", "audio_text": "कृपया रसीद दीजिए"},
        {"category": "Shopping", "english": "Can you pack this as a gift?", "foreign": "क्या आप इसे गिफ्ट पैक कर सकते हैं?", "romanized": "Kya aap ise gift pack kar sakte hain?", "audio_text": "क्या आप इसे पैक कर सकते हैं?"},
        {"category": "Shopping", "english": "What time do the shops close?", "foreign": "दुकानें कितने बजे बंद होती हैं?", "romanized": "Dukaanein kitne baje band hoti hain?", "audio_text": "दुकानें कितने बजे बंद होती हैं?"},

        # Emergency (10)
        {"category": "Emergency", "english": "Please help me immediately", "foreign": "कृपया तुरंत मेरी मदद कीजिए", "romanized": "Kripya turant meri madad kijiye", "audio_text": "कृपया मेरी मदद कीजिए"},
        {"category": "Emergency", "english": "I need a doctor or hospital", "foreign": "मुझे डॉक्टर या अस्पताल की ज़रूरत है", "romanized": "Mujhe doctor ya aspatal ki zaroorat hai", "audio_text": "मुझे डॉक्टर की ज़रूरत है"},
        {"category": "Emergency", "english": "Call the police right now", "foreign": "तुरंत पुलिस को बुलाइए", "romanized": "Turant police ko bulaiye", "audio_text": "तुरंत पुलिस को बुलाइए"},
        {"category": "Emergency", "english": "I lost my passport and travel bag", "foreign": "मेरा पासपोर्ट और बैग खो गया है", "romanized": "Mera passport aur bag kho gaya hai", "audio_text": "मेरा पासपोर्ट खो गया है"},
        {"category": "Emergency", "english": "There has been an accident", "foreign": "यहाँ एक दुर्घटना हो गई है", "romanized": "Yahan ek durghatna ho gayi hai", "audio_text": "यहाँ दुर्घटना हो गई है"},
        {"category": "Emergency", "english": "I am feeling very unwell / sick", "foreign": "मेरी तबीयत बहुत खराब लग रही है", "romanized": "Meri tabiyat bahut kharab lag rahi hai", "audio_text": "मेरी तबीयत खराब है"},
        {"category": "Emergency", "english": "Where is the nearest tourist embassy?", "foreign": "दूतावास कहाँ पर है?", "romanized": "Dootavaas kahan par hai?", "audio_text": "दूतावास कहाँ है?"},
        {"category": "Emergency", "english": "Please call an ambulance", "foreign": "कृपया एम्बुलेंस बुलाइए", "romanized": "Kripya ambulance bulaiye", "audio_text": "कृपया एम्बुलेंस बुलाइए"},
        {"category": "Emergency", "english": "I am allergic to nuts and dairy", "foreign": "मुझे नट्स और दूध से एलर्जी है", "romanized": "Mujhe nuts aur doodh se allergy hai", "audio_text": "मुझे एलर्जी है"},
        {"category": "Emergency", "english": "I am lost, can you guide me?", "foreign": "मैं रास्ता भटक गया हूँ, क्या रास्ता बताएँगे?", "romanized": "Main raasta bhatak gaya hoon, kya raasta batayenge?", "audio_text": "मैं रास्ता भटक गया हूँ"},

        # Directions (10)
        {"category": "Directions", "english": "Where is the nearest ATM or bank?", "foreign": "पास में एटीएम या बैंक कहाँ है?", "romanized": "Paas mein ATM ya bank kahan hai?", "audio_text": "पास में एटीएम कहाँ है?"},
        {"category": "Directions", "english": "Where is the nearest pharmacy / medical store?", "foreign": "नजदीकी मेडिकल स्टोर कहाँ है?", "romanized": "Najdeeki medical store kahan hai?", "audio_text": "नजदीकी मेडिकल स्टोर कहाँ है?"},
        {"category": "Directions", "english": "Go straight and turn left", "foreign": "सीधे जाइए और बाएँ मुड़िए", "romanized": "Seedhe jaiye aur baayein mudiye", "audio_text": "सीधे जाइए और बाएँ मुड़िए"},
        {"category": "Directions", "english": "Turn right at the traffic signal", "foreign": "ट्रैफिक सिग्नल से दाएँ मुड़िए", "romanized": "Traffic signal se daayein mudiye", "audio_text": "ट्रैफिक सिग्नल से दाएँ मुड़िए"},
        {"category": "Directions", "english": "How far is the city center on foot?", "foreign": "पैदल शहर का केंद्र कितनी दूर है?", "romanized": "Paidal shahar ka kendra kitni door hai?", "audio_text": "शहर का केंद्र कितनी दूर है?"},
        {"category": "Directions", "english": "Is it on the left or right side?", "foreign": "यह बायीं तरफ है या दायीं तरफ?", "romanized": "Yeh baayeen taraf hai ya daayeen taraf?", "audio_text": "यह किस तरफ है?"},
        {"category": "Directions", "english": "Where is the entrance and exit?", "foreign": "प्रवेश द्वार और निकास कहाँ है?", "romanized": "Pravesh dwaar aur nikaas kahan hai?", "audio_text": "प्रवेश द्वार कहाँ है?"},
        {"category": "Directions", "english": "Can you show me on Google Maps?", "foreign": "क्या आप मुझे नक्शे पर दिखा सकते हैं?", "romanized": "Kya aap mujhe nakshe par dikha sakte hain?", "audio_text": "क्या आप नक्शे पर दिखा सकते हैं?"},
        {"category": "Directions", "english": "Where is the public restroom / washroom?", "foreign": "शौचालय कहाँ पर है?", "romanized": "Shauchalay kahan par hai?", "audio_text": "शौचालय कहाँ है?"},
        {"category": "Directions", "english": "Is this the correct way to the monument?", "foreign": "क्या यह स्मारक का सही रास्ता है?", "romanized": "Kya yeh smaarak ka sahi raasta hai?", "audio_text": "क्या यह सही रास्ता है?"}
    ],
    "tamil": [
        # Greetings (10)
        {"category": "Greetings", "english": "Hello / Greetings", "foreign": "வணக்கம்", "romanized": "Vanakkam", "audio_text": "வணக்கம்"},
        {"category": "Greetings", "english": "Good morning", "foreign": "காலை வணக்கம்", "romanized": "Kaalai Vanakkam", "audio_text": "காலை வணக்கம்"},
        {"category": "Greetings", "english": "Good evening", "foreign": "மாலை வணக்கம்", "romanized": "Maalai Vanakkam", "audio_text": "மாலை வணக்கம்"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "மிக்க நன்றி", "romanized": "Mikka Nandri", "audio_text": "மிக்க நன்றி"},
        {"category": "Greetings", "english": "You are welcome", "foreign": "நல்வரவு", "romanized": "Nalvaravu", "audio_text": "நல்வரவு"},
        {"category": "Greetings", "english": "How are you?", "foreign": "நீங்கள் எப்படி இருக்கிறீர்கள்?", "romanized": "Neengal eppadi irukkireergal?", "audio_text": "நீங்கள் எப்படி இருக்கிறீர்கள்?"},
        {"category": "Greetings", "english": "I am fine, thank you", "foreign": "நான் நலமாக இருக்கிறேன்", "romanized": "Naan nalamaaga irukkiren", "audio_text": "நான் நலமாக இருக்கிறேன்"},
        {"category": "Greetings", "english": "What is your name?", "foreign": "உங்கள் பெயர் என்ன?", "romanized": "Ungal peyar enna?", "audio_text": "உங்கள் பெயர் என்ன?"},
        {"category": "Greetings", "english": "Nice to meet you", "foreign": "உங்களை சந்தித்ததில் மகிழ்ச்சி", "romanized": "Ungalai sandhithadhil magizhchi", "audio_text": "உங்களை சந்தித்ததில் மகிழ்ச்சி"},
        {"category": "Greetings", "english": "See you again", "foreign": "மீண்டும் சந்திப்போம்", "romanized": "Meendum sandhippom", "audio_text": "மீண்டும் சந்திப்போம்"},

        # Dining (10)
        {"category": "Dining", "english": "The food is very tasty", "foreign": "சாப்பாடு மிகவும் சுவையாக இருக்கிறது", "romanized": "Saapaadu migavum suvaiyaaga irukkiradhu", "audio_text": "சாப்பாடு மிகவும் சுவையாக இருக்கிறது"},
        {"category": "Dining", "english": "Please bring the bill", "foreign": "பில் கொண்டு வாருங்கள்", "romanized": "Bill kondu vaarungal", "audio_text": "பில் கொண்டு வாருங்கள்"},
        {"category": "Dining", "english": "Please give me one filter coffee", "foreign": "ஒரு பில்டர் காபி கொடுங்கள்", "romanized": "Oru filter coffee kodungal", "audio_text": "ஒரு பில்டர் காபி கொடுங்கள்"},
        {"category": "Dining", "english": "Is this vegetarian?", "foreign": "இது சைவ உணவா?", "romanized": "Idhu saiva unavaa?", "audio_text": "இது சைவ உணவா?"},
        {"category": "Dining", "english": "Make it less spicy, please", "foreign": "காரத்தை குறைவாக போடுங்கள்", "romanized": "Kaarathai kuraivaaga podungal", "audio_text": "காரத்தை குறைவாக போடுங்கள்"},
        {"category": "Dining", "english": "Please give drinking water", "foreign": "குடிநீர் தாருங்கள்", "romanized": "Kudineer thaarungal", "audio_text": "குடிநீர் தாருங்கள்"},
        {"category": "Dining", "english": "Give me crispy ghee roast dosa", "foreign": "ஒரு நெய் ரோஸ்ட் தோசை கொடுங்கள்", "romanized": "Oru ghee roast dosa kodungal", "audio_text": "ஒரு நெய் ரோஸ்ட் தோசை கொடுங்கள்"},
        {"category": "Dining", "english": "Can I see the food menu?", "foreign": "உணவுப் பட்டியலைக் காட்டுங்கள்", "romanized": "Unavu pattiyalai kaattungal", "audio_text": "உணவுப் பட்டியலைக் காட்டுங்கள்"},
        {"category": "Dining", "english": "A table for two, please", "foreign": "இருவருக்கு மேஜை வேண்டும்", "romanized": "Iruvarukku meejai vendum", "audio_text": "இருவருக்கு மேஜை வேண்டும்"},
        {"category": "Dining", "english": "What is the special dish today?", "foreign": "இன்றைய சிறப்பு உணவு என்ன?", "romanized": "Indraya sirappu unavu enna?", "audio_text": "இன்றைய சிறப்பு உணவு என்ன?"},

        # Transport (10)
        {"category": "Transport", "english": "Where is the bus stand / railway station?", "foreign": "பேருந்து நிலையம் எங்கே உள்ளது?", "romanized": "Perundhu nilayam engae ulladhu?", "audio_text": "பேருந்து நிலையம் எங்கே உள்ளது?"},
        {"category": "Transport", "english": "I want to go to Central Station", "foreign": "சென்ட்ரல் ரயில் நிலையத்திற்கு செல்ல வேண்டும்", "romanized": "Central railway nilayathirku sella vendum", "audio_text": "சென்ட்ரல் ரயில் நிலையத்திற்கு செல்ல வேண்டும்"},
        {"category": "Transport", "english": "Please turn on the auto meter", "foreign": "தயவுசெய்து மீட்டர் போடுங்கள்", "romanized": "Dhayavuseidhu meter podungal", "audio_text": "தயவுசெய்து மீட்டர் போடுங்கள்"},
        {"category": "Transport", "english": "Please stop the vehicle here", "foreign": "வண்டியை இங்கே நிறுத்துங்கள்", "romanized": "Vandiyai ingae niruthungal", "audio_text": "வண்டியை இங்கே நிறுத்துங்கள்"},
        {"category": "Transport", "english": "How far is the airport?", "foreign": "விமான நிலையம் எவ்வளவு தூரம்?", "romanized": "Vimaana nilayam evvalavu dhooram?", "audio_text": "விமான நிலையம் எவ்வளவு தூரம்?"},
        {"category": "Transport", "english": "How much is the auto fare?", "foreign": "ஆட்டோ கட்டணம் எவ்வளவு?", "romanized": "Auto kattanam evvalavu?", "audio_text": "ஆட்டோ கட்டணம் எவ்வளவு?"},
        {"category": "Transport", "english": "Does this bus go to Marina Beach?", "foreign": "இந்த பேருந்து மெரினா கடற்கரைக்கு போகுமா?", "romanized": "Indha perundhu Marina kadarkarai-kku pogumaa?", "audio_text": "இந்த பேருந்து மெரினாவுக்கு போகுமா?"},
        {"category": "Transport", "english": "Where can I get a metro ticket?", "foreign": "மெட்ரோ டிக்கெட் எங்கே கிடைக்கும்?", "romanized": "Metro ticket engae kidaikkum?", "audio_text": "மெட்ரோ டிக்கெட் எங்கே கிடைக்கும்?"},
        {"category": "Transport", "english": "What time is the next local train?", "foreign": "அடுத்த ரயில் எத்தனை மணிக்கு?", "romanized": "Adutha rayil ethana manikku?", "audio_text": "அடுத்த ரயில் எத்தனை மணிக்கு?"},
        {"category": "Transport", "english": "Can you call a cab for me?", "foreign": "எனக்கு ஒரு டாக்ஸி புக் செய்ய முடியுமா?", "romanized": "Enakku oru taxi book seiya mudiyumaa?", "audio_text": "எனக்கு டாக்ஸி புக் செய்ய முடியுமா?"},

        # Shopping (10)
        {"category": "Shopping", "english": "How much is this item?", "foreign": "இதன் விலை என்ன?", "romanized": "Idhan vilai enna?", "audio_text": "இதன் விலை என்ன?"},
        {"category": "Shopping", "english": "Can you reduce the price a bit?", "foreign": "விலையை கொஞ்சம் குறைக்க முடியுமா?", "romanized": "Vilaiyai konjam kuraikka mudiyumaa?", "audio_text": "விலையை கொஞ்சம் குறைக்க முடியுமா?"},
        {"category": "Shopping", "english": "Do you accept Google Pay or Card?", "foreign": "கூகிள் பே அல்லது கார்டு ஏற்கப்படுகிறதா?", "romanized": "Google Pay alladhu card erkappadugiradhaa?", "audio_text": "கூகிள் பே ஏற்கப்படுகிறதா?"},
        {"category": "Shopping", "english": "I will buy this one", "foreign": "நான் இதை வாங்குகிறேன்", "romanized": "Naan idhai vaangugiren", "audio_text": "நான் இதை வாங்குகிறேன்"},
        {"category": "Shopping", "english": "Can you show another silk saree / shirt?", "foreign": "வேறு நிறம் அல்லது பட்டுப் புடவை உள்ளதா?", "romanized": "Veru niram alladhu pattu pudavai ulladhaa?", "audio_text": "வேறு நிறம் உள்ளதா?"},
        {"category": "Shopping", "english": "This is very high quality", "foreign": "இது மிகவும் நல்ல தரமாக உள்ளது", "romanized": "Idhu migavum nalla tharamaaga ulladhu", "audio_text": "இது நல்ல தரமாக உள்ளது"},
        {"category": "Shopping", "english": "Please give me a bill / receipt", "foreign": "ரசீது கொடுங்கள்", "romanized": "Raseedhu kodungal", "audio_text": "ரசீது கொடுங்கள்"},
        {"category": "Shopping", "english": "Can you pack it safely for travel?", "foreign": "பயணத்திற்கு ஏற்றவாறு பேக் செய்ய முடியுமா?", "romanized": "Payanathirku etravaaru pack seiya mudiyumaa?", "audio_text": "பேக் செய்ய முடியுமா?"},
        {"category": "Shopping", "english": "Where can I buy traditional filter coffee powder?", "foreign": "பில்டர் காபித்தூள் எங்கே கிடைக்கும்?", "romanized": "Filter coffee thool engae kidaikkum?", "audio_text": "காபித்தூள் எங்கே கிடைக்கும்?"},
        {"category": "Shopping", "english": "What time does the market close?", "foreign": "கடை எத்தனை மணிக்கு மூடுவார்கள்?", "romanized": "Kadai ethana manikku mooduvaargal?", "audio_text": "கடை எத்தனை மணிக்கு மூடுவார்கள்?"},

        # Emergency (10)
        {"category": "Emergency", "english": "Please help me immediately", "foreign": "தயவுசெய்து எனக்கு உதவுங்கள்", "romanized": "Dhayavuseidhu enakku udhavungal", "audio_text": "தயவுசெய்து எனக்கு உதவுங்கள்"},
        {"category": "Emergency", "english": "I need a doctor immediately", "foreign": "எனக்கு உடனடியாக மருத்துவர் தேவை", "romanized": "Enakku udanadiyaaga maruthuvar thevai", "audio_text": "எனக்கு உடனடியாக மருத்துவர் தேவை"},
        {"category": "Emergency", "english": "Call the police right now", "foreign": "காவல்துறையை அழையுங்கள்", "romanized": "Kaavalthuraiyai azhaiyungal", "audio_text": "காவல்துறையை அழையுங்கள்"},
        {"category": "Emergency", "english": "I lost my mobile and purse", "foreign": "என் மொபைல் மற்றும் பர்ஸ் தொலைந்துவிட்டது", "romanized": "En mobile matrum purse tholaindhuvittadhu", "audio_text": "மொபைல் தொலைந்துவிட்டது"},
        {"category": "Emergency", "english": "Call an ambulance quickly", "foreign": "உடனடியாக ஆம்புலன்ஸ் அழையுங்கள்", "romanized": "Udanadiyaaga ambulance azhaiyungal", "audio_text": "ஆம்புலன்ஸ் அழையுங்கள்"},
        {"category": "Emergency", "english": "I am feeling very dizzy / ill", "foreign": "எனக்கு மயக்கமாக இருக்கிறது", "romanized": "Enakku mayakkamaaga irukkiradhu", "audio_text": "எனக்கு மயக்கமாக இருக்கிறது"},
        {"category": "Emergency", "english": "Where is the emergency ward?", "foreign": "அவசர சிகிச்சை பிரிவு எங்கே?", "romanized": "Avasara sigichai pirivu engae?", "audio_text": "அவசர சிகிச்சை பிரிவு எங்கே?"},
        {"category": "Emergency", "english": "An accident has occurred", "foreign": "இங்கு ஒரு விபத்து நடந்துள்ளது", "romanized": "Ingu oru vibathu nadandhulladhu", "audio_text": "விபத்து நடந்துள்ளது"},
        {"category": "Emergency", "english": "I am allergic to seafood", "foreign": "எனக்கு கடல் உணவுகள் ஒவ்வாமை", "romanized": "Enakku kadal unavu ovvaamai", "audio_text": "எனக்கு ஒவ்வாமை உண்டு"},
        {"category": "Emergency", "english": "I am lost, please guide me", "foreign": "வழி தெரியவில்லை, உதவி செய்யுங்கள்", "romanized": "Vazhi theriyavillai, udhavi seiyungal", "audio_text": "உதவி செய்யுங்கள்"},

        # Directions (10)
        {"category": "Directions", "english": "Where is the temple / beach?", "foreign": "கோவில் அல்லது கடற்கரை எங்கே உள்ளது?", "romanized": "Kovil alladhu kadarkarai engae ulladhu?", "audio_text": "கோவில் எங்கே உள்ளது?"},
        {"category": "Directions", "english": "Go straight and turn right", "foreign": "நேராக சென்று வலதுபுறம் திரும்புங்கள்", "romanized": "Neraaga sendru valadhu puram thirumbungal", "audio_text": "நேராக சென்று வலதுபுறம் திரும்புங்கள்"},
        {"category": "Directions", "english": "Turn left at the next junction", "foreign": "அடுத்த சந்திப்பில் இடதுபுறம் திரும்புங்கள்", "romanized": "Adutha sandhippil idadhu puram thirumbungal", "audio_text": "இடதுபுறம் திரும்புங்கள்"},
        {"category": "Directions", "english": "Where is the nearest medical shop / pharmacy?", "foreign": "அருகில் உள்ள மருந்தகம் எங்கே?", "romanized": "Arugil ulla marundhagam engae?", "audio_text": "மருந்தகம் எங்கே?"},
        {"category": "Directions", "english": "Where is the nearest ATM counter?", "foreign": "அருகில் உள்ள ஏடிஎம் எங்கே?", "romanized": "Arugil ulla ATM engae?", "audio_text": "ஏடிஎம் எங்கே?"},
        {"category": "Directions", "english": "Is it within walking distance?", "foreign": "நடந்து செல்லும் தூரத்திலா உள்ளது?", "romanized": "Nadandhu sellum dhoorathilaa ulladhu?", "audio_text": "நடந்து செல்லும் தூரத்திலா உள்ளது?"},
        {"category": "Directions", "english": "Where is the public restroom?", "foreign": "கழிப்பறை எங்கே உள்ளது?", "romanized": "Kazhipparai engae ulladhu?", "audio_text": "கழிப்பறை எங்கே உள்ளது?"},
        {"category": "Directions", "english": "Which bus goes to T. Nagar / Mylapore?", "foreign": "தி.நகர் செல்ல எந்த பேருந்து போகும்?", "romanized": "T. Nagar sella endha perundhu pogum?", "audio_text": "எந்த பேருந்து போகும்?"},
        {"category": "Directions", "english": "Can you show me the route on Google Maps?", "foreign": "வரைபடத்தில் வழியைக் காட்ட முடியுமா?", "romanized": "Varaipadathil vazhiyai kaatta mudiyumaa?", "audio_text": "வழியைக் காட்ட முடியுமா?"},
        {"category": "Directions", "english": "Where is the main entrance gate?", "foreign": "முக்கிய நுழைவு வாயில் எங்கே?", "romanized": "Mukkiya nuzhaivu vaayil engae?", "audio_text": "நுழைவு வாயில் எங்கே?"}
    ],
    "telugu": [
        # Greetings (10)
        {"category": "Greetings", "english": "Hello / Greetings", "foreign": "నమస్కారం", "romanized": "Namaskaram", "audio_text": "నమస్కారం"},
        {"category": "Greetings", "english": "Good morning", "foreign": "శుభోదయం", "romanized": "Shubhodhayam", "audio_text": "శుభోదయం"},
        {"category": "Greetings", "english": "Good evening", "foreign": "శుభ సాయంత్రం", "romanized": "Shubha Saayantram", "audio_text": "శుభ సాయంత్రం"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "చాలా ధన్యవాదాలు", "romanized": "Chaala Dhanyavaadaalu", "audio_text": "చాలా ధన్యవాదాలు"},
        {"category": "Greetings", "english": "You are welcome", "foreign": "స్వాగతం", "romanized": "Swaagatham", "audio_text": "స్వాగతం"},
        {"category": "Greetings", "english": "How are you?", "foreign": "మీరు ఎలా ఉన్నారు?", "romanized": "Meeru ela unnaaru?", "audio_text": "మీరు ఎలా ఉన్నారు?"},
        {"category": "Greetings", "english": "I am fine, thank you", "foreign": "నేను బాగున్నాను, ధన్యవాదాలు", "romanized": "Nenu baagunnanu, dhanyavaadalu", "audio_text": "నేను బాగున్నాను"},
        {"category": "Greetings", "english": "What is your name?", "foreign": "మీ పేరు ఏమిటి?", "romanized": "Mee peru emiti?", "audio_text": "మీ పేరు ఏమిటి?"},
        {"category": "Greetings", "english": "Nice to meet you", "foreign": "మిమ్మల్ని కలవడం చాలా సంతోషం", "romanized": "Mimmalni kalavadam chaala santhosham", "audio_text": "మిమ్మల్ని కలవడం సంతోషం"},
        {"category": "Greetings", "english": "See you again", "foreign": "మళ్ళీ కలుద్దాం", "romanized": "Mallee kaluddhaam", "audio_text": "మళ్ళీ కలుద్దాం"},

        # Dining (10)
        {"category": "Dining", "english": "The food is very good", "foreign": "భోజనం చాలా బాగుంది", "romanized": "Bhojanam chaala baagundi", "audio_text": "భోజనం చాలా బాగుంది"},
        {"category": "Dining", "english": "Please bring the bill", "foreign": "దయచేసి బిల్ ఇవ్వండి", "romanized": "Dayachesi bill ivvandi", "audio_text": "దయచేసి బిల్ ఇవ్వండి"},
        {"category": "Dining", "english": "Please give drinking water", "foreign": "దయచేసి తాగే నీరు ఇవ్వండి", "romanized": "Dayachesi thaage neeru ivvandi", "audio_text": "దయచేసి తాగే నీరు ఇవ్వండి"},
        {"category": "Dining", "english": "Is this vegetarian?", "foreign": "ఇది శాకాహార భోజనమా?", "romanized": "Idi shaakaahaara bhojanamaa?", "audio_text": "ఇది శాకాహార భోజనమా?"},
        {"category": "Dining", "english": "Make it less spicy, please", "foreign": "కారం తక్కువ వేయండి", "romanized": "Kaaram thakkuva veyandi", "audio_text": "కారం తక్కువ వేయండి"},
        {"category": "Dining", "english": "Please give one plate Hyderabadi Biryani", "foreign": "ఒక ప్లేట్ బిర్యానీ ఇవ్వండి", "romanized": "Oka plate biryani ivvandi", "audio_text": "ఒక ప్లేట్ బిర్యానీ ఇవ్వండి"},
        {"category": "Dining", "english": "Can I have one hot coffee / tea?", "foreign": "ఒక వేడి కాఫీ లేదా టీ ఇవ్వండి", "romanized": "Oka vedi coffee leda tea ivvandi", "audio_text": "ఒక కాఫీ ఇవ్వండి"},
        {"category": "Dining", "english": "A table for two, please", "foreign": "ఇద్దరికీ టేబుల్ కావాలి", "romanized": "Iddariki table kaavali", "audio_text": "ఇద్దరికీ టేబుల్ కావాలి"},
        {"category": "Dining", "english": "What is the chef special dish today?", "foreign": "ఈ రోజు స్పెషల్ ఏమిటి?", "romanized": "Ee roju special emiti?", "audio_text": "ఈ రోజు స్పెషల్ ఏమిటి?"},
        {"category": "Dining", "english": "Can I see the food menu?", "foreign": "మెనూ కార్డు ఇవ్వండి", "romanized": "Menu card ivvandi", "audio_text": "మెనూ కార్డు ఇవ్వండి"},

        # Transport (10)
        {"category": "Transport", "english": "Where is the station / bus stop?", "foreign": "రైల్వే స్టేషన్ లేదా బస్ స్టాప్ ఎక్కడ ఉంది?", "romanized": "Railway station leda bus stop ekkada undi?", "audio_text": "స్టేషన్ ఎక్కడ ఉంది?"},
        {"category": "Transport", "english": "Please turn on the meter", "foreign": "దయచేసి మీటర్ వేయండి", "romanized": "Dayachesi meter veyandi", "audio_text": "దయచేసి మీటర్ వేయండి"},
        {"category": "Transport", "english": "Please stop the vehicle here", "foreign": "ఇక్కడ బండి ఆపండి", "romanized": "Ikkada bandi aapandi", "audio_text": "ఇక్కడ బండి ఆపండి"},
        {"category": "Transport", "english": "How far is the airport?", "foreign": "విమానాశ్రయం ఎంత దూరం?", "romanized": "Vimaanaashrayam entha dooram?", "audio_text": "విమానాశ్రయం ఎంత దూరం?"},
        {"category": "Transport", "english": "I want to go to Charminar / Hitec City", "foreign": "నేను చార్మినార్ వెళ్ళాలి", "romanized": "Nenu Charminar vellali", "audio_text": "నేను చార్మినార్ వెళ్ళాలి"},
        {"category": "Transport", "english": "How much is the auto fare?", "foreign": "ఆటో ఛార్జ్ ఎంత?", "romanized": "Auto charge entha?", "audio_text": "ఆటో ఛార్జ్ ఎంత?"},
        {"category": "Transport", "english": "Where can I get a metro train token?", "foreign": "మెట్రో టోకెన్ ఎక్కడ దొరుకుతుంది?", "romanized": "Metro token ekkada dorukuthundi?", "audio_text": "మెట్రో టోకెన్ ఎక్కడ దొరుకుతుంది?"},
        {"category": "Transport", "english": "What time does the train arrive?", "foreign": "రైలు ఎన్ని గంటలకు వస్తుంది?", "romanized": "Railu enni gantalaku vasthundi?", "audio_text": "రైలు ఎన్ని గంటలకు వస్తుంది?"},
        {"category": "Transport", "english": "Does this bus go to the city center?", "foreign": "ఈ బస్సు సిటీ సెంటర్ కి వెళ్తుందా?", "romanized": "Ee bus city center ki velthundaa?", "audio_text": "ఈ బస్సు వెళ్తుందా?"},
        {"category": "Transport", "english": "Can you book a cab for me?", "foreign": "నాకు క్యాబ్ బుక్ చేయగలరా?", "romanized": "Naaku cab book cheyagalaraa?", "audio_text": "క్యాబ్ బుక్ చేయగలరా?"},

        # Shopping (10)
        {"category": "Shopping", "english": "How much does this cost?", "foreign": "ఇది ఎంత?", "romanized": "Idi entha?", "audio_text": "ఇది ఎంత?"},
        {"category": "Shopping", "english": "Can you reduce the price a bit?", "foreign": "కొంచెం ధర తగ్గించగలరా?", "romanized": "Konchem dhara thagginchagalaraa?", "audio_text": "కొంచెం ధర తగ్గించగలరా?"},
        {"category": "Shopping", "english": "Do you accept PhonePe, GPay or Card?", "foreign": "యూపీఐ లేదా కార్డ్ తీసుకుంటారా?", "romanized": "UPI leda card theesukuntaaraa?", "audio_text": "యూపీఐ తీసుకుంటారా?"},
        {"category": "Shopping", "english": "I will buy this one", "foreign": "నేను ఇది తీసుకుంటాను", "romanized": "Nenu idi theesukuntaanu", "audio_text": "నేను ఇది తీసుకుంటాను"},
        {"category": "Shopping", "english": "Can you show me another size or color?", "foreign": "వేరే కలర్ లేదా సైజు ఉందా?", "romanized": "Vere color leda size undaa?", "audio_text": "వేరే సైజు ఉందా?"},
        {"category": "Shopping", "english": "This item is very nice", "foreign": "ఇది చాలా బాగుంది", "romanized": "Idi chaala baagundi", "audio_text": "ఇది చాలా బాగుంది"},
        {"category": "Shopping", "english": "Please give me the bill", "foreign": "దయచేసి బిల్ ఇవ్వండి", "romanized": "Dayachesi bill ivvandi", "audio_text": "దయచేసి బిల్ ఇవ్వండి"},
        {"category": "Shopping", "english": "Where can I buy traditional pearls / sarees?", "foreign": "ముత్యాలు లేదా చీరలు ఎక్కడ దొరుకుతాయి?", "romanized": "Muthyaalu leda cheeralu ekkada dorukuthaayi?", "audio_text": "ముత్యాలు ఎక్కడ దొరుకుతాయి?"},
        {"category": "Shopping", "english": "Can you pack this as a gift?", "foreign": "గిఫ్ట్ ప్యాక్ చేయగలరా?", "romanized": "Gift pack cheyagalaraa?", "audio_text": "గిఫ్ట్ ప్యాక్ చేయగలరా?"},
        {"category": "Shopping", "english": "What time do the stores close?", "foreign": "షాపులు ఎన్ని గంటలకు మూస్తారు?", "romanized": "Shop-lu enni gantalaku moosthaaru?", "audio_text": "షాపులు ఎన్ని గంటలకు మూస్తారు?"},

        # Emergency (10)
        {"category": "Emergency", "english": "Please help me immediately", "foreign": "దయచేసి నాకు సహాయం చేయండి", "romanized": "Dayachesi naaku sahaayam cheyandi", "audio_text": "దయచేసి నాకు సహాయం చేయండి"},
        {"category": "Emergency", "english": "I need a doctor immediately", "foreign": "నాకు వెంటనే డాక్టర్ కావాలి", "romanized": "Naaku ventane doctor kaavaali", "audio_text": "నాకు వెంటనే డాక్టర్ కావాలి"},
        {"category": "Emergency", "english": "Call the police right now", "foreign": "పోలీసులకు ఫోన్ చేయండి", "romanized": "Police-laku phone cheyandi", "audio_text": "పోలీసులకు ఫోన్ చేయండి"},
        {"category": "Emergency", "english": "I lost my bag and phone", "foreign": "నా బ్యాగ్ మరియు ఫోన్ పోయింది", "romanized": "Naa bag mariyu phone poyindi", "audio_text": "నా ఫోన్ పోయింది"},
        {"category": "Emergency", "english": "Call an ambulance immediately", "foreign": "వెంటనే అంబులెన్స్ పిలవండి", "romanized": "Ventane ambulance pilavandi", "audio_text": "అంబులెన్స్ పిలవండి"},
        {"category": "Emergency", "english": "I am feeling unwell / feverish", "foreign": "నాకు ఒంట్లో బాగోలేదు", "romanized": "Naaku ontlo baagoledu", "audio_text": "నాకు బాగోలేదు"},
        {"category": "Emergency", "english": "An accident has occurred here", "foreign": "ఇక్కడ ప్రమాదం జరిగింది", "romanized": "Ikkada pramaadam jarigindi", "audio_text": "ప్రమాదం జరిగింది"},
        {"category": "Emergency", "english": "Where is the emergency hospital?", "foreign": "ఎమర్జెన్సీ ఆసుపత్రి ఎక్కడ ఉంది?", "romanized": "Emergency aasupathri ekkada undi?", "audio_text": "ఆసుపత్రి ఎక్కడ ఉంది?"},
        {"category": "Emergency", "english": "I am allergic to peanuts", "foreign": "నాకు వేరుశనగ అలర్జీ ఉంది", "romanized": "Naaku verusanaga allergy undi", "audio_text": "నాకు అలర్జీ ఉంది"},
        {"category": "Emergency", "english": "I lost my way, please guide me", "foreign": "నేను దారి తప్పాను, సహాయం చేయండి", "romanized": "Nenu daari thappaanu, sahaayam cheyandi", "audio_text": "సహాయం చేయండి"},

        # Directions (10)
        {"category": "Directions", "english": "Where is the nearest ATM?", "foreign": "దగ్గర్లో ఏటీఎం ఎక్కడ ఉంది?", "romanized": "Daggarlo ATM ekkada undi?", "audio_text": "దగ్గర్లో ఏటీఎం ఎక్కడ ఉంది?"},
        {"category": "Directions", "english": "Turn left / Turn right", "foreign": "ఎడమవైపు తిరగండి / కుడివైపు తిరగండి", "romanized": "Edamavaipu thiragandi / Kudivaipu thiragandi", "audio_text": "ఎడమవైపు తిరగండి"},
        {"category": "Directions", "english": "Go straight down this road", "foreign": "ఈ రోడ్డులో తిన్నగా వెళ్ళండి", "romanized": "Ee road-lo thinnaga vellandi", "audio_text": "తిన్నగా వెళ్ళండి"},
        {"category": "Directions", "english": "Where is the nearest medical store / pharmacy?", "foreign": "దగ్గర్లో మందుల షాప్ ఎక్కడ ఉంది?", "romanized": "Daggarlo mandula shop ekkada undi?", "audio_text": "మందుల షాప్ ఎక్కడ ఉంది?"},
        {"category": "Directions", "english": "How far is the lake / monument on foot?", "foreign": "నడక దూరంలో ఉందా?", "romanized": "Nadaka dooramlo undaa?", "audio_text": "నడక దూరంలో ఉందా?"},
        {"category": "Directions", "english": "Where is the public washroom?", "foreign": "వాష్ రూమ్ ఎక్కడ ఉంది?", "romanized": "Washroom ekkada undi?", "audio_text": "వాష్ రూమ్ ఎక్కడ ఉంది?"},
        {"category": "Directions", "english": "Is this the road to the airport?", "foreign": "ఇది ఎయిర్ పోర్ట్ కి వెళ్లే దారేనా?", "romanized": "Idi airport ki velle daarenaa?", "audio_text": "ఇది ఎయిర్ పోర్ట్ దారేనా?"},
        {"category": "Directions", "english": "Where is the entrance gate?", "foreign": "ప్రవేశ ద్వారం ఎక్కడ?", "romanized": "Pravesha dwaaram ekkada?", "audio_text": "ప్రవేశ ద్వారం ఎక్కడ?"},
        {"category": "Directions", "english": "Can you show the route on map?", "foreign": "మ్యాప్ లో రూట్ చూపించగలరా?", "romanized": "Map lo route choopinchagalaraa?", "audio_text": "మ్యాప్ లో చూపించగలరా?"},
        {"category": "Directions", "english": "Which bus goes to Secunderabad?", "foreign": "సికింద్రాబాద్ కి ఏ బస్సు వెళ్తుంది?", "romanized": "Secunderabad ki ee bus velthundi?", "audio_text": "ఏ బస్సు వెళ్తుంది?"}
    ],
    "bengali": [
        # Greetings (10)
        {"category": "Greetings", "english": "Hello / Greetings", "foreign": "নমস্কার", "romanized": "Nomoshkar", "audio_text": "নমস্কার"},
        {"category": "Greetings", "english": "Good morning", "foreign": "সুপ্রভাত", "romanized": "Suprobhat", "audio_text": "সুপ্রভাত"},
        {"category": "Greetings", "english": "Good evening", "foreign": "শুভ সন্ধ্যা", "romanized": "Shubho Shondhya", "audio_text": "শুভ সন্ধ্যা"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "অনেক ধন্যবাদ", "romanized": "Onek Dhonnobad", "audio_text": "অনেক ধন্যবাদ"},
        {"category": "Greetings", "english": "You are welcome", "foreign": "স্বাগতম", "romanized": "Swagatom", "audio_text": "স্বাগতম"},
        {"category": "Greetings", "english": "How are you?", "foreign": "আপনি কেমন আছেন?", "romanized": "Aapni kemon aachen?", "audio_text": "আপনি কেমন আছেন?"},
        {"category": "Greetings", "english": "I am fine", "foreign": "আমি ভালো আছি", "romanized": "Aami bhaalo aachi", "audio_text": "আমি ভালো আছি"},
        {"category": "Greetings", "english": "What is your name?", "foreign": "আপনার নাম কি?", "romanized": "Aapnar naam ki?", "audio_text": "আপনার নাম কি?"},
        {"category": "Greetings", "english": "Nice to meet you", "foreign": "আপনার সাথে দেখা হয়ে ভালো লাগলো", "romanized": "Aapnar saathe dekha hoye bhaalo laaglo", "audio_text": "দেখা হয়ে ভালো লাগলো"},
        {"category": "Greetings", "english": "See you later", "foreign": "আবার দেখা হবে", "romanized": "Aabaar dekha hobe", "audio_text": "আবার দেখা হবে"},

        # Dining (10)
        {"category": "Dining", "english": "The food is very tasty", "foreign": "খাবারটা খুব সুস্বাদু", "romanized": "Khabarta khub shushwadu", "audio_text": "খাবারটা খুব সুস্বাদু"},
        {"category": "Dining", "english": "Please bring the bill", "foreign": "বিলটা নিয়ে আসুন", "romanized": "Bill-ta niye aashun", "audio_text": "বিলটা নিয়ে আসুন"},
        {"category": "Dining", "english": "Give me one cup of hot tea", "foreign": "এক কাপ গরম চা দিন", "romanized": "Ek cup gorom chaa din", "audio_text": "এক কাপ চা দিন"},
        {"category": "Dining", "english": "Please give drinking water", "foreign": "আমাকে খাওয়ার জল দিন", "romanized": "Aamake khaowar jol din", "audio_text": "আমাকে খাওয়ার জল দিন"},
        {"category": "Dining", "english": "Is this fish curry fresh?", "foreign": "এই মাছের ঝোলটা কি তাজা?", "romanized": "Ei maacher jhol-ta ki taaja?", "audio_text": "এই মাছটা কি তাজা?"},
        {"category": "Dining", "english": "Please make it less spicy", "foreign": "ঝাল একটু কম দেবেন", "romanized": "Jhaal ektu kom deben", "audio_text": "ঝাল কম দেবেন"},
        {"category": "Dining", "english": "Is this vegetarian?", "foreign": "এটা কি নিরামিষ খাবার?", "romanized": "Eta ki niraamish khabaar?", "audio_text": "এটা কি নিরামিষ খাবার?"},
        {"category": "Dining", "english": "Give me two pieces of Rosogolla", "foreign": "দুটো রসগোল্লা দিন", "romanized": "Duto Rosogolla din", "audio_text": "দুটো রসগোল্লা দিন"},
        {"category": "Dining", "english": "A table for two, please", "foreign": "দুজনের জন্য একটা টেবিল দিন", "romanized": "Dujoner jonno ekta table din", "audio_text": "দুজনের জন্য টেবিল দিন"},
        {"category": "Dining", "english": "Can I see the food menu?", "foreign": "মেনু কার্ডটা একটু দেবেন?", "romanized": "Menu card-ta ektu deben?", "audio_text": "মেনু কার্ডটা দেবেন?"},

        # Transport (10)
        {"category": "Transport", "english": "Where is the station / bus stand?", "foreign": "স্টেশনটি বা বাস স্ট্যান্ড কোথায়?", "romanized": "Station-ti baa bus stand kothay?", "audio_text": "স্টেশনটি কোথায়?"},
        {"category": "Transport", "english": "Please stop the taxi here", "foreign": "এখানে ট্যাক্সিটা থামান", "romanized": "Ekhane taxi-ta thaamaan", "audio_text": "এখানে ট্যাক্সিটা থামান"},
        {"category": "Transport", "english": "I want to go to Howrah Station", "foreign": "আমি হাওড়া স্টেশনে যেতে চাই", "romanized": "Aami Howrah station-e jete chaai", "audio_text": "আমি হাওড়া যেতে চাই"},
        {"category": "Transport", "english": "Please turn on the taxi meter", "foreign": "দয়া করে মিটার চালু করুন", "romanized": "Doya kore meter chaalu korun", "audio_text": "মিটার চালু করুন"},
        {"category": "Transport", "english": "How far is the airport?", "foreign": "বিমানবন্দর কত দূর?", "romanized": "Bimaan-bondor koto door?", "audio_text": "বিমানবন্দর কত দূর?"},
        {"category": "Transport", "english": "Where can I get a metro card / ticket?", "foreign": "মেট্রো টিকিট কোথায় পাওয়া যাবে?", "romanized": "Metro ticket kothay paawa jaabe?", "audio_text": "মেট্রো টিকিট কোথায় পাওয়া যাবে?"},
        {"category": "Transport", "english": "How much is the yellow taxi fare?", "foreign": "ট্যাক্সি ভাড়া কত?", "romanized": "Taxi bhaara koto?", "audio_text": "ট্যাক্সি ভাড়া কত?"},
        {"category": "Transport", "english": "What time is the next train?", "foreign": "পরের ট্রেন কটার সময়?", "romanized": "Porer train kotar shomoy?", "audio_text": "পরের ট্রেন কটার সময়?"},
        {"category": "Transport", "english": "Does this bus go to Park Street?", "foreign": "এই বাসটা কি পার্ক স্ট্রিট যাবে?", "romanized": "Ei bus-ta ki Park Street jaabe?", "audio_text": "এই বাসটা কি পার্ক স্ট্রিট যাবে?"},
        {"category": "Transport", "english": "Can you call a cab for me?", "foreign": "আমার জন্য একটা ক্যাব ডাকতে পারেন?", "romanized": "Aamar jonno ekta cab daakte paaren?", "audio_text": "একটা ক্যাব ডাকতে পারেন?"},

        # Shopping (10)
        {"category": "Shopping", "english": "What is the price of this?", "foreign": "এটার দাম কত?", "romanized": "Etar daam koto?", "audio_text": "এটার দাম কত?"},
        {"category": "Shopping", "english": "Can you lower the price a little?", "foreign": "একটু কম রাখা যাবে?", "romanized": "Ektu kom raakha jaabe?", "audio_text": "একটু কম রাখা যাবে?"},
        {"category": "Shopping", "english": "Do you accept UPI, Card or Cash?", "foreign": "ইউপিআই বা কার্ড নেবেন?", "romanized": "UPI baa card neben?", "audio_text": "ইউপিআই বা কার্ড নেবেন?"},
        {"category": "Shopping", "english": "I will buy this one", "foreign": "আমি এটা নেব", "romanized": "Aami eta nebo", "audio_text": "আমি এটা নেব"},
        {"category": "Shopping", "english": "Can you show me another color?", "foreign": "অন্য কোনো রঙ আছে?", "romanized": "Onno kono rong aache?", "audio_text": "অন্য রঙ আছে?"},
        {"category": "Shopping", "english": "This saree / handicraft is very nice", "foreign": "শাড়িটা খুব সুন্দর", "romanized": "Shari-ta khub shundor", "audio_text": "শাড়িটা খুব সুন্দর"},
        {"category": "Shopping", "english": "Please give me the cash memo / receipt", "foreign": "রসিদটা দিন", "romanized": "Roshid-ta din", "audio_text": "রসিদটা দিন"},
        {"category": "Shopping", "english": "Where can I buy traditional sweets?", "foreign": "ভালো মিষ্টির দোকান কোথায়?", "romanized": "Bhaalo mishtir dokan kothay?", "audio_text": "মিষ্টির দোকান কোথায়?"},
        {"category": "Shopping", "english": "Can you pack it as a gift?", "foreign": "উপহার হিসেবে প্যাক করে দেবেন?", "romanized": "Upahaar hishebe pack kore deben?", "audio_text": "প্যাক করে দেবেন?"},
        {"category": "Shopping", "english": "When does New Market close?", "foreign": "মার্কেট কটায় বন্ধ হয়?", "romanized": "Market kotay bondho hoy?", "audio_text": "মার্কেট কটায় বন্ধ হয়?"},

        # Emergency (10)
        {"category": "Emergency", "english": "Please help me immediately", "foreign": "দয়া করে আমাকে সাহায্য করুন", "romanized": "Doya kore amake sahajjo korun", "audio_text": "দয়া করে আমাকে সাহায্য করুন"},
        {"category": "Emergency", "english": "I need a doctor / hospital", "foreign": "আমার একজন ডাক্তার বা হাসপাতাল প্রয়োজন", "romanized": "Aamar ekjon doctor baa hospital proyojon", "audio_text": "আমার একজন ডাক্তার প্রয়োজন"},
        {"category": "Emergency", "english": "Call the police right now", "foreign": "পুলিশকে ডাকুন", "romanized": "Police-ke daakun", "audio_text": "পুলিশকে ডাকুন"},
        {"category": "Emergency", "english": "I lost my passport and wallet", "foreign": "আমার পাসপোর্ট আর মানিব্যাগ হারিয়ে গেছে", "romanized": "Aamar passport aar maanibag haariye geche", "audio_text": "পাসপোর্ট হারিয়ে গেছে"},
        {"category": "Emergency", "english": "Call an ambulance immediately", "foreign": "অ্যাম্বুলেন্স ডাকুন", "romanized": "Ambulance daakun", "audio_text": "অ্যাম্বুলেন্স ডাকুন"},
        {"category": "Emergency", "english": "I feel very sick", "foreign": "আমার শরীর খুব খারাপ লাগছে", "romanized": "Aamar shorir khub kharaap laagche", "audio_text": "শরীর খারাপ লাগছে"},
        {"category": "Emergency", "english": "An accident happened here", "foreign": "এখানে একটা দুর্ঘটনা ঘটেছে", "romanized": "Ekhane ekta durghatna ghoteche", "audio_text": "দুর্ঘটনা ঘটেছে"},
        {"category": "Emergency", "english": "Where is the police station?", "foreign": "থানা কোথায়?", "romanized": "Thaana kothay?", "audio_text": "থানা কোথায়?"},
        {"category": "Emergency", "english": "I am allergic to seafood", "foreign": "আমার সামুদ্রিক খাবারে অ্যালার্জি আছে", "romanized": "Aamar shaamudrik khaabaare allergy aache", "audio_text": "আমার অ্যালার্জি আছে"},
        {"category": "Emergency", "english": "I am lost, can you guide me?", "foreign": "আমি পথ হারিয়ে ফেলেছি, একটু পথ দেখাবেন?", "romanized": "Aami poth haariye felechi, ektu poth dekhaaben?", "audio_text": "একটু পথ দেখাবেন?"},

        # Directions (10)
        {"category": "Directions", "english": "Where is the nearest medical shop?", "foreign": "কাছের ওষুধের দোকান কোথায়?", "romanized": "Kaacher oushodher dokan kothay?", "audio_text": "কাছের ওষুধের দোকান কোথায়?"},
        {"category": "Directions", "english": "Where is the nearest ATM?", "foreign": "কাছের এটিএম কোথায়?", "romanized": "Kaacher ATM kothay?", "audio_text": "কাছের এটিএম কোথায়?"},
        {"category": "Directions", "english": "Go straight and turn left", "foreign": "সোজা গিয়ে বাঁদিকে যান", "romanized": "Soja giye baandike jaan", "audio_text": "সোজা গিয়ে বাঁদিকে যান"},
        {"category": "Directions", "english": "Turn right at the traffic intersection", "foreign": "মোড় থেকে ডানদিকে ঘুরুন", "romanized": "Mor theke daandike ghurun", "audio_text": "ডানদিকে ঘুরুন"},
        {"category": "Directions", "english": "Where is the Victoria Memorial / monument?", "foreign": "স্মারকটি কোন দিকে?", "romanized": "Smaarak-ti kon dike?", "audio_text": "স্মারকটি কোন দিকে?"},
        {"category": "Directions", "english": "Is it within walking distance?", "foreign": "এটা কি হেঁটে যাওয়ার মতো দূরত্ব?", "romanized": "Eta ki hete jaaoaar moto doorotto?", "audio_text": "হেঁটে যাওয়ার দূরত্ব?"},
        {"category": "Directions", "english": "Where is the public washroom / toilet?", "foreign": "শৌচালয় কোথায়?", "romanized": "Shouchaloy kothay?", "audio_text": "শৌচালয় কোথায়?"},
        {"category": "Directions", "english": "Which way is the metro station?", "foreign": "মেট্রো স্টেশন কোন দিকে?", "romanized": "Metro station kon dike?", "audio_text": "মেট্রো স্টেশন কোন দিকে?"},
        {"category": "Directions", "english": "Can you show me the route on Google Maps?", "foreign": "ম্যাপে একটু রাস্তাটা দেখিয়ে দেবেন?", "romanized": "Map-e ektu raasta-ta dekhiye deben?", "audio_text": "ম্যাপে রাস্তাটা দেখিয়ে দেবেন?"},
        {"category": "Directions", "english": "Where is the main entry gate?", "foreign": "মূল প্রবেশদ্বার কোথায়?", "romanized": "Mool probesh-dwaar kothay?", "audio_text": "প্রবেশদ্বার কোথায়?"}
    ],
    "marathi": [
        # Greetings (10)
        {"category": "Greetings", "english": "Hello / Greetings", "foreign": "नमस्कार", "romanized": "Namaskar", "audio_text": "नमस्कार"},
        {"category": "Greetings", "english": "Good morning", "foreign": "शुभ सकाळ", "romanized": "Shubh Sakaal", "audio_text": "शुभ सकाळ"},
        {"category": "Greetings", "english": "Good evening", "foreign": "शुभ संध्याकाळ", "romanized": "Shubh Sandhyakaal", "audio_text": "शुभ संध्याकाळ"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "खूप खूप धन्यवाद", "romanized": "Khoop khoop dhanyavaad", "audio_text": "खूप खूप धन्यवाद"},
        {"category": "Greetings", "english": "You are welcome", "foreign": "आपले स्वागत आहे", "romanized": "Aaple swaagat aahe", "audio_text": "आपले स्वागत आहे"},
        {"category": "Greetings", "english": "How are you?", "foreign": "तुम्ही कसे आहात?", "romanized": "Tumhi kase aahaat?", "audio_text": "तुम्ही कसे आहात?"},
        {"category": "Greetings", "english": "I am fine", "foreign": "मी ठीक आहे", "romanized": "Mee theek aahe", "audio_text": "मी ठीक आहे"},
        {"category": "Greetings", "english": "What is your name?", "foreign": "तुमचे नाव काय आहे?", "romanized": "Tumche naav kaay aahe?", "audio_text": "तुमचे नाव काय आहे?"},
        {"category": "Greetings", "english": "Nice to meet you", "foreign": "तुम्हाला भेटून आनंद झाला", "romanized": "Tumhaala bhetun aanand zhaala", "audio_text": "आनंद झाला"},
        {"category": "Greetings", "english": "See you soon", "foreign": "पुन्हा भेटू", "romanized": "Punha bhetu", "audio_text": "पुन्हा भेटू"},

        # Dining (10)
        {"category": "Dining", "english": "Food is very delicious", "foreign": "जेवण खूप छान आहे", "romanized": "Jevan khoop chhaan aahe", "audio_text": "जेवण खूप छान आहे"},
        {"category": "Dining", "english": "Please bring the bill", "foreign": "कृपया बिल आणा", "romanized": "Kripya bill aana", "audio_text": "कृपया बिल आणा"},
        {"category": "Dining", "english": "Give me one Vada Pav / Misal Pav", "foreign": "एक वडा पाव किंवा मिसळ पाव द्या", "romanized": "Ek Vada Pav kivha Misal Pav dyaa", "audio_text": "एक वडा पाव द्या"},
        {"category": "Dining", "english": "Please give drinking water", "foreign": "पिण्याचे पाणी द्या", "romanized": "Pinyache paani dyaa", "audio_text": "पिण्याचे पाणी द्या"},
        {"category": "Dining", "english": "Make it less spicy", "foreign": "कमी तिखट करा", "romanized": "Kamee thikhat karaa", "audio_text": "कमी तिखट करा"},
        {"category": "Dining", "english": "Is this pure vegetarian?", "foreign": "हे शुद्ध शाकाहारी आहे का?", "romanized": "He shuddha shaakaahaari aahe kaa?", "audio_text": "हे शाकाहारी आहे का?"},
        {"category": "Dining", "english": "Can I have one hot cutting chai?", "foreign": "एक कटिंग चहा मिळेल का?", "romanized": "Ek cutting chahaa milel kaa?", "audio_text": "एक कटिंग चहा मिळेल का?"},
        {"category": "Dining", "english": "A table for two, please", "foreign": "दोघांसाठी टेबल मिळेल का?", "romanized": "Doghaansaathi table milel kaa?", "audio_text": "दोघांसाठी टेबल मिळेल का?"},
        {"category": "Dining", "english": "What is today special dish?", "foreign": "आजचे स्पेशल काय आहे?", "romanized": "Aajche special kaay aahe?", "audio_text": "आजचे स्पेशल काय आहे?"},
        {"category": "Dining", "english": "Please give me the food menu", "foreign": "मेनू कार्ड द्या", "romanized": "Menu card dyaa", "audio_text": "मेनू कार्ड द्या"},

        # Transport (10)
        {"category": "Transport", "english": "Where is the railway station?", "foreign": "रेल्वे स्टेशन कुठे आहे?", "romanized": "Railway station kuthe aahe?", "audio_text": "स्टेशन कुठे आहे?"},
        {"category": "Transport", "english": "Please turn on the meter", "foreign": "कृपया मीटर चालू करा", "romanized": "Kripya meter chaaloo karaa", "audio_text": "कृपया मीटर चालू करा"},
        {"category": "Transport", "english": "Stop the vehicle here", "foreign": "गाडी इथे थांबवा", "romanized": "Gaadi ithe thaambvaa", "audio_text": "गाडी इथे थांबवा"},
        {"category": "Transport", "english": "I want to go to Dadar / CSMT", "foreign": "मला दादरला जायचे आहे", "romanized": "Mala Dadarla jaayche aahe", "audio_text": "मला दादरला जायचे आहे"},
        {"category": "Transport", "english": "How far is the airport?", "foreign": "विमानतळ किती लांब आहे?", "romanized": "Vimaan-tal kiti laamb aahe?", "audio_text": "विमानतळ किती लांब आहे?"},
        {"category": "Transport", "english": "How much is the taxi fare?", "foreign": "टॅक्सीचे भाडे किती होईल?", "romanized": "Taxi-che bhaade kiti hoeel?", "audio_text": "भाडे किती होईल?"},
        {"category": "Transport", "english": "Which platform does the train arrive on?", "foreign": "गाडी कोणत्या प्लॅटफॉर्मवर येईल?", "romanized": "Gaadi konthya platform-var yeel?", "audio_text": "प्लॅटफॉर्म कोणता?"},
        {"category": "Transport", "english": "Where can I get a local train ticket?", "foreign": "लोकलचे तिकीट कुठे मिळेल?", "romanized": "Local-che ticket kuthe milel?", "audio_text": "तिकीट कुठे मिळेल?"},
        {"category": "Transport", "english": "Does this bus go to Gateway of India?", "foreign": "ही बस गेटवे ऑफ इंडियाला जाईल का?", "romanized": "Hee bus Gateway of India-la jaaeel kaa?", "audio_text": "ही बस जाईल का?"},
        {"category": "Transport", "english": "Can you call an auto or cab for me?", "foreign": "माझ्यासाठी रिक्षा बोलावू शकता का?", "romanized": "Maajhyaasaathi rickshaw bolaavoo shaktaa kaa?", "audio_text": "रिक्षा बोलावू शकता का?"},

        # Shopping (10)
        {"category": "Shopping", "english": "How much for this item?", "foreign": "याची किंमत काय आहे?", "romanized": "Yaachi kimmat kaay aahe?", "audio_text": "याची किंमत काय आहे?"},
        {"category": "Shopping", "english": "Can you give a discount?", "foreign": "काही कमी होईल का?", "romanized": "Kaahi kamee hoeel kaa?", "audio_text": "काही कमी होईल का?"},
        {"category": "Shopping", "english": "Do you take online payment or UPI?", "foreign": "गुगल पे किंवा ऑनलाईन चालेल का?", "romanized": "Google Pay kivha online chaalel kaa?", "audio_text": "गुगल पे चालेल का?"},
        {"category": "Shopping", "english": "I will take this one", "foreign": "मी हे घेतो", "romanized": "Mee he gheto", "audio_text": "मी हे घेतो"},
        {"category": "Shopping", "english": "Do you have another color or size?", "foreign": "दुसरा रंग किंवा साईझ आहे का?", "romanized": "Doosra rang kivha size aahe kaa?", "audio_text": "दुसरा साईझ आहे का?"},
        {"category": "Shopping", "english": "This Paithani saree is very nice", "foreign": "ही पैठणी खूप सुंदर आहे", "romanized": "Hee Paithani khoop sundar aahe", "audio_text": "खूप सुंदर आहे"},
        {"category": "Shopping", "english": "Please give me the purchase bill", "foreign": "कृपया पावती द्या", "romanized": "Kripya paavti dyaa", "audio_text": "पावती द्या"},
        {"category": "Shopping", "english": "Where can I buy Alphonso mangoes / sweets?", "foreign": "हापूस आंबे किंवा मिठाई कुठे मिळेल?", "romanized": "Haapoos aambe kivha mithai kuthe milel?", "audio_text": "मिठाई कुठे मिळेल?"},
        {"category": "Shopping", "english": "Can you pack this safely?", "foreign": "हे व्यवस्थित पॅक करून द्याल का?", "romanized": "He vyavasthit pack karoon dyaal kaa?", "audio_text": "पॅक करून द्याल का?"},
        {"category": "Shopping", "english": "What time does the market close?", "foreign": "बाजार किती वाजता बंद होतो?", "romanized": "Baajaar kiti vaajtaa band hoto?", "audio_text": "बाजार कधी बंद होतो?"},

        # Emergency (10)
        {"category": "Emergency", "english": "Please help me immediately", "foreign": "कृपया मला मदत करा", "romanized": "Kripya mala madat kara", "audio_text": "कृपया मला मदत करा"},
        {"category": "Emergency", "english": "Call the police immediately", "foreign": "लगेच पोलिसांना बोलवा", "romanized": "Lagech police-aana bolvaa", "audio_text": "लगेच पोलिसांना बोलवा"},
        {"category": "Emergency", "english": "I need a doctor or hospital", "foreign": "मला डॉक्टर किंवा दवाखान्याची गरज आहे", "romanized": "Mala doctor kivha davaakhaanyaachi garaj aahe", "audio_text": "मला डॉक्टरची गरज आहे"},
        {"category": "Emergency", "english": "I lost my mobile and purse", "foreign": "माझा फोन आणि पाकीट हरवले आहे", "romanized": "Maazha phone aani paakit haravle aahe", "audio_text": "फोन हरवला आहे"},
        {"category": "Emergency", "english": "Please call an ambulance", "foreign": "रुग्णवाहिका बोलवा", "romanized": "Rugnavaahikaa bolvaa", "audio_text": "रुग्णवाहिका बोलवा"},
        {"category": "Emergency", "english": "I am feeling very unwell", "foreign": "मला बरे वाटत नाहीये", "romanized": "Mala bare vaatat naahiye", "audio_text": "मला बरे वाटत नाहीये"},
        {"category": "Emergency", "english": "An accident has occurred here", "foreign": "इथे अपघात झाला आहे", "romanized": "Ithe apghaat zhaala aahe", "audio_text": "अपघात झाला आहे"},
        {"category": "Emergency", "english": "Where is the police station?", "foreign": "पोलीस स्टेशन कुठे आहे?", "romanized": "Police station kuthe aahe?", "audio_text": "पोलीस स्टेशन कुठे आहे?"},
        {"category": "Emergency", "english": "I am allergic to nuts", "foreign": "मला नट्सची ऍलर्जी आहे", "romanized": "Mala nuts-chee allergy aahe", "audio_text": "मला ऍलर्जी आहे"},
        {"category": "Emergency", "english": "I am lost, please help me", "foreign": "मी रस्ता चुकलो आहे, मदत करा", "romanized": "Mee rasta chuklo aahe, madat kara", "audio_text": "मदत करा"},

        # Directions (10)
        {"category": "Directions", "english": "Where is the nearest medical shop / ATM?", "foreign": "जवळचा मेडिकल किंवा एटीएम कुठे आहे?", "romanized": "Javalcha medical kivha ATM kuthe aahe?", "audio_text": "जवळचा मेडिकल कुठे आहे?"},
        {"category": "Directions", "english": "Turn right / Turn left", "foreign": "उजवीकडे वळा / डावीकडे वळा", "romanized": "Ujveekade valaa / Daaveekade valaa", "audio_text": "उजवीकडे वळा"},
        {"category": "Directions", "english": "Go straight ahead", "foreign": "सरळ पुढे जा", "romanized": "Saral pudhe jaa", "audio_text": "सरळ पुढे जा"},
        {"category": "Directions", "english": "How far is the beach / fort on foot?", "foreign": "समुद्रकिनारा किती अंतरावर आहे?", "romanized": "Samudrakinaaraa kiti antraavar aahe?", "audio_text": "समुद्रकिनारा किती लांब आहे?"},
        {"category": "Directions", "english": "Where is the public washroom?", "foreign": "शौचालय कुठे आहे?", "romanized": "Shauchalay kuthe aahe?", "audio_text": "शौचालय कुठे आहे?"},
        {"category": "Directions", "english": "Which local train goes to Churchgate?", "foreign": "चर्चगेटला कोणती लोकल जाते?", "romanized": "Churchgate-la konthi local jaate?", "audio_text": "कोणती लोकल जाते?"},
        {"category": "Directions", "english": "Where is the entrance gate?", "foreign": "प्रवेशद्वार कुठे आहे?", "romanized": "Praveshdwaar kuthe aahe?", "audio_text": "प्रवेशद्वार कुठे आहे?"},
        {"category": "Directions", "english": "Can you show the way on Google Maps?", "foreign": "मॅपवर रस्ता दाखवू शकता का?", "romanized": "Map-var rasta daakhvoo shaktaa kaa?", "audio_text": "रस्ता दाखवू शकता का?"},
        {"category": "Directions", "english": "Is this the correct way to Marine Drive?", "foreign": "मरीन ड्राईव्हचा हाच रस्ता आहे का?", "romanized": "Marine Drive-cha haach rasta aahe kaa?", "audio_text": "हाच रस्ता आहे का?"},
        {"category": "Directions", "english": "Where is the nearest bus depot?", "foreign": "जवळचे बस डेपो कुठे आहे?", "romanized": "Javalche bus depot kuthe aahe?", "audio_text": "बस डेपो कुठे आहे?"}
    ],
    "urdu": [
        # Greetings (10)
        {"category": "Greetings", "english": "Hello / Peace be upon you", "foreign": "السلام علیکم", "romanized": "Assalam-o-Alaikum", "audio_text": "السلام علیکم"},
        {"category": "Greetings", "english": "Good morning", "foreign": "صبح بخیر", "romanized": "Subah bakhair", "audio_text": "صبح بخیر"},
        {"category": "Greetings", "english": "Good evening", "foreign": "شام بخیر", "romanized": "Shaam bakhair", "audio_text": "شام بخیر"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "بہت بہت شکریہ", "romanized": "Bahut bahut shukriya", "audio_text": "بہت بہت شکریہ"},
        {"category": "Greetings", "english": "You are welcome", "foreign": "خوش آمدید", "romanized": "Khush aamdeed", "audio_text": "خوش آمدید"},
        {"category": "Greetings", "english": "How are you?", "foreign": "آپ کیسے ہیں؟", "romanized": "Aap kaise hain?", "audio_text": "آپ کیسے ہیں؟"},
        {"category": "Greetings", "english": "I am fine, thank you", "foreign": "میں ٹھیک ہوں، شکریہ", "romanized": "Main theek hoon, shukriya", "audio_text": "میں ٹھیک ہوں"},
        {"category": "Greetings", "english": "What is your name?", "foreign": "آپ کا نام کیا ہے؟", "romanized": "Aap ka naam kya hai?", "audio_text": "آپ کا نام کیا ہے؟"},
        {"category": "Greetings", "english": "Nice to meet you", "foreign": "آپ سے مل کر خوشی ہوئی", "romanized": "Aap se mil kar khushi hui", "audio_text": "آپ سے مل کر خوشی ہوئی"},
        {"category": "Greetings", "english": "Goodbye / May Allah protect you", "foreign": "خدا حافظ", "romanized": "Khuda hafiz", "audio_text": "خدا حافظ"},

        # Dining (10)
        {"category": "Dining", "english": "The food is extremely delicious", "foreign": "کھانا بہت لذیذ ہے", "romanized": "Khaana bahut lazeez hai", "audio_text": "کھانا بہت لذیذ ہے"},
        {"category": "Dining", "english": "Please bring the bill", "foreign": "براہ کرم بل لائیں", "romanized": "Barahe-karam bill laayen", "audio_text": "براہ کرم بل لائیں"},
        {"category": "Dining", "english": "Please give drinking water", "foreign": "پینے کا پانی دیجیے", "romanized": "Peene ka paani dijiye", "audio_text": "پینے کا پانی دیجیے"},
        {"category": "Dining", "english": "Is this meat halal?", "foreign": "کیا یہ کھانا حلال ہے؟", "romanized": "Kya yeh khaana halal hai?", "audio_text": "کیا یہ کھانا حلال ہے؟"},
        {"category": "Dining", "english": "Please make it less spicy", "foreign": "مرچ کم رکھیے گا", "romanized": "Mirch kam rakhiye gaa", "audio_text": "مرچ کم رکھیے گا"},
        {"category": "Dining", "english": "Give me one plate mutton biryani / kebabs", "foreign": "ایک پلیٹ بریانی دیجیے", "romanized": "Ek plate biryani dijiye", "audio_text": "ایک پلیٹ بریانی دیجیے"},
        {"category": "Dining", "english": "Can I have hot tea / chai?", "foreign": "ایک کپ گرما گرم چائے ملے گی؟", "romanized": "Ek cup garma garam chai milegi?", "audio_text": "ایک کپ چائے ملے گی؟"},
        {"category": "Dining", "english": "A table for two, please", "foreign": "دو افراد کے لیے میز چاہیے", "romanized": "Do afraad ke liye mez chahiye", "audio_text": "دو افراد کے لیے میز چاہیے"},
        {"category": "Dining", "english": "What is today special dish?", "foreign": "آج کی خاص ڈش کیا ہے؟", "romanized": "Aaj ki khaas dish kya hai?", "audio_text": "آج کی خاص ڈش کیا ہے؟"},
        {"category": "Dining", "english": "Please show me the food menu", "foreign": "کھانے کا مینو دکھائیے", "romanized": "Khaane ka menu dikhaiye", "audio_text": "مینو دکھائیے"},

        # Transport (10)
        {"category": "Transport", "english": "Where is the railway station / bus stand?", "foreign": "ریلوے اسٹیشن کہاں ہے؟", "romanized": "Railway station kahan hai?", "audio_text": "اسٹیشن کہاں ہے؟"},
        {"category": "Transport", "english": "Please stop the car here", "foreign": "گاڑی یہاں روکیں", "romanized": "Gaadi yahan rokein", "audio_text": "گاڑی یہاں روکیں"},
        {"category": "Transport", "english": "Please turn on the meter", "foreign": "میٹر چالو کیجیے", "romanized": "Meter chaaloo kijiye", "audio_text": "میٹر چالو کیجیے"},
        {"category": "Transport", "english": "How far is the airport?", "foreign": "ہوائی اڈہ کتنی دور ہے؟", "romanized": "Hawai adda kitni door hai?", "audio_text": "ہوائی اڈہ کتنی دور ہے؟"},
        {"category": "Transport", "english": "I want to go to this destination", "foreign": "مجھے اس پتے پر جانا ہے", "romanized": "Mujhe is pate par jaana hai", "audio_text": "مجھے اس پتے پر جانا ہے"},
        {"category": "Transport", "english": "How much is the taxi fare?", "foreign": "ٹیکسی کا کرایہ کتنا ہوگا؟", "romanized": "Taxi ka kiraya kitna hoga?", "audio_text": "کرایہ کتنا ہوگا؟"},
        {"category": "Transport", "english": "What time does the train leave?", "foreign": "ٹرین کتنے بجے روانہ ہوگی؟", "romanized": "Train kitne baje rawana hogi?", "audio_text": "ٹرین کتنے بجے روانہ ہوگی؟"},
        {"category": "Transport", "english": "Where can I buy tickets?", "foreign": "ٹکٹ کہاں سے ملے گا؟", "romanized": "Ticket kahan se milega?", "audio_text": "ٹکٹ کہاں سے ملے گا؟"},
        {"category": "Transport", "english": "Does this bus go to the old city?", "foreign": "کیا یہ بس پرانے شہر جاتی ہے؟", "romanized": "Kya yeh bus purane shahar jaati hai?", "audio_text": "کیا یہ بس جاتی ہے؟"},
        {"category": "Transport", "english": "Can you call a cab for me?", "foreign": "کیا آپ میرے لیے ٹیکسی منگوا سکتے ہیں؟", "romanized": "Kya aap mere liye taxi mangwa sakte hain?", "audio_text": "ٹیکسی منگوا سکتے ہیں؟"},

        # Shopping (10)
        {"category": "Shopping", "english": "What is the price of this?", "foreign": "اس کی قیمت کیا ہے؟", "romanized": "Is ki qeemat kya hai?", "audio_text": "اس کی قیمت کیا ہے؟"},
        {"category": "Shopping", "english": "Can you reduce the price a bit?", "foreign": "کیا کچھ رعایت مل سکتی ہے؟", "romanized": "Kya kuch riaayat mil sakti hai?", "audio_text": "کیا کچھ رعایت مل سکتی ہے؟"},
        {"category": "Shopping", "english": "Do you take card or digital payment?", "foreign": "کیا آپ کارڈ یا آن لائن پیمنٹ لیتے ہیں؟", "romanized": "Kya aap card ya online payment lete hain?", "audio_text": "کیا آپ کارڈ لیتے ہیں؟"},
        {"category": "Shopping", "english": "I will buy this one", "foreign": "میں یہ لوں گا", "romanized": "Main yeh loon gaa", "audio_text": "میں یہ لوں گا"},
        {"category": "Shopping", "english": "Do you have another color or size?", "foreign": "کیا کوئی دوسرا رنگ یا سائز ہے؟", "romanized": "Kya koi doosra rang ya size hai?", "audio_text": "دوسرا سائز ہے؟"},
        {"category": "Shopping", "english": "This item is very good quality", "foreign": "یہ چیز بہت اعلیٰ ہے", "romanized": "Yeh cheez bahut aala hai", "audio_text": "یہ چیز بہت اعلیٰ ہے"},
        {"category": "Shopping", "english": "Please give me the receipt", "foreign": "براہ کرم رسید دیجیے", "romanized": "Barahe-karam raseed dijiye", "audio_text": "رسید دیجیے"},
        {"category": "Shopping", "english": "Where can I find traditional perfumes / attar?", "foreign": "خالص عطر کہاں ملے گا؟", "romanized": "Khaalis attar kahan milega?", "audio_text": "عطر کہاں ملے گا؟"},
        {"category": "Shopping", "english": "Can you pack this as a gift?", "foreign": "کیا آپ اسے گفٹ پیک کر سکتے ہیں؟", "romanized": "Kya aap ise gift pack kar sakte hain?", "audio_text": "گفٹ پیک کر سکتے ہیں؟"},
        {"category": "Shopping", "english": "What time does the market close?", "foreign": "بازار کتنے بجے بند ہوتا ہے؟", "romanized": "Bazaar kitne baje band hota hai?", "audio_text": "بازار کب بند ہوتا ہے؟"},

        # Emergency (10)
        {"category": "Emergency", "english": "Please help me immediately", "foreign": "براہ کرم میری مدد کریں", "romanized": "Barahe-karam meri madad karen", "audio_text": "براہ کرم میری مدد کریں"},
        {"category": "Emergency", "english": "I need a doctor or hospital", "foreign": "مجھے ڈاکٹر یا ہسپتال کی ضرورت ہے", "romanized": "Mujhe doctor ya aspatal ki zaroorat hai", "audio_text": "مجھے ڈاکٹر کی ضرورت ہے"},
        {"category": "Emergency", "english": "Call the police right now", "foreign": "فوراً پولیس کو بلائیں", "romanized": "Foran police ko bulaayen", "audio_text": "پولیس کو بلائیں"},
        {"category": "Emergency", "english": "I lost my passport and wallet", "foreign": "میرا پاسپورٹ اور پرس گم ہو گیا ہے", "romanized": "Mera passport aur purse gum ho gaya hai", "audio_text": "پاسپورٹ گم ہو گیا ہے"},
        {"category": "Emergency", "english": "Call an ambulance immediately", "foreign": "فوراً ایمبولینس بلائیں", "romanized": "Foran ambulance bulaayen", "audio_text": "ایمبولینس بلائیں"},
        {"category": "Emergency", "english": "I am feeling very ill", "foreign": "میری طبیعت بہت خراب ہے", "romanized": "Meri tabiyat bahut kharab hai", "audio_text": "طبیعت خراب ہے"},
        {"category": "Emergency", "english": "There has been an accident", "foreign": "یہاں ایک حادثہ ہو گیا ہے", "romanized": "Yahan ek haadsa ho gaya hai", "audio_text": "حادثہ ہو گیا ہے"},
        {"category": "Emergency", "english": "Where is the nearest police station?", "foreign": "تھانہ کہاں پر ہے؟", "romanized": "Thaana kahan par hai?", "audio_text": "تھانہ کہاں ہے؟"},
        {"category": "Emergency", "english": "I am allergic to certain medications", "foreign": "مجھے دواؤں سے الرجی ہے", "romanized": "Mujhe dawaon se allergy hai", "audio_text": "مجھے الرجی ہے"},
        {"category": "Emergency", "english": "I am lost, please guide me", "foreign": "میں راستہ بھول گیا ہوں، مدد کیجیے", "romanized": "Main raasta bhool gaya hoon, madad kijiye", "audio_text": "مدد کیجیے"},

        # Directions (10)
        {"category": "Directions", "english": "Where is the nearest ATM or bank?", "foreign": "قریبی اے ٹی ایم کہاں ہے؟", "romanized": "Qareebi ATM kahan hai?", "audio_text": "قریبی اے ٹی ایم کہاں ہے؟"},
        {"category": "Directions", "english": "Where is the nearest pharmacy / medical store?", "foreign": "قریبی میڈیکل اسٹور کہاں ہے؟", "romanized": "Qareebi medical store kahan hai?", "audio_text": "میڈیکل اسٹور کہاں ہے؟"},
        {"category": "Directions", "english": "Go straight and turn left", "foreign": "سیدھے جائیں اور بائیں مڑیں", "romanized": "Seedhe jaayen aur baayen mudein", "audio_text": "سیدھے جائیں اور بائیں مڑیں"},
        {"category": "Directions", "english": "Turn right at the traffic signal", "foreign": "اشارے سے دائیں مڑیں", "romanized": "Ishaare se daayen mudein", "audio_text": "دائیں مڑیں"},
        {"category": "Directions", "english": "How far is the historical monument?", "foreign": "تاریخی عمارت کتنی دور ہے؟", "romanized": "Tareekhi imaarat kitni door hai?", "audio_text": "عمارت کتنی دور ہے؟"},
        {"category": "Directions", "english": "Where is the public restroom?", "foreign": "بیت الخلاء کہاں ہے؟", "romanized": "Bait-ul-khala kahan hai?", "audio_text": "بیت الخلاء کہاں ہے؟"},
        {"category": "Directions", "english": "Is it within walking distance?", "foreign": "کیا یہ پیدل فاصلے پر ہے؟", "romanized": "Kya yeh paidal faasle par hai?", "audio_text": "پیدل فاصلے پر ہے؟"},
        {"category": "Directions", "english": "Where is the main entrance gate?", "foreign": "مرکزی دروازہ کہاں ہے؟", "romanized": "Markazi darwaza kahan hai?", "audio_text": "مرکزی دروازہ کہاں ہے؟"},
        {"category": "Directions", "english": "Can you show me the route on Google Maps?", "foreign": "کیا آپ نقشے پر راستہ دکھا سکتے ہیں؟", "romanized": "Kya aap naqshe par raasta dikha sakte hain?", "audio_text": "راستہ دکھا سکتے ہیں؟"},
        {"category": "Directions", "english": "Which way to the Grand Mosque / Bazaar?", "foreign": "جامع مسجد یا بازار کا راستہ کون سا ہے؟", "romanized": "Jaama Masjid ya bazaar ka raasta kon sa hai?", "audio_text": "راستہ کون سا ہے؟"}
    ],
    "japanese": [
        # Greetings (10)
        {"category": "Greetings", "english": "Hello / Good day", "foreign": "こんにちは", "romanized": "Konnichiwa", "audio_text": "こんにちは"},
        {"category": "Greetings", "english": "Good morning", "foreign": "おはようございます", "romanized": "Ohayou gozaimasu", "audio_text": "おはようございます"},
        {"category": "Greetings", "english": "Good evening", "foreign": "こんばんは", "romanized": "Konbanwa", "audio_text": "こんばんは"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "ありがとうございます", "romanized": "Arigatou gozaimasu", "audio_text": "ありがとうございます"},
        {"category": "Greetings", "english": "You are welcome", "foreign": "どういたしまして", "romanized": "Douitashimashite", "audio_text": "どういたしまして"},
        {"category": "Greetings", "english": "Excuse me / Pardon", "foreign": "すみません", "romanized": "Sumimasen", "audio_text": "すみません"},
        {"category": "Greetings", "english": "How are you?", "foreign": "お元気ですか？", "romanized": "Ogenki desu ka?", "audio_text": "お元気ですか"},
        {"category": "Greetings", "english": "I am fine", "foreign": "元気です", "romanized": "Genki desu", "audio_text": "元気です"},
        {"category": "Greetings", "english": "Nice to meet you", "foreign": "はじめまして", "romanized": "Hajimemashite", "audio_text": "はじめまして"},
        {"category": "Greetings", "english": "Goodbye", "foreign": "さようなら", "romanized": "Sayounara", "audio_text": "さようなら"},

        # Dining (10)
        {"category": "Dining", "english": "Check please / Bill please", "foreign": "お会計をお願いします", "romanized": "Okaikei o onegaishimasu", "audio_text": "お会計をお願いします"},
        {"category": "Dining", "english": "Delicious! (compliment to chef)", "foreign": "とても美味しいです！", "romanized": "Totemo oishii desu!", "audio_text": "とても美味しいです"},
        {"category": "Dining", "english": "Water, please", "foreign": "お水をお願いします", "romanized": "Omizu o onegaishimasu", "audio_text": "お水をお願いします"},
        {"category": "Dining", "english": "Menu please", "foreign": "メニューをお願いします", "romanized": "Menyuu o onegaishimasu", "audio_text": "メニューをお願いします"},
        {"category": "Dining", "english": "Is there a vegetarian option?", "foreign": "ベジタリアン料理はありますか？", "romanized": "Bejitarian ryouri wa arimasu ka?", "audio_text": "ベジタリアン料理はありますか"},
        {"category": "Dining", "english": "What do you recommend?", "foreign": "おすすめは何ですか？", "romanized": "Osusume wa nan desu ka?", "audio_text": "おすすめは何ですか"},
        {"category": "Dining", "english": "Table for two, please", "foreign": "2人席をお願いします", "romanized": "Futari seki o onegaishimasu", "audio_text": "2人席をお願いします"},
        {"category": "Dining", "english": "I have an allergy to shellfish", "foreign": "甲殻類アレルギーがあります", "romanized": "Koukakurui arerugii ga arimasu", "audio_text": "アレルギーがあります"},
        {"category": "Dining", "english": "Thank you for the meal (after eating)", "foreign": "ごちそうさまでした", "romanized": "Gochisousama deshita", "audio_text": "ごちそうさまでした"},
        {"category": "Dining", "english": "Can I have one more beer / tea?", "foreign": "もう一杯お願いします", "romanized": "Mou ippai onegaishimasu", "audio_text": "もう一杯お願いします"},

        # Transport (10)
        {"category": "Transport", "english": "Where is the train station?", "foreign": "駅はどこですか？", "romanized": "Eki wa doko desu ka?", "audio_text": "駅はどこですか"},
        {"category": "Transport", "english": "To Tokyo Station, please", "foreign": "東京駅までお願いします", "romanized": "Tokyo eki made onegaishimasu", "audio_text": "東京駅までお願いします"},
        {"category": "Transport", "english": "Where is the ticket vending machine?", "foreign": "券売機はどこですか？", "romanized": "Kenbaiki wa doko desu ka?", "audio_text": "券売機はどこですか"},
        {"category": "Transport", "english": "Which platform for the Shinkansen?", "foreign": "新幹線は何番線ですか？", "romanized": "Shinkansen wa nanbansen desu ka?", "audio_text": "新幹線は何番線ですか"},
        {"category": "Transport", "english": "Does this train go to Shibuya?", "foreign": "この電車は渋谷に行きますか？", "romanized": "Kono densha wa Shibuya ni ikimasu ka?", "audio_text": "この電車は渋谷に行きますか"},
        {"category": "Transport", "english": "Stop here, please", "foreign": "ここで止めてください", "romanized": "Koko de tomete kudasai", "audio_text": "ここで止めてください"},
        {"category": "Transport", "english": "How much is the subway fare?", "foreign": "地下鉄の運賃はいくらですか？", "romanized": "Chikatetsu no unchin wa ikura desu ka?", "audio_text": "運賃はいくらですか"},
        {"category": "Transport", "english": "Where is the bus stop?", "foreign": "バス停はどこですか？", "romanized": "Basutei wa doko desu ka?", "audio_text": "バス停はどこですか"},
        {"category": "Transport", "english": "How far is the airport?", "foreign": "空港までどのくらいかかりますか？", "romanized": "Kuukou made dono kurai kakarimasu ka?", "audio_text": "空港までどのくらいかかりますか"},
        {"category": "Transport", "english": "Can I charge my IC card / Suica here?", "foreign": "Suicaのチャージはできますか？", "romanized": "Suica no chaaji wa dekimasu ka?", "audio_text": "チャージはできますか"},

        # Shopping (10)
        {"category": "Shopping", "english": "How much is this?", "foreign": "これはいくらですか？", "romanized": "Kore wa ikura desu ka?", "audio_text": "これはいくらですか"},
        {"category": "Shopping", "english": "I will take this one", "foreign": "これをください", "romanized": "Kore o kudasai", "audio_text": "これをください"},
        {"category": "Shopping", "english": "Can I pay with credit card?", "foreign": "クレジットカードは使えますか？", "romanized": "Kurejitto kaado wa tsukaemasu ka?", "audio_text": "クレジットカードは使えますか"},
        {"category": "Shopping", "english": "Is this tax-free (Duty Free)?", "foreign": "免税できますか？", "romanized": "Menzei dekimasu ka?", "audio_text": "免税できますか"},
        {"category": "Shopping", "english": "Can I try this on?", "foreign": "試着してもいいですか？", "romanized": "Shichaku shitemo ii desu ka?", "audio_text": "試着してもいいですか"},
        {"category": "Shopping", "english": "Do you have a different size or color?", "foreign": "別のサイズや色はありますか？", "romanized": "Betsu no saizu ya iro wa arimasu ka?", "audio_text": "別のサイズはありますか"},
        {"category": "Shopping", "english": "Please give me a receipt", "foreign": "レシートをください", "romanized": "Reshiito o kudasai", "audio_text": "レシートをください"},
        {"category": "Shopping", "english": "Where is the souvenir section?", "foreign": "お土産コーナーはどこですか？", "romanized": "Omiyage koonaa wa doko desu ka?", "audio_text": "お土産コーナーはどこですか"},
        {"category": "Shopping", "english": "Can you wrap this as a gift?", "foreign": "プレゼント用にラッピングできますか？", "romanized": "Purezento you ni rappingu dekimasu ka?", "audio_text": "ラッピングできますか"},
        {"category": "Shopping", "english": "What time do you close?", "foreign": "何時に閉店しますか？", "romanized": "Nanji ni heiten shimasu ka?", "audio_text": "何時に閉店しますか"},

        # Emergency (10)
        {"category": "Emergency", "english": "Please help me!", "foreign": "助けてください！", "romanized": "Tasukete kudasai!", "audio_text": "助けてください"},
        {"category": "Emergency", "english": "Call the police immediately", "foreign": "警察を呼んでください", "romanized": "Keisatsu o yonde kudasai", "audio_text": "警察を呼んでください"},
        {"category": "Emergency", "english": "Please call an ambulance", "foreign": "救急車を呼んでください", "romanized": "Kyuukyuusha o yonde kudasai", "audio_text": "救急車を呼んでください"},
        {"category": "Emergency", "english": "I need a doctor / hospital", "foreign": "病院に行きたいです", "romanized": "Byouin ni ikitai desu", "audio_text": "病院に行きたいです"},
        {"category": "Emergency", "english": "I lost my passport and wallet", "foreign": "パスポートと財布をなくしました", "romanized": "Pasupooto to saifu o nakushimashita", "audio_text": "パスポートをなくしました"},
        {"category": "Emergency", "english": "I feel very sick / feverish", "foreign": "気分が悪いです", "romanized": "Kibun ga warui desu", "audio_text": "気分が悪いです"},
        {"category": "Emergency", "english": "Where is the police box (Koban)?", "foreign": "交番はどこですか？", "romanized": "Kouban wa doko desu ka?", "audio_text": "交番はどこですか"},
        {"category": "Emergency", "english": "There is a fire / accident", "foreign": "火事です / 事故です", "romanized": "Kaji desu / Jiko desu", "audio_text": "事故です"},
        {"category": "Emergency", "english": "I am lost, please guide me", "foreign": "道に迷いました", "romanized": "Michi ni mayoimashita", "audio_text": "道に迷いました"},
        {"category": "Emergency", "english": "Where is the embassy?", "foreign": "大使館はどこですか？", "romanized": "Taishikan wa doko desu ka?", "audio_text": "大使館はどこですか"},

        # Directions (10)
        {"category": "Directions", "english": "Where is the restroom / toilet?", "foreign": "お手洗いはどこですか？", "romanized": "Otearai wa doko desu ka?", "audio_text": "お手洗いはどこですか"},
        {"category": "Directions", "english": "Where is the nearest ATM or convenience store?", "foreign": "近くのコンビニやATMはどこですか？", "romanized": "Chikaku no konbini ya ATM wa doko desu ka?", "audio_text": "コンビニはどこですか"},
        {"category": "Directions", "english": "Go straight and turn left", "foreign": "まっすぐ行って、左に曲がってください", "romanized": "Massugu itte, hidari ni magatte kudasai", "audio_text": "まっすぐ行って左に曲がってください"},
        {"category": "Directions", "english": "Turn right at the traffic signal", "foreign": "信号を右に曲がってください", "romanized": "Shingou o migi ni magatte kudasai", "audio_text": "信号を右に曲がってください"},
        {"category": "Directions", "english": "Where is the nearest pharmacy?", "foreign": "薬局はどこですか？", "romanized": "Yakkyoku wa doko desu ka?", "audio_text": "薬局はどこですか"},
        {"category": "Directions", "english": "Where is the entrance / exit?", "foreign": "入口と出口はどこですか？", "romanized": "Iriguchi to deguchi wa doko desu ka?", "audio_text": "入口はどこですか"},
        {"category": "Directions", "english": "Can you show me on Google Maps?", "foreign": "マップで場所を教えてもらえますか？", "romanized": "Mappu de basho o oshiete moraemasu ka?", "audio_text": "マップで教えてもらえますか"},
        {"category": "Directions", "english": "Is it within walking distance?", "foreign": "歩いて行けますか？", "romanized": "Aruite ikemasu ka?", "audio_text": "歩いて行けますか"},
        {"category": "Directions", "english": "Where is the temple / shrine?", "foreign": "お寺や神社はどこですか？", "romanized": "Otera ya jinja wa doko desu ka?", "audio_text": "お寺はどこですか"},
        {"category": "Directions", "english": "Which way to the central avenue?", "foreign": "大通りはどちらですか？", "romanized": "Oodoori wa dochira desu ka?", "audio_text": "大通りはどちらですか"}
    ],
    "french": [
        # Greetings (10)
        {"category": "Greetings", "english": "Hello / Good day", "foreign": "Bonjour", "romanized": "Bon-ZHOOR", "audio_text": "Bonjour"},
        {"category": "Greetings", "english": "Good evening", "foreign": "Bonsoir", "romanized": "Bohn-SWAHR", "audio_text": "Bonsoir"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "Merci beaucoup", "romanized": "Mair-SEE boh-KOO", "audio_text": "Merci beaucoup"},
        {"category": "Greetings", "english": "Please", "foreign": "S'il vous plaît", "romanized": "Seel voo pleh", "audio_text": "S'il vous plaît"},
        {"category": "Greetings", "english": "You are welcome", "foreign": "De rien / Je vous en prie", "romanized": "Duh ryen", "audio_text": "De rien"},
        {"category": "Greetings", "english": "How are you?", "foreign": "Comment allez-vous ?", "romanized": "Koh-mahn tah-lay voo?", "audio_text": "Comment allez-vous"},
        {"category": "Greetings", "english": "I am fine, thank you", "foreign": "Je vais bien, merci", "romanized": "Zhuh veh byen, mair-see", "audio_text": "Je vais bien, merci"},
        {"category": "Greetings", "english": "Excuse me / Pardon", "foreign": "Excusez-moi / Pardon", "romanized": "Ex-kew-zay mwah", "audio_text": "Excusez-moi"},
        {"category": "Greetings", "english": "Nice to meet you", "foreign": "Enchanté", "romanized": "Ahn-shahn-TAY", "audio_text": "Enchanté"},
        {"category": "Greetings", "english": "Goodbye", "foreign": "Au revoir", "romanized": "Oh ruh-VWAHR", "audio_text": "Au revoir"},

        # Dining (10)
        {"category": "Dining", "english": "The menu, please", "foreign": "La carte, s'il vous plaît", "romanized": "Lah kart, seel voo pleh", "audio_text": "La carte, s'il vous plaît"},
        {"category": "Dining", "english": "The check / bill, please", "foreign": "L'addition, s'il vous plaît", "romanized": "Lah-dee-SYOHN, seel voo pleh", "audio_text": "L'addition, s'il vous plaît"},
        {"category": "Dining", "english": "A table for two, please", "foreign": "Une table pour deux, s'il vous plaît", "romanized": "Ewn tahbl poor duh", "audio_text": "Une table pour deux"},
        {"category": "Dining", "english": "A bottle of water, please", "foreign": "Une carafe d'eau, s'il vous plaît", "romanized": "Ewn kah-rahf doh", "audio_text": "Une carafe d'eau, s'il vous plaît"},
        {"category": "Dining", "english": "It is delicious!", "foreign": "C'est délicieux !", "romanized": "Say day-lee-SYUH!", "audio_text": "C'est délicieux"},
        {"category": "Dining", "english": "Do you have vegetarian dishes?", "foreign": "Avez-vous des plats végétariens ?", "romanized": "Ah-vay voo day plah vay-zhay-tah-ryen?", "audio_text": "Avez-vous des plats végétariens"},
        {"category": "Dining", "english": "What is the dish of the day?", "foreign": "Quel est le plat du jour ?", "romanized": "Kel ay luh plah dew zhoor?", "audio_text": "Quel est le plat du jour"},
        {"category": "Dining", "english": "A coffee, please", "foreign": "Un café, s'il vous plaît", "romanized": "Un kah-fay, seel voo pleh", "audio_text": "Un café, s'il vous plaît"},
        {"category": "Dining", "english": "I am allergic to gluten / nuts", "foreign": "Je suis allergique au gluten", "romanized": "Zhuh swee zah-lair-zheek oh glew-ten", "audio_text": "Je suis allergique au gluten"},
        {"category": "Dining", "english": "Is service included?", "foreign": "Le service est-il compris ?", "romanized": "Luh sair-vees ay-teel kohm-pree?", "audio_text": "Le service est-il compris"},

        # Transport (10)
        {"category": "Transport", "english": "Where is the metro / train station?", "foreign": "Où est la station de métro / la gare ?", "romanized": "Oo eh lah stah-syohn duh may-troh?", "audio_text": "Où est la gare"},
        {"category": "Transport", "english": "Where can I buy a ticket?", "foreign": "Où puis-je acheter un billet ?", "romanized": "Oo pweezh ahsh-tay un bee-yay?", "audio_text": "Où puis-je acheter un billet"},
        {"category": "Transport", "english": "To the airport, please", "foreign": "À l'aéroport, s'il vous plaît", "romanized": "Ah lah-ay-roh-por, seel voo pleh", "audio_text": "À l'aéroport, s'il vous plaît"},
        {"category": "Transport", "english": "Please stop here", "foreign": "Arrêtez-vous ici, s'il vous plaît", "romanized": "Ah-reh-tay voo zee-see", "audio_text": "Arrêtez-vous ici"},
        {"category": "Transport", "english": "Does this bus go to the center?", "foreign": "Ce bus va-t-il au centre-ville ?", "romanized": "Suh bews vah-teel oh sahn-truh veel?", "audio_text": "Ce bus va-t-il au centre-ville"},
        {"category": "Transport", "english": "Which train platform for Lyon / Nice?", "foreign": "Quel est le quai pour Nice ?", "romanized": "Kel ay luh kay poor Nice?", "audio_text": "Quel est le quai"},
        {"category": "Transport", "english": "How much is the taxi fare?", "foreign": "Combien coûte la course ?", "romanized": "Kohm-byen koot lah koors?", "audio_text": "Combien coûte la course"},
        {"category": "Transport", "english": "Is this seat free / taken?", "foreign": "Cette place est-elle libre ?", "romanized": "Set plahs ay-tel lee-bruh?", "audio_text": "Cette place est-elle libre"},
        {"category": "Transport", "english": "What time is the next departure?", "foreign": "À quelle heure est le prochain départ ?", "romanized": "Ah kel ur ay luh proh-shen day-par?", "audio_text": "Quel est le prochain départ"},
        {"category": "Transport", "english": "Can you call a taxi for me?", "foreign": "Pouvez-vous m'appeler un taxi ?", "romanized": "Poo-vay voo mah-play un tahk-see?", "audio_text": "Pouvez-vous m'appeler un taxi"},

        # Shopping (10)
        {"category": "Shopping", "english": "How much does this cost?", "foreign": "Combien ça coûte ?", "romanized": "Kohm-byen sah koot?", "audio_text": "Combien ça coûte"},
        {"category": "Shopping", "english": "Can I pay by credit card?", "foreign": "Puis-je payer par carte bancaire ?", "romanized": "Pweezh pay-yay par kart bahn-kair?", "audio_text": "Puis-je payer par carte"},
        {"category": "Shopping", "english": "I will take this one", "foreign": "Je vais prendre celui-ci", "romanized": "Zhuh veh prahn-druh suh-lwee-see", "audio_text": "Je vais prendre celui-ci"},
        {"category": "Shopping", "english": "Can I try this on?", "foreign": "Puis-je l'essayer ?", "romanized": "Pweezh lay-say-yay?", "audio_text": "Puis-je l'essayer"},
        {"category": "Shopping", "english": "Do you have another size or color?", "foreign": "Avez-vous une autre taille ou couleur ?", "romanized": "Ah-vay voo ewn ohtruh tye oo koo-lur?", "audio_text": "Avez-vous une autre taille"},
        {"category": "Shopping", "english": "It is too expensive", "foreign": "C'est trop cher", "romanized": "Say troh shair", "audio_text": "C'est trop cher"},
        {"category": "Shopping", "english": "Can I get a tax-free receipt (Détaxe)?", "foreign": "Faites-vous la détaxe ?", "romanized": "Fet voo lah day-taks?", "audio_text": "Faites-vous la détaxe"},
        {"category": "Shopping", "english": "Please give me the receipt", "foreign": "Le ticket de caisse, s'il vous plaît", "romanized": "Luh tee-kay duh kes", "audio_text": "Le ticket de caisse"},
        {"category": "Shopping", "english": "Can you gift wrap this?", "foreign": "Pouvez-vous faire un paquet cadeau ?", "romanized": "Poo-vay voo fair un pah-kay kah-doh?", "audio_text": "Pouvez-vous faire un paquet cadeau"},
        {"category": "Shopping", "english": "What time do the boutiques close?", "foreign": "À quelle heure ferment les magasins ?", "romanized": "Ah kel ur fairm lay mah-gah-zan?", "audio_text": "À quelle heure ferment les magasins"},

        # Emergency (10)
        {"category": "Emergency", "english": "Help!", "foreign": "Au secours !", "romanized": "Oh suh-KOOR!", "audio_text": "Au secours"},
        {"category": "Emergency", "english": "Call the police immediately", "foreign": "Appelez la police immédiatement", "romanized": "Ah-play lah poh-lees", "audio_text": "Appelez la police"},
        {"category": "Emergency", "english": "Call an ambulance (SAMU)", "foreign": "Appelez une ambulance", "romanized": "Ah-play zewn ahm-bew-lahns", "audio_text": "Appelez une ambulance"},
        {"category": "Emergency", "english": "I need a doctor / hospital", "foreign": "J'ai besoin d'un médecin", "romanized": "Zhay buh-zwan dun mayd-san", "audio_text": "J'ai besoin d'un médecin"},
        {"category": "Emergency", "english": "I lost my passport and wallet", "foreign": "J'ai perdu mon passeport et mon portefeuille", "romanized": "Zhay pair-dew mohn pahs-por", "audio_text": "J'ai perdu mon passeport"},
        {"category": "Emergency", "english": "I feel very sick", "foreign": "Je me sens très malade", "romanized": "Zhuh muh sahn treh mah-lahd", "audio_text": "Je me sens très malade"},
        {"category": "Emergency", "english": "There has been an accident", "foreign": "Il y a eu un accident", "romanized": "Eel ee ah ew un ahk-see-dahn", "audio_text": "Il y a eu un accident"},
        {"category": "Emergency", "english": "Where is the police station (Commissariat)?", "foreign": "Où est le commissariat de police ?", "romanized": "Oo eh luh koh-mee-sah-ryah?", "audio_text": "Où est le commissariat"},
        {"category": "Emergency", "english": "Where is my embassy?", "foreign": "Où est l'ambassade ?", "romanized": "Oo eh lahm-bah-sahd?", "audio_text": "Où est l'ambassade"},
        {"category": "Emergency", "english": "I am lost, can you help me?", "foreign": "Je suis perdu, pouvez-vous m'aider ?", "romanized": "Zhuh swee pair-dew, poo-vay voo may-day?", "audio_text": "Je suis perdu, pouvez-vous m'aider"},

        # Directions (10)
        {"category": "Directions", "english": "Where are the restrooms / toilets?", "foreign": "Où sont les toilettes, s'il vous plaît ?", "romanized": "Oo sohn lay twah-let?", "audio_text": "Où sont les toilettes"},
        {"category": "Directions", "english": "Where is the nearest pharmacy / ATM?", "foreign": "Où est la pharmacie / le distributeur ?", "romanized": "Oo eh lah far-mah-see?", "audio_text": "Où est la pharmacie"},
        {"category": "Directions", "english": "Go straight ahead", "foreign": "Allez tout droit", "romanized": "Ah-lay too drwah", "audio_text": "Allez tout droit"},
        {"category": "Directions", "english": "Turn left / Turn right", "foreign": "Tournez à gauche / Tournez à droite", "romanized": "Toor-nay ah gohsh / ah drwaht", "audio_text": "Tournez à gauche"},
        {"category": "Directions", "english": "Where is the Eiffel Tower / Museum?", "foreign": "Où est la Tour Eiffel / le musée ?", "romanized": "Oo eh lah toor ay-fel?", "audio_text": "Où est le musée"},
        {"category": "Directions", "english": "Is it far on foot?", "foreign": "Est-ce loin à pied ?", "romanized": "Es lwan ah pyay?", "audio_text": "Est-ce loin à pied"},
        {"category": "Directions", "english": "Where is the entrance / exit?", "foreign": "Où est l'entrée / la sortie ?", "romanized": "Oo eh lahn-tray / lah sor-tee?", "audio_text": "Où est l'entrée"},
        {"category": "Directions", "english": "Can you show me on the map?", "foreign": "Pouvez-vous me montrer sur le plan ?", "romanized": "Poo-vay voo muh mohn-tray soor luh plahn?", "audio_text": "Montrez-moi sur le plan"},
        {"category": "Directions", "english": "Which way to the Champs-Élysées?", "foreign": "Par où va-t-on aux Champs-Élysées ?", "romanized": "Par oo vah-tohn oh shahn-zay-lee-zay?", "audio_text": "Par où va-t-on"},
        {"category": "Directions", "english": "Is this the right way to the cathedral?", "foreign": "Est-ce le bon chemin pour la cathédrale ?", "romanized": "Es luh bohn shuh-man poor lah kah-tay-drahl?", "audio_text": "Est-ce le bon chemin"}
    ],
    "spanish": [
        # Greetings (10)
        {"category": "Greetings", "english": "Hello / Good day", "foreign": "¡Hola! Buenos días", "romanized": "OH-lah! BWEH-nohs DEE-ahs", "audio_text": "Hola! Buenos días"},
        {"category": "Greetings", "english": "Good evening", "foreign": "Buenas noches", "romanized": "BWEH-nahs NOH-ches", "audio_text": "Buenas noches"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "Muchas gracias", "romanized": "MOO-chahs GRAH-syahs", "audio_text": "Muchas gracias"},
        {"category": "Greetings", "english": "You are welcome", "foreign": "De nada", "romanized": "Deh NAH-dah", "audio_text": "De nada"},
        {"category": "Greetings", "english": "Please", "foreign": "Por favor", "romanized": "Por fah-VOR", "audio_text": "Por favor"},
        {"category": "Greetings", "english": "How are you?", "foreign": "¿Cómo está usted?", "romanized": "KOH-moh ehs-TAH oos-TED?", "audio_text": "Cómo está usted"},
        {"category": "Greetings", "english": "I am fine, thank you", "foreign": "Muy bien, gracias", "romanized": "Mwee byen, GRAH-syahs", "audio_text": "Muy bien, gracias"},
        {"category": "Greetings", "english": "Excuse me / Pardon", "foreign": "Disculpe / Con permiso", "romanized": "Dees-KOOL-peh", "audio_text": "Disculpe"},
        {"category": "Greetings", "english": "Nice to meet you", "foreign": "Mucho gusto", "romanized": "MOO-choh GOOS-toh", "audio_text": "Mucho gusto"},
        {"category": "Greetings", "english": "Goodbye", "foreign": "Adiós / Hasta luego", "romanized": "Ah-DYOHS / AHS-tah LWEH-goh", "audio_text": "Adiós"},

        # Dining (10)
        {"category": "Dining", "english": "The bill, please", "foreign": "La cuenta, por favor", "romanized": "Lah KWEN-tah, por fah-VOR", "audio_text": "La cuenta, por favor"},
        {"category": "Dining", "english": "A table for two, please", "foreign": "Una mesa para dos, por favor", "romanized": "OO-nah MEH-sah PAH-rah dohs", "audio_text": "Una mesa para dos"},
        {"category": "Dining", "english": "The menu, please", "foreign": "El menú / la carta, por favor", "romanized": "El meh-NOO, por fah-VOR", "audio_text": "La carta, por favor"},
        {"category": "Dining", "english": "It is delicious!", "foreign": "¡Está delicioso!", "romanized": "Ehs-TAH deh-lee-SYOH-soh!", "audio_text": "Está delicioso"},
        {"category": "Dining", "english": "Do you have vegetarian food?", "foreign": "¿Tiene comida vegetariana?", "romanized": "TYEH-neh koh-MEE-dah veh-heh-tah-RYAH-nah?", "audio_text": "Tiene comida vegetariana"},
        {"category": "Dining", "english": "A bottle of water, please", "foreign": "Una botella de agua, por favor", "romanized": "OO-nah boh-TEH-yah deh AH-gwah", "audio_text": "Una botella de agua"},
        {"category": "Dining", "english": "What is the house specialty / tapas?", "foreign": "¿Cuál es la especialidad de la casa?", "romanized": "KWAHL es lah es-peh-syah-lee-DAHD?", "audio_text": "Cuál es la especialidad"},
        {"category": "Dining", "english": "A coffee with milk, please", "foreign": "Un café con leche, por favor", "romanized": "Oon kah-FAY kohn LEH-cheh", "audio_text": "Un café con leche"},
        {"category": "Dining", "english": "I am allergic to nuts / gluten", "foreign": "Soy alérgico a los frutos secos", "romanized": "Soy ah-LAIR-hee-koh ah lohs FROO-tohs SEH-kohs", "audio_text": "Soy alérgico a los frutos secos"},
        {"category": "Dining", "english": "Is service / tip included?", "foreign": "¿El servicio está incluido?", "romanized": "El sair-VEE-syoh ehs-TAH een-kloo-EE-doh?", "audio_text": "El servicio está incluido"},

        # Transport (10)
        {"category": "Transport", "english": "Where is the train / metro station?", "foreign": "¿Dónde está la estación de tren / metro?", "romanized": "DOHN-deh ehs-TAH lah ehs-tah-SYOHN?", "audio_text": "Dónde está la estación"},
        {"category": "Transport", "english": "To the airport, please", "foreign": "Al aeropuerto, por favor", "romanized": "Ahl ah-ay-roh-PWER-toh, por fah-VOR", "audio_text": "Al aeropuerto, por favor"},
        {"category": "Transport", "english": "Please stop here", "foreign": "Pare aquí, por favor", "romanized": "PAH-reh ah-KEE, por fah-VOR", "audio_text": "Pare aquí, por favor"},
        {"category": "Transport", "english": "Where can I buy a ticket?", "foreign": "¿Dónde puedo comprar un billete?", "romanized": "DOHN-deh PWEH-doh kohm-PRAR oon bee-YEH-teh?", "audio_text": "Dónde puedo comprar un billete"},
        {"category": "Transport", "english": "Does this bus go to downtown / Plaza Mayor?", "foreign": "¿Este autobús va al centro?", "romanized": "EHS-teh ow-toh-BOOS vah ahl SEN-troh?", "audio_text": "Este autobús va al centro"},
        {"category": "Transport", "english": "How much is the taxi fare?", "foreign": "¿Cuánto cuesta el taxi?", "romanized": "KWAHN-toh KWEHS-tah el TAHK-see?", "audio_text": "Cuánto cuesta el taxi"},
        {"category": "Transport", "english": "What time is the next departure?", "foreign": "¿A qué hora sale el próximo tren?", "romanized": "Ah kay OH-rah SAH-leh el PROHK-see-moh tren?", "audio_text": "A qué hora sale el tren"},
        {"category": "Transport", "english": "Which platform does the train leave from?", "foreign": "¿De qué andén sale el tren?", "romanized": "Deh kay ahn-DEN SAH-leh el tren?", "audio_text": "De qué andén sale"},
        {"category": "Transport", "english": "Can you call a taxi for me?", "foreign": "¿Puede llamar a un taxi para mí?", "romanized": "PWEH-deh yah-MAR ah oon TAHK-see PAH-rah mee?", "audio_text": "Puede llamar a un taxi"},
        {"category": "Transport", "english": "Where is the bus stop?", "foreign": "¿Dónde está la parada de autobús?", "romanized": "DOHN-deh ehs-TAH lah pah-RAH-dah?", "audio_text": "Dónde está la parada"},

        # Shopping (10)
        {"category": "Shopping", "english": "How much does this cost?", "foreign": "¿Cuánto cuesta esto?", "romanized": "KWAHN-toh KWEHS-tah EHS-toh?", "audio_text": "Cuánto cuesta esto"},
        {"category": "Shopping", "english": "Can I pay with credit card?", "foreign": "¿Puedo pagar con tarjeta?", "romanized": "PWEH-doh pah-GAR kohn tar-HEH-tah?", "audio_text": "Puedo pagar con tarjeta"},
        {"category": "Shopping", "english": "I will buy this one", "foreign": "Me llevo esto", "romanized": "Meh YEH-voh EHS-toh", "audio_text": "Me llevo esto"},
        {"category": "Shopping", "english": "Can I try this on?", "foreign": "¿Me lo puedo probar?", "romanized": "Meh loh PWEH-doh proh-BAR?", "audio_text": "Me lo puedo probar"},
        {"category": "Shopping", "english": "Do you have another size or color?", "foreign": "¿Tiene otra talla o color?", "romanized": "TYEH-neh OH-trah TAH-yah oh koh-LOR?", "audio_text": "Tiene otra talla"},
        {"category": "Shopping", "english": "Can you give a discount?", "foreign": "¿Me puede hacer un descuento?", "romanized": "Meh PWEH-deh ah-SAIR oon dehs-KWEN-toh?", "audio_text": "Me puede hacer un descuento"},
        {"category": "Shopping", "english": "It is too expensive", "foreign": "Es demasiado caro", "romanized": "Es deh-mah-SYAH-doh KAH-roh", "audio_text": "Es demasiado caro"},
        {"category": "Shopping", "english": "Please give me the receipt / invoice", "foreign": "El recibo / la factura, por favor", "romanized": "El reh-SEE-boh, por fah-VOR", "audio_text": "El recibo, por favor"},
        {"category": "Shopping", "english": "Can you gift wrap it?", "foreign": "¿Puede envolverlo para regalo?", "romanized": "PWEH-deh en-vohl-VAIR-loh PAH-rah reh-GAH-loh?", "audio_text": "Puede envolverlo para regalo"},
        {"category": "Shopping", "english": "What time does the store close?", "foreign": "¿A qué hora cierran?", "romanized": "Ah kay OH-rah SYEH-rahn?", "audio_text": "A qué hora cierran"},

        # Emergency (10)
        {"category": "Emergency", "english": "Help me, please!", "foreign": "¡Ayúdeme, por favor!", "romanized": "ah-YOO-deh-meh, por fah-VOR!", "audio_text": "Ayúdeme, por favor"},
        {"category": "Emergency", "english": "Call the police immediately", "foreign": "Llame a la policía inmediatamente", "romanized": "YAH-meh ah lah poh-lee-SEE-ah", "audio_text": "Llame a la policía"},
        {"category": "Emergency", "english": "Call an ambulance", "foreign": "Llame a una ambulancia", "romanized": "YAH-meh ah OO-nah ahm-boo-LAHN-syah", "audio_text": "Llame a una ambulancia"},
        {"category": "Emergency", "english": "I need a doctor / hospital", "foreign": "Necesito un médico / hospital", "romanized": "Neh-seh-SEE-toh oon MEH-dee-koh", "audio_text": "Necesito un médico"},
        {"category": "Emergency", "english": "I lost my passport and wallet", "foreign": "He perdido mi pasaporte y mi cartera", "romanized": "Eh pair-DEE-doh mee pah-sah-POR-teh", "audio_text": "He perdido mi pasaporte"},
        {"category": "Emergency", "english": "I feel very sick / dizzy", "foreign": "Me siento muy mal", "romanized": "Meh SYEN-toh mwee mahl", "audio_text": "Me siento muy mal"},
        {"category": "Emergency", "english": "There has been an accident", "foreign": "Ha habido un accidente", "romanized": "Ah ah-BEE-doh oon ahk-see-DEN-teh", "audio_text": "Ha habido un accidente"},
        {"category": "Emergency", "english": "Where is the police station?", "foreign": "¿Dónde está la comisaría de policía?", "romanized": "DOHN-deh ehs-TAH lah koh-mee-sah-REE-ah?", "audio_text": "Dónde está la comisaría"},
        {"category": "Emergency", "english": "Where is the embassy / consulate?", "foreign": "¿Dónde está la embajada?", "romanized": "DOHN-deh ehs-TAH lah em-bah-HAH-dah?", "audio_text": "Dónde está la embajada"},
        {"category": "Emergency", "english": "I am lost, can you help me?", "foreign": "Estoy perdido, ¿me puede ayudar?", "romanized": "Ehs-TOY pair-DEE-doh, meh PWEH-deh ah-yoo-DAR?", "audio_text": "Estoy perdido, puede ayudarme"},

        # Directions (10)
        {"category": "Directions", "english": "Where are the restrooms / toilets?", "foreign": "¿Dónde están los baños / servicios?", "romanized": "DOHN-deh ehs-TAHN lohs BAH-nyohs?", "audio_text": "Dónde están los baños"},
        {"category": "Directions", "english": "Where is the nearest pharmacy / ATM?", "foreign": "¿Dónde hay una farmacia o cajero automático?", "romanized": "DOHN-deh eye OO-nah far-MAH-syah?", "audio_text": "Dónde hay una farmacia"},
        {"category": "Directions", "english": "Go straight ahead", "foreign": "Siga todo recto", "romanized": "SEE-gah TOH-doh REHK-toh", "audio_text": "Siga todo recto"},
        {"category": "Directions", "english": "Turn left / Turn right", "foreign": "Gire a la izquierda / Gire a la derecha", "romanized": "HEE-reh ah lah ees-KYAIR-dah / deh-REH-chah", "audio_text": "Gire a la izquierda"},
        {"category": "Directions", "english": "How far is the beach / museum on foot?", "foreign": "¿Está lejos caminando?", "romanized": "Ehs-TAH LEH-hohs kah-mee-NAHN-doh?", "audio_text": "Está lejos caminando"},
        {"category": "Directions", "english": "Where is the main entrance / exit?", "foreign": "¿Dónde está la entrada / salida?", "romanized": "DOHN-deh ehs-TAH lah en-TRAH-dah / sah-LEE-dah?", "audio_text": "Dónde está la entrada"},
        {"category": "Directions", "english": "Can you show me the way on the map?", "foreign": "¿Me puede indicar en el mapa?", "romanized": "Meh PWEH-deh een-dee-KAR en el MAH-pah?", "audio_text": "Indíqueme en el mapa"},
        {"category": "Directions", "english": "Is this the correct way to the Cathedral?", "foreign": "¿Es este el camino correcto hacia la catedral?", "romanized": "Es EHS-teh el kah-MEE-noh koh-REHK-toh?", "audio_text": "Es este el camino correcto"},
        {"category": "Directions", "english": "Where is the city center / main square?", "foreign": "¿Dónde está el centro histórico / plaza mayor?", "romanized": "DOHN-deh ehs-TAH el SEN-troh?", "audio_text": "Dónde está el centro"},
        {"category": "Directions", "english": "Which bus goes to the beach?", "foreign": "¿Qué autobús va a la playa?", "romanized": "Kay ow-toh-BOOS vah ah lah PLAH-yah?", "audio_text": "Qué autobús va a la playa"}
    ],
    "italian": [
        # Greetings (10)
        {"category": "Greetings", "english": "Good morning / Hello", "foreign": "Buongiorno", "romanized": "Bwon-JOR-noh", "audio_text": "Buongiorno"},
        {"category": "Greetings", "english": "Good evening", "foreign": "Buonasera", "romanized": "Bwoh-nah-SEH-rah", "audio_text": "Buonasera"},
        {"category": "Greetings", "english": "Thank you so much", "foreign": "Grazie mille", "romanized": "GRAHT-syeh MEE-leh", "audio_text": "Grazie mille"},
        {"category": "Greetings", "english": "You are welcome", "foreign": "Prego", "romanized": "PRAY-goh", "audio_text": "Prego"},
        {"category": "Greetings", "english": "Please", "foreign": "Per favore / Per piacere", "romanized": "Pair fah-VOH-reh", "audio_text": "Per favore"},
        {"category": "Greetings", "english": "How are you?", "foreign": "Come sta?", "romanized": "KOH-meh stah?", "audio_text": "Come sta"},
        {"category": "Greetings", "english": "I am fine, thank you", "foreign": "Sto bene, grazie", "romanized": "Stoh BEH-neh, GRAHT-syeh", "audio_text": "Sto bene, grazie"},
        {"category": "Greetings", "english": "Excuse me / Pardon", "foreign": "Scusi / Permesso", "romanized": "SKOO-zee", "audio_text": "Scusi"},
        {"category": "Greetings", "english": "Nice to meet you", "foreign": "Piacere di conoscerla", "romanized": "Pyah-CHEH-reh dee koh-NOH-shair-lah", "audio_text": "Piacere"},
        {"category": "Greetings", "english": "Goodbye", "foreign": "Arrivederci / Ciao", "romanized": "Ah-ree-veh-DAIR-chee", "audio_text": "Arrivederci"},

        # Dining (10)
        {"category": "Dining", "english": "A table for two, please", "foreign": "Un tavolo per due, per favore", "romanized": "Oon TAH-voh-loh pair DOO-eh, pair fah-VOH-reh", "audio_text": "Un tavolo per due, per favore"},
        {"category": "Dining", "english": "The bill, please", "foreign": "Il conto, per favore", "romanized": "Eel KOHN-toh, pair fah-VOH-reh", "audio_text": "Il conto, per favore"},
        {"category": "Dining", "english": "The menu, please", "foreign": "Il menu, per favore", "romanized": "Eel meh-NOO, pair fah-VOH-reh", "audio_text": "Il menu, per favore"},
        {"category": "Dining", "english": "It is delicious!", "foreign": "È delizioso / buonissimo!", "romanized": "Eh deh-lee-TSYOH-zoh / bwon-EES-see-moh!", "audio_text": "È buonissimo"},
        {"category": "Dining", "english": "Do you have vegetarian dishes?", "foreign": "Avete piatti vegetariani?", "romanized": "Ah-VEH-teh PYAH-tee veh-zheh-tah-RYAH-nee?", "audio_text": "Avete piatti vegetariani"},
        {"category": "Dining", "english": "A bottle of mineral water, please", "foreign": "Una bottiglia d'acqua naturale, per favore", "romanized": "OO-nah boh-TEEL-yah DAHK-wah nah-too-RAH-leh", "audio_text": "Una bottiglia d'acqua"},
        {"category": "Dining", "english": "What is the chef recommendation?", "foreign": "Cosa consiglia lo chef?", "romanized": "KOH-zah kohn-SEEL-yah loh shef?", "audio_text": "Cosa consiglia lo chef"},
        {"category": "Dining", "english": "An espresso coffee, please", "foreign": "Un caffè espresso, per favore", "romanized": "Oon kahf-FEH es-PRES-soh", "audio_text": "Un caffè, per favore"},
        {"category": "Dining", "english": "I am allergic to gluten / cheese", "foreign": "Sono allergico al glutine / latticini", "romanized": "SOH-noh ahl-LAIR-zhee-koh ahl GLOO-tee-neh", "audio_text": "Sono allergico al glutine"},
        {"category": "Dining", "english": "Is service included (coperto)?", "foreign": "Il coperto è incluso?", "romanized": "Eel koh-PAIR-toh eh een-KLOO-zoh?", "audio_text": "Il coperto è incluso"},

        # Transport (10)
        {"category": "Transport", "english": "Where is the railway station?", "foreign": "Dov'è la stazione ferroviaria?", "romanized": "Doh-VEH lah stah-TSYOH-neh fair-roh-VYAH-ryah?", "audio_text": "Dov'è la stazione"},
        {"category": "Transport", "english": "To the airport / Roma Termini, please", "foreign": "All'aeroporto, per favore", "romanized": "Ahl-ah-eh-roh-POR-toh, pair fah-VOH-reh", "audio_text": "All'aeroporto, per favore"},
        {"category": "Transport", "english": "Please stop here", "foreign": "Si fermi qui, per favore", "romanized": "See FAIR-mee kwee, pair fah-VOH-reh", "audio_text": "Si fermi qui"},
        {"category": "Transport", "english": "Where can I buy a train / metro ticket?", "foreign": "Dove posso comprare un biglietto?", "romanized": "DOH-veh POHS-soh kohm-PRAH-reh oon beel-YEHT-toh?", "audio_text": "Dove posso comprare un biglietto"},
        {"category": "Transport", "english": "Does this bus go to the Colosseum?", "foreign": "Questo autobus va al Colosseo?", "romanized": "KWEHS-toh OW-toh-boos vah ahl Koh-lohs-SEH-oh?", "audio_text": "Questo autobus va al Colosseo"},
        {"category": "Transport", "english": "How much is the taxi ride?", "foreign": "Quanto costa la corsa in taxi?", "romanized": "KWAHN-toh KOHS-tah lah KOR-sah een TAHK-see?", "audio_text": "Quanto costa il taxi"},
        {"category": "Transport", "english": "Which platform for the Frecciarossa train?", "foreign": "Da quale binario parte il treno?", "romanized": "Dah KWAH-leh bee-NAH-ryoh PAHR-teh eel TREH-noh?", "audio_text": "Da quale binario parte"},
        {"category": "Transport", "english": "What time is the next departure?", "foreign": "A che ora è la prossima partenza?", "romanized": "Ah kay OH-rah eh lah PROHS-see-mah pahr-TEN-tsah?", "audio_text": "A che ora è la partenza"},
        {"category": "Transport", "english": "Can you call a taxi for me?", "foreign": "Può chiamarmi un taxi?", "romanized": "Pwoh kyah-MAHR-mee oon TAHK-see?", "audio_text": "Può chiamarmi un taxi"},
        {"category": "Transport", "english": "Where is the bus stop?", "foreign": "Dov'è la fermata dell'autobus?", "romanized": "Doh-VEH lah fair-MAH-tah dehl-OW-toh-boos?", "audio_text": "Dov'è la fermata dell'autobus"},

        # Shopping (10)
        {"category": "Shopping", "english": "How much is this?", "foreign": "Quanto costa questo?", "romanized": "KWAHN-toh KOHS-tah KWEHS-toh?", "audio_text": "Quanto costa questo"},
        {"category": "Shopping", "english": "Can I pay by credit card?", "foreign": "Posso pagare con la carta di credito?", "romanized": "POHS-soh pah-GAH-reh kohn lah KAHR-tah?", "audio_text": "Posso pagare con la carta"},
        {"category": "Shopping", "english": "I will buy this one", "foreign": "Prendo questo", "romanized": "PREHN-doh KWEHS-toh", "audio_text": "Prendo questo"},
        {"category": "Shopping", "english": "Can I try this on?", "foreign": "Posso provarlo?", "romanized": "POHS-soh proh-VAHR-loh?", "audio_text": "Posso provarlo"},
        {"category": "Shopping", "english": "Do you have another size or color?", "foreign": "Avete un'altra taglia o colore?", "romanized": "Ah-VEH-teh oon-AHL-trah TAHL-yah oh koh-LOH-reh?", "audio_text": "Avete un'altra taglia"},
        {"category": "Shopping", "english": "Can you give a discount (sconto)?", "foreign": "È possibile avere uno sconto?", "romanized": "Eh pohs-SEE-bee-leh ah-VEH-reh OO-noh SKOHN-toh?", "audio_text": "È possibile uno sconto"},
        {"category": "Shopping", "english": "It is too expensive", "foreign": "È troppo caro", "romanized": "Eh TROHP-poh KAH-roh", "audio_text": "È troppo caro"},
        {"category": "Shopping", "english": "Please give me the receipt (scontrino)", "foreign": "Lo scontrino, per favore", "romanized": "Loh skohn-TREE-noh, pair fah-VOH-reh", "audio_text": "Lo scontrino, per favore"},
        {"category": "Shopping", "english": "Can you wrap it as a gift package?", "foreign": "Può fare una confezione regalo?", "romanized": "Pwoh FAH-reh OO-nah kohn-feh-TSYOH-neh reh-GAH-loh?", "audio_text": "Può fare una confezione regalo"},
        {"category": "Shopping", "english": "What time do the stores close?", "foreign": "A che ora chiudono i negozi?", "romanized": "Ah kay OH-rah KYOO-doh-noh ee neh-GOHT-see?", "audio_text": "A che ora chiudono i negozi"},

        # Emergency (10)
        {"category": "Emergency", "english": "I need a doctor immediately", "foreign": "Ho bisogno di un medico", "romanized": "Oh bee-ZOHN-yoh dee oon MEH-dee-koh", "audio_text": "Ho bisogno di un medico"},
        {"category": "Emergency", "english": "Call the police (Carabinieri) now", "foreign": "Chiamate la polizia / i carabinieri", "romanized": "Kyah-MAH-teh lah poh-lee-TSEE-ah", "audio_text": "Chiamate la polizia"},
        {"category": "Emergency", "english": "Call an ambulance (118)", "foreign": "Chiamate un'ambulanza", "romanized": "Kyah-MAH-teh oon-ahm-boo-LAHN-tsah", "audio_text": "Chiamate un'ambulanza"},
        {"category": "Emergency", "english": "Help me, please!", "foreign": "Aiuto, per favore!", "romanized": "Ah-YOO-toh, pair fah-VOH-reh!", "audio_text": "Aiuto, per favore"},
        {"category": "Emergency", "english": "I lost my passport and wallet", "foreign": "Ho perso il passaporto e il portafoglio", "romanized": "Oh PAIR-soh eel pahs-sah-POR-toh", "audio_text": "Ho perso il passaporto"},
        {"category": "Emergency", "english": "I feel very sick / dizzy", "foreign": "Mi sento molto male", "romanized": "Mee SEHN-toh MOHL-toh MAH-leh", "audio_text": "Mi sento molto male"},
        {"category": "Emergency", "english": "There has been an accident", "foreign": "C'è stato un incidente", "romanized": "Cheh STAH-toh oon een-chee-DEN-teh", "audio_text": "C'è stato un incidente"},
        {"category": "Emergency", "english": "Where is the nearest hospital / ER (Pronto Soccorso)?", "foreign": "Dov'è il pronto soccorso?", "romanized": "Doh-VEH eel PROHN-toh sohk-KOR-soh?", "audio_text": "Dov'è il pronto soccorso"},
        {"category": "Emergency", "english": "Where is the embassy / consulate?", "foreign": "Dov'è l'ambasciata?", "romanized": "Doh-VEH lahm-bah-SHAH-tah?", "audio_text": "Dov'è l'ambasciata"},
        {"category": "Emergency", "english": "I am lost, can you help me?", "foreign": "Mi sono perso, mi può aiutare?", "romanized": "Mee SOH-noh PAIR-soh, mee pwoh ah-yoo-TAH-reh?", "audio_text": "Mi sono perso, mi può aiutare"},

        # Directions (10)
        {"category": "Directions", "english": "Where is the restroom / toilet?", "foreign": "Dov'è il bagno / la toilette?", "romanized": "Doh-VEH eel BAHN-yoh?", "audio_text": "Dov'è il bagno"},
        {"category": "Directions", "english": "Where is the nearest pharmacy / ATM (Bancomat)?", "foreign": "Dov'è la farmacia o il bancomat più vicino?", "romanized": "Doh-VEH lah far-mah-CHEE-ah oh eel BAHN-koh-maht?", "audio_text": "Dov'è la farmacia"},
        {"category": "Directions", "english": "Go straight ahead", "foreign": "Vada sempre dritto", "romanized": "VAH-dah SEM-preh DREET-toh", "audio_text": "Vada sempre dritto"},
        {"category": "Directions", "english": "Turn left / Turn right", "foreign": "Giri a sinistra / Giri a destra", "romanized": "JEE-ree ah see-NEES-trah / ah DEHS-trah", "audio_text": "Giri a sinistra"},
        {"category": "Directions", "english": "Where is the Duomo / Historic Center?", "foreign": "Dov'è il Duomo / il centro storico?", "romanized": "Doh-VEH eel DWO-moh eel CHEN-troh?", "audio_text": "Dov'è il Duomo"},
        {"category": "Directions", "english": "Is it far on foot?", "foreign": "È lontano a piedi?", "romanized": "Eh lohn-TAH-noh ah PYEH-dee?", "audio_text": "È lontano a piedi"},
        {"category": "Directions", "english": "Where is the entrance / exit?", "foreign": "Dov'è l'entrata / l'uscita?", "romanized": "Doh-VEH len-TRAH-tah / loosh-CHEE-tah?", "audio_text": "Dov'è l'entrata"},
        {"category": "Directions", "english": "Can you show me on Google Maps?", "foreign": "Me lo può indicare sulla mappa?", "romanized": "Meh loh pwoh een-dee-KAH-reh SOOL-lah MAHP-pah?", "audio_text": "Me lo indichi sulla mappa"},
        {"category": "Directions", "english": "Which way to the main square (Piazza)?", "foreign": "Da che parte è la piazza principale?", "romanized": "Dah kay PAHR-teh eh lah PYAHT-tsah?", "audio_text": "Da che parte è la piazza"},
        {"category": "Directions", "english": "Is this the right street?", "foreign": "È questa la strada giusta?", "romanized": "Eh KWEHS-tah lah STRAH-dah JOOS-tah?", "audio_text": "È questa la strada giusta"}
    ],
    "german": [
        # Greetings (10)
        {"category": "Greetings", "english": "Hello / Good day", "foreign": "Guten Tag", "romanized": "GOO-ten tahk", "audio_text": "Guten Tag"},
        {"category": "Greetings", "english": "Good morning", "foreign": "Guten Morgen", "romanized": "GOO-ten MOR-gen", "audio_text": "Guten Morgen"},
        {"category": "Greetings", "english": "Good evening", "foreign": "Guten Abend", "romanized": "GOO-ten AH-bent", "audio_text": "Guten Abend"},
        {"category": "Greetings", "english": "Thank you very much", "foreign": "Vielen Dank", "romanized": "FEE-len dahnk", "audio_text": "Vielen Dank"},
        {"category": "Greetings", "english": "You are welcome", "foreign": "Bitte schön / Gern geschehen", "romanized": "BIH-tuh shurn", "audio_text": "Bitte schön"},
        {"category": "Greetings", "english": "Please", "foreign": "Bitte", "romanized": "BIH-tuh", "audio_text": "Bitte"},
        {"category": "Greetings", "english": "How are you?", "foreign": "Wie geht es Ihnen?", "romanized": "Vee gayt es EE-nen?", "audio_text": "Wie geht es Ihnen"},
        {"category": "Greetings", "english": "I am fine, thank you", "foreign": "Mir geht es gut, danke", "romanized": "Meer gayt es goot, DAHN-kuh", "audio_text": "Mir geht es gut, danke"},
        {"category": "Greetings", "english": "Excuse me / Pardon", "foreign": "Entschuldigung", "romanized": "Ent-SHOOL-dee-goong", "audio_text": "Entschuldigung"},
        {"category": "Greetings", "english": "Goodbye", "foreign": "Auf Wiedersehen / Tschüss", "romanized": "Owf VEE-der-zay-en", "audio_text": "Auf Wiedersehen"},

        # Dining (10)
        {"category": "Dining", "english": "The bill, please", "foreign": "Die Rechnung, bitte", "romanized": "Dee REKH-noong, BIH-tuh", "audio_text": "Die Rechnung, bitte"},
        {"category": "Dining", "english": "A table for two, please", "foreign": "Einen Tisch für zwei Personen, bitte", "romanized": "EYE-nen tish feer tsvye, BIH-tuh", "audio_text": "Einen Tisch für zwei, bitte"},
        {"category": "Dining", "english": "The menu, please", "foreign": "Die Speisekarte, bitte", "romanized": "Dee SHPY-zuh-kar-tuh, BIH-tuh", "audio_text": "Die Speisekarte, bitte"},
        {"category": "Dining", "english": "Mineral water, please", "foreign": "Ein Mineralwasser, bitte", "romanized": "Eyn mee-neh-RAHL-vah-ser, BIH-tuh", "audio_text": "Ein Mineralwasser, bitte"},
        {"category": "Dining", "english": "It tastes very delicious!", "foreign": "Es schmeckt sehr lecker!", "romanized": "Es shmekt zayr LEK-er!", "audio_text": "Es schmeckt sehr lecker"},
        {"category": "Dining", "english": "Do you have vegetarian dishes?", "foreign": "Haben Sie vegetarische Gerichte?", "romanized": "HAH-ben zee veh-geh-TAH-ree-shuh geh-RIKH-tuh?", "audio_text": "Haben Sie vegetarische Gerichte"},
        {"category": "Dining", "english": "What do you recommend?", "foreign": "Was können Sie empfehlen?", "romanized": "Vahs KUR-nen zee em-PFAY-len?", "audio_text": "Was können Sie empfehlen"},
        {"category": "Dining", "english": "One beer / coffee, please", "foreign": "Ein Bier / Ein Kaffee, bitte", "romanized": "Eyn beer / eyn KAH-fay, BIH-tuh", "audio_text": "Ein Bier, bitte"},
        {"category": "Dining", "english": "I have an allergy to nuts / gluten", "foreign": "Ich bin allergisch gegen Nüsse", "romanized": "Ikh bin ah-LAIR-gish GAY-gen NEW-suh", "audio_text": "Ich bin allergisch gegen Nüsse"},
        {"category": "Dining", "english": "Can we pay separately?", "foreign": "Können wir getrennt zahlen?", "romanized": "KUR-nen veer geh-TRENT TSAH-len?", "audio_text": "Können wir getrennt zahlen"},

        # Transport (10)
        {"category": "Transport", "english": "Where is the central railway station (Hauptbahnhof)?", "foreign": "Wo ist der Hauptbahnhof?", "romanized": "Voh ist der HOWPT-bahn-hohf?", "audio_text": "Wo ist der Hauptbahnhof"},
        {"category": "Transport", "english": "To the airport, please", "foreign": "Zum Flughafen, bitte", "romanized": "Tsoom FLOOK-hah-fen, BIH-tuh", "audio_text": "Zum Flughafen, bitte"},
        {"category": "Transport", "english": "Please stop here", "foreign": "Halten Sie bitte hier", "romanized": "HAHL-ten zee BIH-tuh heer", "audio_text": "Halten Sie bitte hier"},
        {"category": "Transport", "english": "Where can I buy a ticket (Fahrkarte)?", "foreign": "Wo kann ich eine Fahrkarte kaufen?", "romanized": "Voh kahn ikh EYE-nuh FAHR-kar-tuh KOW-fen?", "audio_text": "Wo kann ich eine Fahrkarte kaufen"},
        {"category": "Transport", "english": "Does this U-Bahn / S-Bahn go to the center?", "foreign": "Fährt diese Bahn ins Stadtzentrum?", "romanized": "Fairt DEE-zuh bahn ins SHTAHT-tsen-troom?", "audio_text": "Fährt diese Bahn ins Zentrum"},
        {"category": "Transport", "english": "Which platform for the ICE train?", "foreign": "Auf welchem Gleis fährt der Zug ab?", "romanized": "Owf VEL-khem glyes fairt der tsook ahp?", "audio_text": "Auf welchem Gleis fährt der Zug"},
        {"category": "Transport", "english": "How much is the taxi fare?", "foreign": "Wie viel kostet die Taxifahrt?", "romanized": "Vee feel KOHS-tet dee TAHK-see-fahrt?", "audio_text": "Wie viel kostet die Taxifahrt"},
        {"category": "Transport", "english": "What time is the next departure?", "foreign": "Wann fährt der nächste Zug?", "romanized": "Vahn fairt der NAYKH-stuh tsook?", "audio_text": "Wann fährt der nächste Zug"},
        {"category": "Transport", "english": "Can you call a taxi for me?", "foreign": "Können Sie mir ein Taxi rufen?", "romanized": "KUR-nen zee meer eyn TAHK-see ROO-fen?", "audio_text": "Können Sie mir ein Taxi rufen"},
        {"category": "Transport", "english": "Where is the bus stop?", "foreign": "Wo ist die Bushaltestelle?", "romanized": "Voh ist dee BOOS-hahl-tuh-shtel-luh?", "audio_text": "Wo ist die Bushaltestelle"},

        # Shopping (10)
        {"category": "Shopping", "english": "How much does that cost?", "foreign": "Wie viel kostet das?", "romanized": "Vee feel KOHS-tet dahs?", "audio_text": "Wie viel kostet das"},
        {"category": "Shopping", "english": "Can I pay by card (EC-Karte)?", "foreign": "Kann ich mit Karte zahlen?", "romanized": "Kahn ikh mit KAR-tuh TSAH-len?", "audio_text": "Kann ich mit Karte zahlen"},
        {"category": "Shopping", "english": "I will take this one", "foreign": "Ich nehme das", "romanized": "Ikh NAY-muh dahs", "audio_text": "Ich nehme das"},
        {"category": "Shopping", "english": "Can I try this on in the fitting room?", "foreign": "Kann ich das anprobieren?", "romanized": "Kahn ikh dahs AHN-proh-bee-ren?", "audio_text": "Kann ich das anprobieren"},
        {"category": "Shopping", "english": "Do you have another size or color?", "foreign": "Haben Sie das in einer anderen Größe?", "romanized": "HAH-ben zee dahs in EYE-ner AHN-deh-ren GRUR-suh?", "audio_text": "Haben Sie eine andere Größe"},
        {"category": "Shopping", "english": "That is too expensive", "foreign": "Das ist zu teuer", "romanized": "Dahs ist tsoo TOY-er", "audio_text": "Das ist zu teuer"},
        {"category": "Shopping", "english": "Can you give a discount?", "foreign": "Gibt es einen Rabatt?", "romanized": "Gipt es EYE-nen rah-BAHT?", "audio_text": "Gibt es einen Rabatt"},
        {"category": "Shopping", "english": "Please give me the receipt (Quittung)", "foreign": "Die Quittung, bitte", "romanized": "Dee KVIT-toong, BIH-tuh", "audio_text": "Die Quittung, bitte"},
        {"category": "Shopping", "english": "Can you gift wrap this item?", "foreign": "Können Sie das als Geschenk einpacken?", "romanized": "KUR-nen zee dahs ahls geh-SHENK EYN-pah-ken?", "audio_text": "Als Geschenk einpacken"},
        {"category": "Shopping", "english": "What time does the store close?", "foreign": "Wann schließt das Geschäft?", "romanized": "Vahn shleest dahs geh-SHEFT?", "audio_text": "Wann schließt das Geschäft"},

        # Emergency (10)
        {"category": "Emergency", "english": "Help, please!", "foreign": "Hilfe, bitte!", "romanized": "HIL-fuh, BIH-tuh!", "audio_text": "Hilfe, bitte"},
        {"category": "Emergency", "english": "Call the police (Polizei - 110)", "foreign": "Rufen Sie sofort die Polizei!", "romanized": "ROO-fen zee zoh-FORT dee poh-lee-TSYE!", "audio_text": "Rufen Sie die Polizei"},
        {"category": "Emergency", "english": "Call an ambulance (112)", "foreign": "Rufen Sie einen Krankenwagen!", "romanized": "ROO-fen zee EYE-nen KRAHN-ken-vah-gen!", "audio_text": "Rufen Sie einen Krankenwagen"},
        {"category": "Emergency", "english": "I need a doctor / hospital", "foreign": "Ich brauche einen Arzt / ein Krankenhaus", "romanized": "Ikh BROW-khuh EYE-nen ahrts", "audio_text": "Ich brauche einen Arzt"},
        {"category": "Emergency", "english": "I lost my passport and wallet", "foreign": "Ich habe meinen Reisepass und Geldbeutel verloren", "romanized": "Ikh HAH-buh MY-nen RYE-zuh-pahs fair-LOH-ren", "audio_text": "Ich habe meinen Pass verloren"},
        {"category": "Emergency", "english": "I feel very sick", "foreign": "Mir ist sehr schlecht", "romanized": "Meer ist zayr shlekht", "audio_text": "Mir ist sehr schlecht"},
        {"category": "Emergency", "english": "There has been an accident", "foreign": "Es gab einen Unfall", "romanized": "Es gahp EYE-nen OON-fahl", "audio_text": "Es gab einen Unfall"},
        {"category": "Emergency", "english": "Where is the police station?", "foreign": "Wo ist die Polizeiwache?", "romanized": "Voh ist dee poh-lee-TSYE-vah-khuh?", "audio_text": "Wo ist die Polizeiwache"},
        {"category": "Emergency", "english": "Where is my embassy / consulate?", "foreign": "Wo ist die Botschaft?", "romanized": "Voh ist dee BOHT-shahft?", "audio_text": "Wo ist die Botschaft"},
        {"category": "Emergency", "english": "I am lost, can you help me?", "foreign": "Ich habe mich verlaufen, können Sie mir helfen?", "romanized": "Ikh HAH-buh mikh fair-LOW-fen, KUR-nen zee meer HEL-fen?", "audio_text": "Können Sie mir helfen"},

        # Directions (10)
        {"category": "Directions", "english": "Where is the restroom / toilet (WC)?", "foreign": "Wo ist die Toilette / das WC, bitte?", "romanized": "Voh ist dee twah-LET-tuh / dahs vay-TSAY?", "audio_text": "Wo ist die Toilette"},
        {"category": "Directions", "english": "Where is the nearest pharmacy (Apotheke) / ATM (Geldautomat)?", "foreign": "Wo ist die nächste Apotheke oder Geldautomat?", "romanized": "Voh ist dee NAYKH-stuh ah-poh-TAY-kuh?", "audio_text": "Wo ist die nächste Apotheke"},
        {"category": "Directions", "english": "Go straight ahead", "foreign": "Gehen Sie geradeaus", "romanized": "GAY-en zee geh-RAH-duh-ows", "audio_text": "Gehen Sie geradeaus"},
        {"category": "Directions", "english": "Turn left / Turn right", "foreign": "Biegen Sie links ab / Biegen Sie rechts ab", "romanized": "BEE-gen zee links ahp / rekhts ahp", "audio_text": "Biegen Sie links ab"},
        {"category": "Directions", "english": "Where is the city center / Cathedral?", "foreign": "Wo ist das Stadtzentrum / der Dom?", "romanized": "Voh ist dahs SHTAHT-tsen-troom?", "audio_text": "Wo ist das Stadtzentrum"},
        {"category": "Directions", "english": "Is it far on foot?", "foreign": "Ist es zu Fuß weit?", "romanized": "Ist es tsoo foos vye-t?", "audio_text": "Ist es zu Fuß weit"},
        {"category": "Directions", "english": "Where is the entrance / exit?", "foreign": "Wo ist der Eingang / Ausgang?", "romanized": "Voh ist der EYN-gahng / OWZ-gahng?", "audio_text": "Wo ist der Eingang"},
        {"category": "Directions", "english": "Can you show me the route on Google Maps?", "foreign": "Können Sie mir das auf der Karte zeigen?", "romanized": "KUR-nen zee meer dahs owf dair KAR-tuh TSY-gen?", "audio_text": "Zeigen Sie mir das auf der Karte"},
        {"category": "Directions", "english": "Which way to the castle / landmark?", "foreign": "Wie komme ich zum Schloss?", "romanized": "Vee KOH-muh ikh tsoom shlohs?", "audio_text": "Wie komme ich zum Schloss"},
        {"category": "Directions", "english": "Is this the right street?", "foreign": "Ist das die richtige Straße?", "romanized": "Ist dahs dee RIKH-tee-guh SHTRAH-suh?", "audio_text": "Ist das die richtige Straße"}
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
