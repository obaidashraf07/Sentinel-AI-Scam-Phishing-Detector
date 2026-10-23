import joblib
import re
from text_preprocessing import normalize_text

model = joblib.load("models/multilingual_scam_detector.pkl")

scam_indicators = {
    "prize": "Message mein prize jeetne ka dawa hai.",
    "inaam": "Message mein inaam milne ka dawa hai.",
    "lottery": "Message mein lottery ka zikr hai.",
    "claim": "Message mein reward claim karne ka kaha gaya hai.",
    "payment": "Message mein payment ka mutalba ho sakta hai.",
    "fee": "Message mein fee ya charges ka zikr hai.",
    "transfer": "Message mein paisay transfer karne ka zikr hai.",
    "blocked": "Message mein account block hone ki warning hai.",
    "band": "Message mein account band hone ka zikr hai.",
    "verify": "Message mein verification ka zikr hai.",
    "verification": "Message mein verification ka zikr hai.",
    "free": "Message mein free offer ka dawa hai.",
    "urgent": "Message mein urgency paida karne wali language hai.",
    "congratulations": "Message mein reward jeetne ka dawa ho sakta hai.",
    "link": "Message mein link ka zikr hai."
}

credential_words = ["password", "otp", "pin", "passcode"]

request_words = [
    "send", "share", "provide", "enter", "reply",
    "give", "tell", "submit", "confirm", "provide",
    "maange", "mangain", "bhejein", "batayein",
    "likhein", "darj", "send karo", "share karo"
]

protective_phrases = [
    "never share",
    "do not share",
    "dont share",
    "don t share",
    "never give",
    "do not give",
    "dont give",
    "don t give",
    "never disclose",
    "do not disclose",
    "dont disclose",
    "don t disclose",
    "never send",
    "do not send",
    "dont send",
    "don t send",
    "keep your password private",
    "keep your otp private",
    "kabhi share na karein",
    "kabhi share na karen",
    "kisi ko na batayein",
    "kisi ko mat batayein",
    "share na karein",
    "share na karen",
    "mat share karein"
]


def explain_message(message):
    normalized_message = normalize_text(message)
    prediction = model.predict([normalized_message])[0]

    print("\nOriginal Message:", message)
    print("Normalized Message:", normalized_message)

    if prediction == "scam":
        print("\nPrediction: SCAM / SUSPICIOUS")
    else:
        print("\nPrediction: NORMAL")

    indicators = []

    # Check whether the message gives safety advice
    protective_advice = any(
        phrase in normalized_message
        for phrase in protective_phrases
    )

    # Check whether credentials are being requested
    credential_found = [
        word for word in credential_words
        if word in normalized_message.split()
    ]

    request_found = any(
        word in normalized_message.split()
        for word in request_words
    )

    if credential_found:
        if protective_advice:
            indicators.append(
                "Message password/OTP share na karne ki safety advice deta hai."
            )
        elif request_found:
            indicators.append(
                "Message mein password, OTP ya security code maanga ja sakta hai."
            )
        else:
            indicators.append(
                "Message mein password/OTP ka zikr hai; context manually check karein."
            )

    # Check other keyword indicators
    words = set(normalized_message.split())

    for word, explanation in scam_indicators.items():
        if word in words:
            indicators.append(explanation)

    # Display account context without claiming it is always suspicious
    if "account" in words:
        indicators.append("Message account se related hai.")

    print("\nMessage Analysis:")

    if indicators:
        for indicator in sorted(set(indicators)):
            print("-", indicator)
    else:
        print("- Koi predefined indicator detect nahi hua.")

    print("\nNote: Indicators keyword/context rules hain, model ki actual reasoning nahi.")

    if prediction == "scam":
        print(
            "\nSafety Advice: Sender verify karein. "
            "OTP, password ya banking details share na karein."
        )
    else:
        print(
            "\nSafety Advice: NORMAL prediction safety ki guarantee nahi hai. "
            "Unknown links se ehtiyat karein."
        )


if __name__ == "__main__":
    print("=" * 40)
    print("SCAM AND PHISHING DETECTOR")
    print("With Context-Aware Message Explanation")
    print("=" * 40)

    while True:
        message = input(
            "\nEnter a message (or type 'exit' to stop): "
        ).strip()

        if message.lower() == "exit":
            print("Detector closed.")
            break

        if not message:
            print("Please enter a message.")
            continue

        explain_message(message)