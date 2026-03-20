import json

from ranker import compute_idf, rank_documents
from text_editor import process_text


def load_data(index_path, doc_lengths_path, documents_path):
    with open(index_path, "r") as f:
        index = json.load(f)

    with open(doc_lengths_path, "r") as f:
        doc_lengths = json.load(f)

    doc_lengths = {int(k): v for k, v in doc_lengths.items()}

    doc_id_to_title = {}
    with open(documents_path, "r") as f:
        for line in f:
            doc = json.loads(line)
            doc_id_to_title[doc["id"]] = doc["title"]

    total_docs = len(doc_lengths)
    idf = compute_idf(index, total_docs)

    return index, idf, doc_lengths, doc_id_to_title


def search(query, index, idf, doc_lengths, doc_id_to_title, top_k=10):
    query_terms = process_text(query)

    ranked = rank_documents(query_terms, index, idf, doc_lengths, top_k)

    results = []
    for doc_id, score in ranked:
        title = doc_id_to_title.get(doc_id, f"[Doc {doc_id}]")
        results.append((title, score))

    return results


if __name__ == "__main__":
    index, idf, doc_lengths, doc_id_to_title = load_data(
        "data/index.json", "data/doc2ntoks.json", "data/documents.jsonl"
    )
    while True:
        query = input("\nSearch: ")
        results = search(query, index, idf, doc_lengths, doc_id_to_title)
        for title, score in results:
            print(f"{score:.4f}  {title}")
