from google import genai

context_prompt = """
<document> 
{document} 
</document> 
Here is the chunk we want to situate within the whole document 
<chunk> 
{chunk_content} 
</chunk> 
Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else. 
"""


def get_context_with_gemini(document, chunk_content):
    """
    Generates a short, succinct context for a given chunk within a document
    using the Gemini generative AI model.

    Args:
        document (str): The entire document content.
        chunk_content (str): The specific chunk of text to contextualize.

    Returns:
        str: A short, succinct context for the chunk.
    """
    client = genai.Client(
        vertexai=True,
        project="kaust-pf2023-marco",
        location="global",
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=context_prompt.format(document=document, chunk_content=chunk_content),
    )
    print(response.text)
    return response.text
