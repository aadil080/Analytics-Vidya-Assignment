from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

from dotenv import load_dotenv

def creating_pinecone_index(embedding, index_name):
    return PineconeVectorStore(embedding=embedding, index_name=index_name)

def retrieve_response_from_pinecone(keyword, k=5):
    """
    Retrieves the most similar responses from the Pinecone index based on the given query.

    Args:
        query (str): The input query used to search the Pinecone index for vectors.
        k (int, optional): Indicates top results to choose. Default is 5.

    Returns:
        list: A list of results containing the most similar vectors from the Pinecone index.
    """
    
    results = pinecone_index.similarity_search(keyword, k=k)
    return results

def response_generator(keyword):
    """
    Generates a response to the given query by retrieving relevant information from the Pinecone index and invoking 
    a processing chain with llm.

    Args:
        query (str): The user's input or question that will be used to retrieve relevant information and generate a response.

    Returns:
        str: The generated response to the query, either based on the retrieved information or an error messageif the process fails.
    """
    
    try:
        results = retrieve_response_from_pinecone(keyword, 5)
        print("results", results)

        # Generating a response by invoking the chain with retrieved content and the original query
        answer = chain.invoke(input={"keyword": keyword, "details": results})
    except Exception as e:
        # Returning an error message if any exception occurs
        answer = f"Sorry, I am unable to find the answer to your query. Please try again later. The error is {e}"
    
    return answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    
    return "HELLO"

@app.get("/get_courses")
def get_courses(keyword: str):
    if keyword.strip() == "":
        return JSONResponse(content={"results": "Please provide a valid keyword to search for the courses and upscale your knowledge."})
    else:
        print("Keyword to searh: ", keyword)
        results = response_generator(keyword)
        return JSONResponse(content={"results": results})


if __name__ == "__main__":
    load_dotenv()
    
    embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    llm = GoogleGenerativeAI(model="gemini-1.5-flash")

    index_name = "analytics-vidya-free-courses"

    pinecone_index = creating_pinecone_index(embedding, index_name)

    template = ChatPromptTemplate([
        ("system", "You are a search engine for finding free courses from Analytics Vidya. Course details will be provided to you"),
        ("system", "You will be provided with course title, course link, description and curriculum. Show the curriculum in a bullet points format"),
        ("system", "Handle the details wisely and give the output in a proper format. Respond only with the course details in a tabular or descriptive markdown format as it suites"),
        ("human", "Give me some detail related to this keyword : {keyword}"),
        ("human", "These are the details of courses : {details}")
    ])

    # Setting up the document processing chain for response generation based on retrieved documents
    chain = create_stuff_documents_chain(llm, template, document_variable_name="details")

    # Starting the FastAPI server with Uvicorn, accessible at 0.0.0.0 on port 8000
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
