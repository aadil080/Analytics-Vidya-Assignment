from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

import time
import os
from dotenv import load_dotenv

from extract_all_courses import scrape_all_courses

def creating_pinecone_index(embedding):
    """
    Creates a Pinecone index using the provided embedding model.

    Args:
        embedding (object): The embedding model or function used to generate vector embeddings.

    Returns:
        PineconeVectorStore: An instance of Pinecone index where the vectors can be processed.
    """
    
    index = PineconeVectorStore(embedding=embedding)
    return index

def convert_into_documents(all_course_data):
    """
    Converting a list of courses' data dictionaries into a list of Langchain Document objects.

    Each course data dictionary contains the following data:
        - 'title' (str): The title of the course.
        - 'description' (str): A brief description of the course.
        - 'curriculum' (list of str): A list of curriculum items/topics covered in the course.

    Args:
        all_course_data (list of dict): It is a list where each element is a dictionary that contains course information.

    Returns:
        list of Document: A list of Document objects, each one represents a course.
    """
    documents = []

    for course_data in all_course_data:

        # Extractin each course details with default empty values if keys are missing
        title = course_data.get("title", "")
        url = course_data.get("url", "")
        description = course_data.get("description", "")
        curriculum = " \n ".join(course_data.get("curriculum", []))

        # Combining the course details into a single text
        full_text = f"Title: {title} ; Web url: {url} Description: {description} ; Curriculum: {curriculum}"

        # Creation of a Document object with the combined text and metadata
        course_document = Document(
            page_content=full_text,
            metadata={"url": url}
        )

        # Appending the course Document object to the list
        documents.append(course_document)

    return documents


def uploading_document_to_pinecone(all_courses):
    """
    Upload all course data to a Pinecone index after converting it into a suitable format.

    Args:
        all_courses (list of dict): A list where each element is a dictionary containing course information.
    """
        
    # Convert course data into Document objects
    final_course_data = convert_into_documents(all_courses)

    print("Deleting file")
    try:
        # Deleting all existing data from the Pinecone index
        pinecone_index.delete(delete_all=True)
        time.sleep(5)
    except Exception as e:
        print(f"Namespace is already empty")

    print("Uploading File to Pinecone")
    
    # Upload the chunked data to Pinecone index
    pinecone_index.from_documents(final_course_data, embedding, index_name=index_name)
    print("Document Uploaded to Pinecone")


if __name__ == "__main__":
    """
    Main function to initialize and execute the pipeline for scraping courses, 
    generating embeddings, and uploading course data to a Pinecone index.

    Steps:
        1. Load environment variables from a `.env` file.
        2. Initializing the google's embedding model for creating document vectors.
        3. Defining the Pinecone index's name and creating its Pinecone index.
        5. Scrape all courses from the specified base URL.
        6. Upload the scraped course data to the Pinecone index.

    """
    # Load all environment variables from .env file
    load_dotenv()

    # Initializing the embedding model for creating document vectors
    embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    # The Pinecone index name for storing document embeddings
    index_name = "analytics-vidya-free-courses"

    # Creation of the Pinecone index using the embedding model
    pinecone_index = creating_pinecone_index(embedding)

    # Defining the base URL for scraping the courses' list
    base_url = "https://courses.analyticsvidhya.com/collections/courses"

    # Scraping all courses available on the base URL
    all_courses = scrape_all_courses(base_url)

    # Uploading the scraped courses' data to the Pinecone index
    uploading_document_to_pinecone(all_courses)
