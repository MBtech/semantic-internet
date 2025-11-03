
import json
import os

def compare_retrieved_info(base_path, docling_path):
    """
    Compares the retrieved_info.json files in two directories.
    """
    base_dirs = {d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))}
    docling_dirs = {d for d in os.listdir(docling_path) if os.path.isdir(os.path.join(docling_path, d))}

    common_dirs = base_dirs.intersection(docling_dirs)

    for dir_name in common_dirs:
        base_json_path = os.path.join(base_path, dir_name, 'retrieved_info.json')
        docling_json_path = os.path.join(docling_path, dir_name, 'retrieved_info.json')

        if os.path.exists(base_json_path) and os.path.exists(docling_json_path):
            with open(base_json_path, 'r') as f1, open(docling_json_path, 'r') as f2:
                try:
                    data1 = json.load(f1)
                    data2 = json.load(f2)

                    if data1["successful_urls"] == data2["successful_urls"]:
                        print(f"Files in {dir_name} are identical.")
                    else:
                        print(len(data2["successful_urls"])-len(data1["successful_urls"]))
                        print(f"Files in {dir_name} are different.")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in {dir_name}: {e}")

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    base_downloaded_path = os.path.join(project_root, 'data', 'downloaded_files')
    docling_downloaded_path = os.path.join(project_root, 'data', 'docling', 'downloaded_files')

    compare_retrieved_info(base_downloaded_path, docling_downloaded_path)
