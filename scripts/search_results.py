import json
from urllib.parse import urlparse

from pydantic import BaseModel
from utils.search import search
from google import genai
import os
from google.genai.types import HttpOptions
import sys 

# Adjust these constants
MODEL = "gemini-2.5-flash"   # switch to a model available to your project
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "kaust-pf2023-marco")

# Instantiate client (Vertex AI mode)
client = genai.Client(http_options=HttpOptions(api_version="v1"), vertexai=True, location=LOCATION, project=PROJECT)


class TransformedQuery(BaseModel):
    query: str


query_prompt = """
Take the user query and transform it into query for a search engine that would provide the best results to find an answer

User Query:
{user_query}
"""

def call_model(query, prompt=query_prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt.format(user_query=query),
        config={
            "response_mime_type": "application/json",
            "response_schema": TransformedQuery,
            "temperature": 0.0
        },
    )   
    return response.parsed

def get_trivia_questions(n: int=500):
    json_data = json.load(open("/Users/bilal/Downloads/triviaqa-rc/qa/web-dev.json"))

    data = json_data["Data"]

    questions = []
    for entry in data[:n]:
        question = entry["Question"]    
        questions.append(question)
    return questions

def get_news_questions():
    questions = json.load(open("data/news_questions.json"))
    return questions


def get_truthfulqa_questions(n: int=500):
    # read jsonl
    questions = []
    i = 0
    with open("data/truthful_qa.jsonl", "r") as f:
        for line in f:
            data = json.loads(line)
            questions.append(data["question"])
            i += 1
            if i == n:
                break
    return questions

def get_hotpotqa_questions(n: int=500):
    # read jsonl
    questions = []
    i = 0
    with open("data/hotpotqa.jsonl", "r") as f:
        for line in f:
            data = json.loads(line)
            questions.append(data["question"])
            i += 1
            if i == n:
                break
    return questions
        

# Get datasetname from cli args
datasetname = sys.argv[1]


# Select questions based on dataset name
if datasetname == "triviaqa":
    questions = get_trivia_questions()
elif datasetname == "hotpotqa":
    questions = get_hotpotqa_questions()
elif datasetname == "truthfulqa":
    questions = get_truthfulqa_questions()
elif datasetname == "news":
    questions = get_news_questions()
else:
    raise ValueError("Invalid dataset name")

print(f"Total questions: {len(questions)}")

MAX_SEARCH_RESULTS = 20

rephrase = False
search_results = []
for question in questions:
    if rephrase:
        rephrased_question = call_model(question).query
        print(question)
        print(rephrased_question)
    else:
        rephrased_question = question

    results = []
    try:
        results = search(rephrased_question, max_results=MAX_SEARCH_RESULTS)
    except Exception as e:
        print(e)

    uris = []
    full_urls = []
    for result in results:        
        parsed_uri = urlparse(result["href"])
        full_urls.append(result["href"])
        uris.append(parsed_uri.netloc)
    
    print(f"Total URIs: {len(uris)}")
    unique_uris = list(set(uris))
    print(f"Unique URIs: {len(unique_uris)}")
    
    from collections import Counter
    uri_counts = Counter(uris)
    # print(uri_counts)

    search_results.append({"question": question, "url": full_urls, "unique_uri_count": len(unique_uris)})

# json.dump(search_results, open("data/news_search_results.json", "w"))
json.dump(search_results, open(f"data/search_results/{datasetname}_500_top{MAX_SEARCH_RESULTS}.json", "w"))