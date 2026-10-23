import re


def normalize_text(text):
    text = str(text).lower()

    replacements = {
        "0": "o",
        "1": "i",
        "3": "e",
        "@": "a",
        "$": "s"
    }

    for symbol, letter in replacements.items():
        text = text.replace(symbol, letter)

    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


if __name__ == "__main__":
    messages = [
        "Fr33 pr1ze j33t0 abhi cl@im karo",
        "Yar kal university ana hai",
        "URG3NT! Ur acc0unt needs verific@ti0n."
    ]

    for message in messages:
        print("Original:", message)
        print("Normalized:", normalize_text(message))
        print()