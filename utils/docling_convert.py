
from docling.document_converter import DocumentConverter
from timeout_function_decorator import timeout

# Change this to a local path or another URL if desired.
# Note: using the default URL requires network access; if offline, provide a
# local file path (e.g., Path("/path/to/file.pdf")).
# source = "https://arxiv.org/pdf/2408.09869"
# source = "https://docling-project.github.io/docling/examples/minimal/"

@timeout(30)
def convert_to_markdown(source):
    converter = DocumentConverter()
    result = converter.convert(source)

    return result.document.export_to_markdown()


if __name__ == "__main__":
    import json
    data = json.load(open("data/trivia_web_dev_search_results.json"))
    for entry in data[:1]:
        question = entry["question"]
        urls = entry["url"]
        print(question)
        print(urls)
        for url in urls:
            print("######New URL######")
            convert_to_markdown(url)
            print("\n\n\n\n\n")