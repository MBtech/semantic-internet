import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# List of JSON files to compare
json_files = [
    '/Users/bilal/workspace/semantic-internet/data/search_results/triviaqa_500_top20.json',
    '/Users/bilal/workspace/semantic-internet/data/search_results/hotpotqa_500_top20.json',
    '/Users/bilal/workspace/semantic-internet/data/search_results/truthfulqa_500_top20.json'
]

# Create a list to store the data
data = []

# Iterate through each JSON file
for file_path in json_files:
    with open(file_path, 'r') as f:
        try:
            content = f.read()
            if not content:
                continue
            json_data = json.loads(content)
            file_name = os.path.basename(file_path)
            for item in json_data:
                if 'unique_uri_count' in item:
                    data.append({
                        'Search Dataset': file_name,
                        'Unique URI Count': item['unique_uri_count']
                    })
        except json.JSONDecodeError:
            # Handle cases where the file is not a valid JSON object
            continue

# Create a DataFrame from the collected data
df = pd.DataFrame(data)

# Create the boxplot
plt.figure(figsize=(12, 8))
sns.boxplot(x='Search Dataset', y='Unique URI Count', data=df)
plt.xticks(rotation=45, ha='right')
plt.title('Distribution of Unique URI Counts')
plt.tight_layout()

# Save the plot
plt.savefig('/Users/bilal/workspace/semantic-internet/plots/unique_uri_counts_boxplot.png')