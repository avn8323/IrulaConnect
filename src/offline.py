def offline_answer(message, language="english"):
    responses = {
        "english": "I'm offline right now, so my general-knowledge brain is taking a tiny nap. I can still help you explore the Irula corpus!",
        "tamil": "இப்போது இணைய இணைப்பு இல்லை. IrulaConnect-இல் உள்ள சொற்களையும் உள்ளடக்கத்தையும் தேடலாம்.",
        "telugu": "ఇప్పుడు ఇంటర్నెట్ అందుబాటులో లేదు. IrulaConnectలో ఉన్న పదాలు, సమాచారాన్ని వెతకవచ్చు.",
        "hindi": "अभी इंटरनेट उपलब्ध नहीं है। मैं IrulaConnect के शब्दों और उपलब्ध सामग्री को खोजने में मदद कर सकती हूँ।",
    }
    return responses.get(language, responses["english"])
