# Import necessary libraries
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import VectorParams, Distance
from qdrant_client.http.models import PointStruct
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from openai import OpenAI
import pandas as pd
import numpy as np
import cohere
from fastapi import FastAPI, Form, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import JSONResponse
import uvicorn
from typing import List
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Set up templates for rendering HTML
templates=Jinja2Templates(directory="templates")

# Add CORS middleware to allow local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Initialize external clients (OpenAI and Cohere)
openai_client = OpenAI(api_key="YOUR-OPENAI-API-KEY")
cohere_api_key = "YOUR-COHERE-API-KEY"
co = cohere.Client(cohere_api_key)

# Initialize Qdrant vector database client
qdrant_client = QdrantClient("localhost", port=6333)

search_result = qdrant_client.search(collection_name="test_collection_2", query_vector=[0.27], limit=4)
print(search_result)

#defining the fast api endpoints for each function
@app.get("/")
async def read_root(request: Request):
    # You can pass variables to the template from here
    return templates.TemplateResponse("index.html", {"request": request})

class RerankRequest(BaseModel):
    query_text: str
    documents: List[str]

#starting with search_result end point
@app.post("/search")
async def vector_search(request: Request, query_text: str = Form(...)):
    #taking search input
    #searching
    embedding_model = "text-embedding-3-small"
    try:
        #making embedding of query
        query_vector=openai_client.embeddings.create(
          input=[query_text],
          model=embedding_model,
        ).data[0].embedding
        print("query embedding generated")
        search_result = qdrant_client.search(
        collection_name="vol1_collection",
        query_vector=query_vector,
        limit='10',
        )
        print(type(search_result))
        if not search_result: 
           print("Search failed")
        else:
            # Process the search results
            results_text = [point.payload['main_speaker'] + " : " + point.payload['text'] for point in search_result]
            print(results_text)
        return JSONResponse(content={"results": results_text})
    except Exception as e:
       return templates.TemplateResponse("index.html", {"request": request, "results": "Vector Search Error"})

# Endpoint: Rerank results using Cohere
@ app.post("/rerank")
async def rerank_results(rerank_request: RerankRequest):
    query_text = rerank_request.query_text
    documents = rerank_request.documents
    print("Received documents:", documents)  # Debugging statement

    try:
        rerank_response = co.rerank(
            query=query_text,
            documents=documents,
            top_n=5,
            model='rerank-multilingual-v2.0'
        )
        print("rerank successful")
        print("rerank_response:", rerank_response)

        # Process and return reranked results
        rerank_results_list = []
        for hit in rerank_response.results:
            rerank_results_list.append({
                "index": hit.index,
                "text": documents[hit.index],  # Retrieve text using the index
                "relevance_score": hit.relevance_score
            })
        print("rerank_results_list:", rerank_results_list)

        # Return reranked results as JSON
        return JSONResponse(content={"reranked_results_list": rerank_results_list})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(content={"message": str(e)}, status_code=400)

# Run the server locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)