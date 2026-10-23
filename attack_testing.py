
import os
import pandas as pd
import joblib

from text_preprocessing import normalize_text

model_path = "models/multilingual_scam_detector.pkl"
model = joblib.load(model_path)

messages = [
    # Standard English scams
    ("Standard English Scam", "Congratulations! You have won a free prize. Claim now.", "scam"),
    ("Standard English Scam", "Your bank account will be blocked. Verify your details immediately.", "scam"),
    ("Standard English Scam", "Pay a registration fee to receive your online job offer.", "scam"),
    ("Standard English Scam", "Send your OTP to claim your cash reward.", "scam"),
    ("Standard English Scam", "You have been selected for a cash lottery. Pay the processing fee.", "scam"),
    ("Standard English Scam", "Your account will be suspended unless you verify your details.", "scam"),

    # Obfuscated scams
    ("Obfuscated Scam", "U have w0n a fr33 pr1ze. Cl@im n0w.", "scam"),
    ("Obfuscated Scam", "URG3NT! V3rify ur acc0unt n0w.", "scam"),
    ("Obfuscated Scam", "Fr33 pr1ze j33t0 abhi cl@im karo.", "scam"),
    ("Obfuscated Scam", "Cl@im ur rew@rd bef0re it expires.", "scam"),
    ("Obfuscated Scam", "Y0ur acc0unt is l0cked. Send OTP n0w.", "scam"),
    ("Obfuscated Scam", "W1n cash n0w by paying a small fee.", "scam"),

    # Roman Urdu scams
    ("Roman Urdu Scam", "Apka inaam nikla hai, abhi claim karein.", "scam"),
    ("Roman Urdu Scam", "Aapka parcel rok diya gaya hai, release fee bhejein.", "scam"),
    ("Roman Urdu Scam", "Scholarship approve hai, processing fee abhi jama karwayein.", "scam"),
    ("Roman Urdu Scam", "Refund lene ke liye bank details aur OTP share karein.", "scam"),
    ("Roman Urdu Scam", "Investment par double profit ke liye abhi paise transfer karein.", "scam"),
    ("Roman Urdu Scam", "Aapka account band ho jayega, foran verification karein.", "scam"),

    # Mixed-language scams
    ("Mixed Language Scam", "Your account band ho jayega, verify now.", "scam"),
    ("Mixed Language Scam", "Free prize claim karne ke liye payment bhejein.", "scam"),
    ("Mixed Language Scam", "Your refund ready hai, click the link and enter details.", "scam"),
    ("Mixed Language Scam", "Online job confirm hai, registration fee transfer karein.", "scam"),
    ("Mixed Language Scam", "Bank verification ke liye apna OTP send karein.", "scam"),
    ("Mixed Language Scam", "Congratulations! Aap cash reward jeet gaye hain.", "scam"),

    # Account security scams
    ("Account Security Scam", "Your bank account is blocked. Send your OTP now.", "scam"),
    ("Account Security Scam", "Your account will be closed today. Verify your password immediately.", "scam"),
    ("Account Security Scam", "We detected suspicious activity. Share your login code to restore access.", "scam"),
    ("Account Security Scam", "Your payment failed. Click the link to confirm your banking details.", "scam"),

    # Normal messages
    ("Normal Message", "I paid my university fee through my bank account.", "normal"),
    ("Normal Message", "Teacher shared the assignment link in our class group.", "normal"),
    ("Normal Message", "I received a payment confirmation for my online order.", "normal"),
    ("Normal Message", "Please verify the information in my university form.", "normal"),
    ("Normal Message", "My parcel arrived and I paid the delivery fee.", "normal"),
    ("Normal Message", "I changed my account password using the official website.", "normal"),
    ("Normal Message", "Our teacher announced a prize for the best project.", "normal"),
    ("Normal Message", "I will send the project details to you tomorrow.", "normal"),

    # Normal banking messages
    ("Normal Banking Message", "I contacted my bank about my account.", "normal"),
    ("Normal Banking Message", "My bank sent me a monthly account statement.", "normal"),
    ("Normal Banking Message", "I changed my bank password through the official app.", "normal"),
    ("Normal Banking Message", "I received my salary in my bank account today.", "normal"),
]

results = []

for category, message, expected in messages:
    normalized_message = normalize_text(message)
    prediction = model.predict([normalized_message])[0]

    result = "CORRECT" if prediction == expected else "INCORRECT"

    results.append({
        "Category": category,
        "Message": message,
        "Expected Label": expected,
        "Predicted Label": prediction,
        "Result": result
    })

    print("\nCategory:", category)
    print("Message:", message)
    print("Expected:", expected)
    print("Predicted:", prediction)
    print("Result:", result)

os.makedirs("results", exist_ok=True)

results_df = pd.DataFrame(results)

results_df.to_csv(
    "results/attack_testing_results.csv",
    index=False,
    encoding="utf-8"
)

correct = (results_df["Result"] == "CORRECT").sum()
total = len(results_df)

print("\n========== CHALLENGE TEST SUMMARY ==========")
print("Total messages:", total)
print("Correct predictions:", correct)
print("Incorrect predictions:", total - correct)
print("Test accuracy:", round(correct / total * 100, 2), "%")

print("\n========== CATEGORY-WISE RESULTS ==========")

category_results = results_df.groupby("Category").agg(
    Total=("Result", "count"),
    Correct=("Result", lambda x: (x == "CORRECT").sum()),
    Incorrect=("Result", lambda x: (x == "INCORRECT").sum())
)

category_results["Accuracy (%)"] = (
    category_results["Correct"] / category_results["Total"] * 100
).round(2)

print(category_results.to_string())

print("\n========== INCORRECT PREDICTIONS ==========")

errors = results_df[results_df["Result"] == "INCORRECT"]

if errors.empty:
    print("No incorrect predictions in this test set.")
else:
    print(errors[
        ["Category", "Message", "Expected Label", "Predicted Label"]
    ].to_string(index=False))

print("\nResults saved to results/attack_testing_results.csv")

