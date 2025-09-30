import json
import logging
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

from semantic_resolver.schemas import InformationSource
from semantic_resolver.enums import Category, License, Topic, ContentType
from semantic_resolver.helpers import call_model

import uvicorn

app = FastAPI()

class QueryParams(BaseModel):
    max_latency: Optional[float] = None
    licenses: Optional[List[License]] = None
    content_type: Optional[List[ContentType]] = None
    quality: float = None
    trust: float = None
    max_results: int = 10
    language: str = "en"


class QueryRequest(BaseModel):
    query: str
    params: QueryParams
    

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logging.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.post("/query")
async def resolve_query(request: QueryRequest):
    """
    Resolves a query using a specified resolver.
    """

    query = request.query 
    results = call_model(query)
    category: Category = results.category
    topic: Topic = results.topic
    print(category, topic)

    try:
        with open(json_file_path, "r") as f:
            registered_sources_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        registered_sources_data = []

    all_sources = [InformationSource(**data) for data in registered_sources_data]
    
    params = request.params
    
    filtered_sources = []
    for source in all_sources:
        # Category filter
        if source.category != category:
            print("Category mismatch")
            print(category, source.category)
            continue

        if topic not in source.scope.topics:
            print("Topic mismatch")
            print(topic, source.scope.topics)
            continue

        # Language filter
        if params.language and source.scope.languages and params.language not in source.scope.languages:
            print("Language mismatch")
            print(params.language, source.scope.languages)
            continue
            
        # License filter
        if params.licenses and source.content.license and source.content.license not in params.licenses:
            print("License mismatch")
            print(params.licenses, source.content.license)
            continue

        # Content type filter
        if params.content_type and source.content.content_types and not any(content_type in source.content.content_types for content_type in params.content_type):
            print("Content type mismatch")
            print(params.content_type, source.content.content_types)
            continue
        
        # Latency filter
        if params.max_latency and source.performance and source.performance.worst_case_latency_ms:
            if source.performance.worst_case_latency_ms > params.max_latency:
                print("Latency mismatch")
                print(params.max_latency, source.performance.worst_case_latency_ms)
                continue

        # Trust filter
        if params.trust and source.relevance and source.relevance.trust_score:
            if source.relevance.trust_score < params.trust:
                print("Trust mismatch")
                print(params.trust, source.relevance.trust_score)
                continue

        filtered_sources.append(source)

    # Limit results
    results = filtered_sources[:params.max_results]
    
    # Convert to dicts for JSON response
    return [source.model_dump() for source in results]
    


@app.post("/register")
async def register_source(source: InformationSource):
    """
    Registers a new information source with the resolver.
    """
    # Convert the InformationSource object to a dictionary
    source_data = json.loads(source.model_dump_json())

    # Load existing sources if the file exists, otherwise initialize an empty list
    try:
        with open(json_file_path, "r") as f:
            registered_sources = json.load(f)
    except FileNotFoundError:
        registered_sources = []
    except json.JSONDecodeError:
        # Handle case where file is empty or contains invalid JSON
        registered_sources = []

    # Add the new source to the list
    registered_sources.append(source_data)

    # Write the updated list back to the JSON file
    with open(json_file_path, "w") as f:
        json.dump(registered_sources, f, indent=4)

    return {"message": f"Information source '{source.name}' registered successfully."}


if __name__ == "__main__":
    # Define the path to the JSON file
    json_file_path = "registered_sources.json"
    uvicorn.run(app, host="0.0.0.0", port=8888)