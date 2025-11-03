from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.contextualize import get_context_with_gemini

def split_docs_to_chunks(markdown_docs):
    doc_chunks = []
    for doc in markdown_docs:
        doc_chunks.extend(split_to_chunks(doc))

    return doc_chunks

def split_to_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 100, use_context = False):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,  # adjust to your needs (in characters)
        chunk_overlap=chunk_overlap,  # optional overlap (in characters)
        length_function=len,  # default, measuring by character length
        is_separator_regex=False,  # treat separators literally, unless regex
    )
    chunks = text_splitter.split_text(text)
    contextualized_chunks = []
    for chunk in chunks:
        if use_context:
            context = get_context_with_gemini(text, chunk)
        else:
            context = ""
        contextualized_chunks.append(context + chunk)
    return contextualized_chunks