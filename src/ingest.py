import re


def parse_dump(dump_path: str, output_path: str) -> None:
    pass


def extract_text(raw_wiki_text: str) -> str:
    # NOTE: nested templates like {{a|{{b}}}} will leave stray }}
    raw_wiki_text = re.sub(
        r"\{\{.*?\}\}", "", raw_wiki_text, flags=re.DOTALL
    )  # remove {{...}} templates
    raw_wiki_text = re.sub(
        r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", raw_wiki_text, flags=re.DOTALL
    )  # get the part after | from [[...|...]]
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
    return raw_wiki_text.strip()


if __name__ == "__main__":
    parse_dump("data/simplewiki-latest-pages-articles.xml.bz2", "documents.jsonl")
