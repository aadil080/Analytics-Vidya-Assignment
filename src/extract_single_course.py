import requests
from bs4 import BeautifulSoup
import re

def clean_newlines(text):
    """
    Funtion to clean up newline and whitespace characters in a given text.

    Args:
        text (str): The input text string to clean.

    Returns:
        str: The cleaned text with normalized whitespace.
    """
    # Replacing consecutive whitespace/newlines with a single space using Regular Expression pattern
    cleaned_text = re.sub(r'\s+', ' ', text)
    
    # Removing leading and trailing spaces
    cleaned_text = cleaned_text.strip()
    
    return cleaned_text


def extract_course_details(course_url):
    """
    Extract the details of a course from its webpage.

    This function fetches the webpage of a single course using its URL and parses the HTML 
    to extract the following details:
        1. Course title.
        2. Course description.
        3. Course curriculum (it is a list of items/topics).

    Args:
        course_url (str): The URL of the course webpage.

    Returns:
        tuple: A tuple containing:
            - title (str): The title of the course (or 'N/A' if not found).
            - description (str): The description of the course (or 'N/A' if not found).
            - curriculum (list of str): A list of curriculum items (or ['N/A'] if not found).

    """
    # Fetching the course webpage content
    response = requests.get(course_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting the course title
    title = (
        soup.find('h1', class_='section__heading').text.strip()
        if soup.find('h1', class_='section__heading') else 'N/A'
    )
    title = clean_newlines(title)

    # Extractintg  the course description
    description = (
        soup.find('div', class_='rich-text__container').text.strip()
        if soup.find('div', class_='rich-text__container') else 'N/A'
    )
    description = clean_newlines(description)

    # Extracting the curriculum of course (assuming the curriculum is in a list format)
    curriculum = []
    curriculum_section = soup.find('div', class_='course-curriculum__container')
    if curriculum_section:
        items = curriculum_section.find_all('h5')
        for idx, item in enumerate(items):
            if idx == 10: # Only Showing maximum 10 curriculums to the users
                text = "...and many more"
                curriculum.append(text)
                break
            text = clean_newlines(item.text.strip())
            curriculum.append(text)
    else:
        curriculum = ['No available for this course']


    return title, description, curriculum
