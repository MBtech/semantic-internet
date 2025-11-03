from search.url_to_md import ArticleExtractor
from utils.docling_convert import convert_to_markdown
import os
import json
import hashlib


def get_md_from_url(search_urls, query):
    markdown_docs = []

    # Create a unique subfolder based on the query hash
    query_hash = hashlib.md5(query.encode()).hexdigest()
    query_output_dir = os.path.join("data/downloaded_files", query_hash)
    os.makedirs(query_output_dir, exist_ok=True)

    retrieved_info = {"query": query, "successful_urls": []}

    for url in search_urls:
        file_name = os.path.join(
            query_output_dir, f"{url.replace('/', '_').replace(':', '')}.md"
        )

        if os.path.exists(file_name):
            print(f"File already exists for URL: {url}. Skipping download.")
            with open(file_name, "r", encoding="utf-8") as f:
                markdown_docs.append(f.read())
            retrieved_info["successful_urls"].append(url)
        else:
            extractor = ArticleExtractor()
            try:
                print(f"Downloading URL: {url}")
                markdown_output = extractor.url_to_markdown(url)
                if not markdown_output:
                    continue
                if len(markdown_output) > 100:  # Skip writing very small outputs
                    markdown_docs.append(markdown_output)
                    with open(file_name, "w", encoding="utf-8") as f:
                        f.write(markdown_output)
                    retrieved_info["successful_urls"].append(url)
            except Exception:
                print(f"Error processing URL: {url}")

    # Write query and successful URLs to a JSON file
    with open(
        os.path.join(query_output_dir, "retrieved_info.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(retrieved_info, f, indent=4)

    return markdown_docs


def get_md_from_url_docling(search_urls, query, index, dataset="general", search=True):
    markdown_docs = []

    # Create a unique subfolder based on the query hash
    # query_hash = hashlib.md5(query.encode()).hexdigest()
    question_num = f"Q_{index}"
    query_output_dir = os.path.join(
        f"data/docling/{dataset}/downloaded_files", question_num
    )
    os.makedirs(query_output_dir, exist_ok=True)

    retrieved_info = {"query": query, "successful_urls": []}

    for url in search_urls:
        if url in [
            "https://en.wikipedia.org/wiki/Reptile",
            "https://www.thoughtco.com/the-six-basic-animal-groups-4096604",
            "https://myanimals.com/animals/wild-animals-animals/invertebrates/10-types-of-insects-and-their-characteristics/",
            "https://www.kuioo.com/what-animal-face-type-are-you/",
            "https://www.history.com/articles/dinosaurs-first-discovery",
            "https://www.came.com/us/",
            "https://www.merriam-webster.com/dictionary/came",
            "https://en.wikipedia.org/wiki/Marsilea",
            "https://aquariumbreeder.com/marsilea-hirsuta-care-guide-planting-growing-and-propagation/"
        ]:
            continue

        file_name = os.path.join(
            query_output_dir, f"{url.replace('/', '_').replace(':', '')}.md"
        )

        if os.path.exists(file_name):
            print(f"File already exists for URL: {url}. Skipping download.")
            with open(file_name, "r", encoding="utf-8") as f:
                markdown_docs.append(f.read())
            retrieved_info["successful_urls"].append(url)
        elif search:
            try:
                print(f"Downloading URL: {url}")
                markdown_output = convert_to_markdown(url)
                if not markdown_output:
                    continue
                if len(markdown_output) > 100:  # Skip writing very small outputs
                    markdown_docs.append(markdown_output)
                    with open(file_name, "w", encoding="utf-8") as f:
                        f.write(markdown_output)
                    retrieved_info["successful_urls"].append(url)
            except Exception:
                print(f"Error processing URL: {url}")
        else:
            print(f"Search Disabled, so skipping URL: {url}")


    # Write query and successful URLs to a JSON file
    with open(
        os.path.join(query_output_dir, "retrieved_info.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(retrieved_info, f, indent=4)

    return markdown_docs
