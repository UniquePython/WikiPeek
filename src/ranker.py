import math
from collections import Counter


def compute_idf(index: dict, total_docs: int) -> dict:
    idf = {}
    for term, data in index.items():
        ndocs = len(data)
        idf[term] = math.log(total_docs / ndocs)

    return idf


def score_document(
    doc_id: int, query_terms: list[str], index: dict, idf: dict, doc_lengths: dict
) -> float:
    score = 0.0

    for term in query_terms:
        if term not in index or term not in idf:
            continue

        postings = index[term]

        for d_id, count in postings:
            if d_id == doc_id:
                tf = count / doc_lengths[doc_id]
                score += tf * idf[term]
                break

    return score


def rank_documents(query_terms, index, idf, doc_lengths, top_k=10):
    candidate_docs = set()
    term_postings = {}

    query_counts = Counter(query_terms)

    for term in query_counts:
        if term in index:
            postings_dict = {int(k): v for k, v in index[term]}
            term_postings[term] = postings_dict
            candidate_docs.update(postings_dict.keys())

    scored_docs = []

    for doc_id in candidate_docs:
        score = 0.0
        for term, qtf in query_counts.items():
            postings = term_postings.get(term)
            if postings and doc_id in postings:
                tf = postings[doc_id] / doc_lengths[doc_id]
                score += qtf * tf * idf.get(term, 0)
        scored_docs.append((doc_id, score))

    scored_docs.sort(key=lambda x: x[1], reverse=True)
    return scored_docs[:top_k]
