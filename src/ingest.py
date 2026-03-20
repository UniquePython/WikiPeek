import bz2
import json
import re
import xml.etree.ElementTree as ET


def parse_dump(dump_path: str, output_path: str) -> None:
    NS = "{http://www.mediawiki.org/xml/export-0.11/}"

    with bz2.open(dump_path, "rb") as f, open(output_path, "w") as out:
        doc_id = 0
        for event, element in ET.iterparse(f, events=("end",)):
            if element.tag == f"{NS}page":
                ns = element.findtext(f"{NS}ns")
                title = element.findtext(f"{NS}title")
                text = element.findtext(f"{NS}revision/{NS}text")
                element.clear()

                if ns != "0" or not text:
                    continue

                text = extract_text(text)
                record = {"id": doc_id, "title": title, "text": text}
                out.write(json.dumps(record) + "\n")
                doc_id += 1

                if doc_id % 10_000 == 0:
                    print(f"{doc_id} articles processed...")


def extract_text(raw_wiki_text: str) -> str:
    # NOTE: nested templates like {{a|{{b}}}} will leave stray }}
    raw_wiki_text = re.sub(
        r"\{\{.*?\}\}", "", raw_wiki_text, flags=re.DOTALL
    )  # remove {{...}} templates
    raw_wiki_text = re.sub(
        r"\[\[(?:File|Image):[^\]]*\]\]",
        "",
        raw_wiki_text,
        flags=re.IGNORECASE | re.DOTALL,
    )  # ignore file / image links
    raw_wiki_text = re.sub(
        r"\[\[(?:[^\]|]*\|)*([^\]|]+)\]\]", r"\1", raw_wiki_text
    )  # handles [[a]], [[a|b]], [[a|b|c|d]] -> always takes last segment
    raw_wiki_text = re.sub(
        r"thumb\|[\w|]+\|", "", raw_wiki_text
    )  # remove image thumbnail directives
    raw_wiki_text = re.sub(
        r"<.*?>", "", raw_wiki_text, flags=re.DOTALL
    )  # remove HTML tags
    raw_wiki_text = re.sub(
        r"\[https?://\S+\s*(.*?)\]", r"\1", raw_wiki_text
    )  # External links like [http://example.com Some text] -> "Some text"
    raw_wiki_text = re.sub(
        r"=+\s*(.*?)\s*=+", r"\1", raw_wiki_text
    )  # get the part inside ==...==
    raw_wiki_text = re.sub(
        r"'{2,3}(.*?)'{2,3}", r"\1", raw_wiki_text
    )  # get the part inside ''...'' and '''...'''
    raw_wiki_text = re.sub(r"\s{2,}", " ", raw_wiki_text)  # collapse whitespace
    raw_wiki_text = re.sub(
        r"^\*+\s*", "", raw_wiki_text, flags=re.MULTILINE
    )  # remove bullet points
    return raw_wiki_text.strip()


if __name__ == "__main__":
    parse_dump("data/simplewiki-latest-pages-articles.xml.bz2", "data/documents.jsonl")
