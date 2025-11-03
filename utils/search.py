from typing import List
from ddgs import DDGS
import time

def search(search_query: str, sites: List[str] = None, max_results=5):
    engine = SearchEngine()
    print(f"Searching for: '{search_query}'")
    results = engine.search(search_query, sites=sites, max_results=max_results)
    # print(results)
    return results

class SearchEngine:
    def search(self, query: str, max_results: int = 5, sites=None) -> str:
        if sites:
            site_string = f"site:{sites[0]}"
            for site in sites[1:]:
                site_string += f" OR site:{site}"
            query = f"{query} {site_string}"
        results = []
        search_results = []
        print(f"Query: {query}")
        for attempt in range(3): # Add 3 retries
            time.sleep(5)
            try:
                search_results = DDGS().text(query, max_results=max_results)
                break # Break out of retry loop if successful
            except Exception as e:
                time.sleep(10)
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == 2: # If all retries fail
                    continue # Continue to the next page
        results.extend(search_results)
        print(results)
        if not results:
            return []
    
        formatted_results = []
        for i, result in enumerate(results):
            formatted_results.append(f"Result {i+1}:")
            formatted_results.append(f"  Title: {result.get('title', 'N/A')}")
            formatted_results.append(f"  URL: {result.get('href', 'N/A')}")
            formatted_results.append(f"  Snippet: {result.get('body', 'N/A')}")
            formatted_results.append("")
        # return "\n".join(formatted_results)
        return results[:max_results]


if __name__ == "__main__":
    engine = SearchEngine()
    search_query = "latest AI research"
    print(f"Searching for: '{search_query}'")
    results = engine.search(search_query)
    print(results)

    search_query_2 = "weather in London"
    print(f"\nSearching for: '{search_query_2}'")
    results_2 = engine.search(search_query_2)
    print(results_2)
