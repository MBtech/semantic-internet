import json
from search.search_agent import answer_query, search_and_insert_into_chromadb
import sys 

def read_json_file(file_path):
    """Reads a JSON file and returns its content."""
    with open(file_path, 'r') as f:
        return json.load(f)



if __name__ == "__main__":
    DATASET = sys.argv[1]

    file_path = f"data/search_results/{DATASET}_500_top20.json"
    data = read_json_file(file_path)
    top_k_list = [1, 2, 5, 10, 15]

    

    all_output_data = {}


    start_index = 100


    # Initialize output data
    for top_k in top_k_list:
        # Check if the output file already exists and load its content
        output_file_path = f"data/results/global_{DATASET}_topk_{top_k}.json"
        try:
            with open(output_file_path, 'r') as f:
                all_output_data[f"topk_{top_k}"] = json.load(f)
        except FileNotFoundError:
            all_output_data[f"topk_{top_k}"] = []

    for i, entry in enumerate(data[:200]):

        if i < start_index:
            continue

        question = entry["question"]
        urls = entry["url"]
        collection, num_chunks = search_and_insert_into_chromadb(question, urls, index=i, dataset=DATASET, search=False)
        for top_k in top_k_list:
            output_file_path = f"data/results/global_{DATASET}_topk_{top_k}.json"
            response, chunks = answer_query(question, collection, top_k=top_k)
            print(i)
            print(question)
            print(response)
            output_data = {
                "question": question, "response": response.answer, "relevant_context_present": response.relevant_context_present,  "chunks": chunks, "total_num_chunks": num_chunks
            }
            all_output_data[f"topk_{top_k}"].append(output_data)
            # Write results in every iteration, appending to the same file
            with open(output_file_path, 'w') as outfile:
                json.dump(all_output_data[f"topk_{top_k}"], outfile, indent=4)
