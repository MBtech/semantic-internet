import json
import os
import pandas as pd
import seaborn as sns
import sys 
import matplotlib.pyplot as plt

def plot_relevant_context_summary(file_paths, output_dir, file_name_mapping, plot_file_name):
    """
    Reads multiple JSON files, and for each question, calculates the number of chunks used and 
    the percentage of total chunks used. It then generates box plots summarizing these distributions 
    for each configuration.

    Args:
        file_paths (list): A list of absolute paths to the JSON files.
        output_dir (str): The directory where the output plot will be saved.
        file_name_mapping (dict): A dictionary mapping filenames to display names.
        plot_file_name (str): The filename for the output plot.
    """
    all_question_data = []
    summary_data = []
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            file_name = os.path.basename(file_path)
            display_name = file_name_mapping.get(file_name, file_name)
            
            questions_with_context = 0
            total_questions = len(data)

            for item in data:
                num_chunks = len(item.get("chunks", []))
                total_num_chunks = item.get("total_num_chunks", 0)
                percentage = (num_chunks / total_num_chunks) * 100 if total_num_chunks > 0 else 0
                
                if item.get("relevant_context_present", False):
                    questions_with_context += 1

                all_question_data.append({
                    "Configuration": display_name,
                    "Number of Chunks": num_chunks,
                    "Percentage of Chunks": percentage
                })
            
            if total_questions > 0:
                summary_data.append({
                    "Configuration": display_name,
                    "Questions with Context": questions_with_context
                })

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error processing file {file_path}: {e}")

    if not all_question_data:
        print("No data to plot.")
        return

    df = pd.DataFrame(all_question_data)
    print(df)

    summary_df = pd.DataFrame(summary_data)
    print(summary_df)

    plt.rcParams.update({'font.size': 14})
    fig, axes = plt.subplots(3, 1, figsize=(12, 21))

    # Box plot for Number of Chunks
    sns.boxplot(ax=axes[0], x="Configuration", y="Number of Chunks", data=df)
    axes[0].set_title('Number of Chunks per Question', fontsize=16)
    axes[0].tick_params(axis='x', rotation=20)

    # Box plot for Percentage of Chunks
    sns.boxplot(ax=axes[1], x="Configuration", y="Percentage of Chunks", data=df)
    axes[1].set_title('Percentage of Total Chunks Used per Question', fontsize=16)
    axes[1].tick_params(axis='x', rotation=20)

    # Bar plot for questions with relevant context
    sns.barplot(ax=axes[2], x="Configuration", y="Questions with Context", data=summary_df)
    axes[2].set_title('Total Questions with Relevant Context', fontsize=16)
    axes[2].tick_params(axis='x', rotation=20)

    plt.tight_layout()

    output_path = os.path.join(output_dir, plot_file_name)
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")

if __name__ == "__main__":
    DATASET = sys.argv[1]
    CONFIG = sys.argv[2]
    # The script should be run from the root of the project directory.
    # Adjust the paths if necessary.
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data/results")
    plots_dir = os.path.join(base_dir, "plots")

    if CONFIG == "individual":
        plot_file_name = f"{CONFIG}_{DATASET}_relevant_context.png"
        files_to_process = [
            os.path.join(data_dir, f"{CONFIG}_{DATASET}_maxsources_2_topk_1.json"),
            os.path.join(data_dir, f"{CONFIG}_{DATASET}_maxsources_2_topk_2.json"),
            os.path.join(data_dir, f"{CONFIG}_{DATASET}_maxsources_2_topk_5.json"),
            os.path.join(data_dir, f"{CONFIG}_{DATASET}_maxsources_3_topk_1.json"),
            os.path.join(data_dir, f"{CONFIG}_{DATASET}_maxsources_3_topk_2.json"),
            os.path.join(data_dir, f"{CONFIG}_{DATASET}_maxsources_3_topk_5.json"),
            os.path.join(data_dir, f"{CONFIG}_{DATASET}_maxsources_6_topk_1.json"),
            os.path.join(data_dir, f"{CONFIG}_{DATASET}_maxsources_6_topk_2.json"),
            os.path.join(data_dir, f"{CONFIG}_{DATASET}_maxsources_6_topk_5.json"),
            os.path.join(data_dir, f"{CONFIG}_{DATASET}_maxsources_None_topk_1.json"),
            os.path.join(data_dir, f"{CONFIG}_{DATASET}_maxsources_None_topk_2.json"),
        ]
        
        file_name_mapping = {
            f"{CONFIG}_{DATASET}_maxsources_1_topk_1.json": "Top 1, 1 Chunk",
            f"{CONFIG}_{DATASET}_maxsources_1_topk_2.json": "Top 1, 2 Chunks",
            f"{CONFIG}_{DATASET}_maxsources_1_topk_5.json": "Top 1, 5 Chunks",
            f"{CONFIG}_{DATASET}_maxsources_2_topk_1.json": "Top 2, 1 Chunk",
            f"{CONFIG}_{DATASET}_maxsources_2_topk_2.json": "Top 2, 2 Chunks",
            f"{CONFIG}_{DATASET}_maxsources_2_topk_5.json": "Top 2, 5 Chunks",
            f"{CONFIG}_{DATASET}_maxsources_5_topk_1.json": "Top 5, 1 Chunk",
            f"{CONFIG}_{DATASET}_maxsources_5_topk_2.json": "Top 5, 2 Chunks",
            f"{CONFIG}_{DATASET}_maxsources_5_topk_5.json": "Top 5, 5 Chunks",
            f"{CONFIG}_{DATASET}_maxsources_None_topk_1.json": "All, 1 Chunk",
            f"{CONFIG}_{DATASET}_maxsources_None_topk_2.json": "All, 2 Chunks",
        }
    elif CONFIG == "global":
        plot_file_name = f"{CONFIG}_{DATASET}_relevant_context.png"
        files_to_process = [
            os.path.join(data_dir, f"{CONFIG}_{DATASET}_topk_1.json"),
            os.path.join(data_dir, f"{CONFIG}_{DATASET}_topk_2.json"),
            os.path.join(data_dir, f"{CONFIG}_{DATASET}_topk_5.json"), 
            os.path.join(data_dir, f"{CONFIG}_{DATASET}_topk_10.json"),
            os.path.join(data_dir, f"{CONFIG}_{DATASET}_topk_15.json")
        ]
        
        file_name_mapping = {
            f"{CONFIG}_{DATASET}_topk_1.json": "Top 1 Chunk",
            f"{CONFIG}_{DATASET}_topk_2.json": "Top 2 Chunks",
            f"{CONFIG}_{DATASET}_topk_5.json": "Top 5 Chunks", 
            f"{CONFIG}_{DATASET}_topk_10.json": "Top 10 Chunks",
            f"{CONFIG}_{DATASET}_topk_15.json": "Top 15 Chunks"
        }
    else:
        raise ValueError("Invalid configuration")


    plot_relevant_context_summary(files_to_process, plots_dir, file_name_mapping, plot_file_name)