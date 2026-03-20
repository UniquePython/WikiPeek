import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Run only once
nltk.download("stopwords", quiet=True)

stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()


def process_text(text: str) -> list[str]:
    text = text.lower()
    tokens = re.findall(r"[a-z]+", text)
    filtered_words = [word for word in tokens if word not in stop_words]
    stemmed = [stemmer.stem(filtered_word) for filtered_word in filtered_words]
    return stemmed


def tokenize_document(doc: dict) -> dict:
    return {**doc, "tokens": process_text(doc["text"])}


if __name__ == "__main__":
    print(process_text("Black holes are the most fascinating objects in the Universe"))
    print(process_text("The quick brown fox jumps over the lazy dog"))
