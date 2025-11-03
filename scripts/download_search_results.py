import json
import sys

from utils.retrieve_md_from_urls import get_md_from_url_docling


def read_json_file(file_path):
    """Reads a JSON file and returns its content."""
    with open(file_path, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    DATASET = sys.argv[1]
    file_path = f"data/search_results/{DATASET}_500_top20.json"
    # file_path = "data/news_search_results.json"
    data = read_json_file(file_path)

    for index, entry in enumerate(data):
        print(index)
        question = entry["question"]
        urls = entry["url"]
        if index < 0:
            continue
        _ = get_md_from_url_docling(urls, question, index, dataset=DATASET)
