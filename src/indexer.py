import json
from collections import Counter, defaultdict

from text_editor import tokenize_document


def build_index(documents_path: str, index_path: str, doc2ntoks_path: str) -> None:
    index = defaultdict(list)
    doc2ntoks = {}

    with open(documents_path) as f:
        for i, line in enumerate(f):
            doc = json.loads(line)
            doc = tokenize_document(doc)

            counts = Counter(doc["tokens"])
            for term, freq in counts.items():
                index[term].append((doc["id"], freq))

            doc2ntoks[doc["id"]] = len(doc["tokens"])

            if (i + 1) % 10_000 == 0:
                print(f"{i + 1} documents indexed...")

    save_index(dict(index), index_path)
    save_doc2ntoks(doc2ntoks, doc2ntoks_path)


def save_index(index: dict, path: str) -> None:
    with open(path, "w") as f:
        json.dump(index, f)


def save_doc2ntoks(doc2ntoks: dict, path: str) -> None:
    with open(path, "w") as f:
        json.dump(doc2ntoks, f)


if __name__ == "__main__":
    build_index("data/documents.jsonl", "data/index.json", "data/doc2ntoks.json")
