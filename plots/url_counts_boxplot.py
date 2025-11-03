import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

def plot_url_counts(dataset_name):
    """
    Generates a boxplot of the number of successful URL downloads for each question in a dataset.

    Args:
        dataset_name (str): The name of the dataset (e.g., 'hotpotqa').
    """
    data_dir = os.path.join('data', 'docling', dataset_name, 'downloaded_files')
    if not os.path.isdir(data_dir):
        print(f"Error: Directory not found for dataset '{dataset_name}'")
        return

    question_dirs = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d)) and d.startswith('Q_')]

    url_counts = []
    for q_dir in question_dirs:
        q_path = os.path.join(data_dir, q_dir)
        num_files = len([f for f in os.listdir(q_path) if os.path.isfile(os.path.join(q_path, f)) and f != 'retrieved_info.json'])
        url_counts.append(num_files)

    if not url_counts:
        print(f"No data found for dataset '{dataset_name}'")
        return

    df = pd.DataFrame({'url_count': url_counts})

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, y='url_count')
    plt.title(f'Number of Successful URL Downloads per Question for {dataset_name}')
    plt.ylabel('Number of URLs')
    
    output_path = os.path.join('plots', f'{dataset_name}_url_counts_boxplot.png')
    plt.savefig(output_path)
    print(f"Boxplot saved to {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a boxplot of URL download counts for a dataset.')
    parser.add_argument('dataset_name', type=str, help='The name of the dataset (e.g., hotpotqa)')
    args = parser.parse_args()

    plot_url_counts(args.dataset_name)
