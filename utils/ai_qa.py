from openai import OpenAI
from pydantic import BaseModel
from openai.types.chat import ChatCompletionMessageParam

class Answer(BaseModel):
    answer: str
    relevant_context_present: bool


openai_client = OpenAI()

def answer(query, context, model="gpt-5-mini"):
    response = openai_client.responses.parse(
    model=model,
    input=[
        {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
        {"role": "user", "content": f"""
            Instructions:
            1. Based on the following context answer the question.
            2. Do not use any other information or your internal knowledge to answer the question.
            3. If required information is not present in the context, reply correspondingly with "Not enough context"
            
            Query:
            {query}
            
            Context:
            {context}"""
        }
    ],
        text_format=Answer,
    )
    # The openai_response object is already parsed into an Answer object due to response_model
    # We can directly return it.
    # If the model couldn't find relevant context, it should set relevant_context_present to False
    # and the answer to "Not enough context" based on the prompt instructions.
    return response.output_parsed