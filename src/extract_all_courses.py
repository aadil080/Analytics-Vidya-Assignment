import requests
from bs4 import BeautifulSoup
import time

from extract_single_course import extract_course_details

def scrape_courses_from_page(page_url):
    """
    Scrapes all courses details from a given main page URL.

    Args:
        page_url (str): The URL of the main page containing the list of courses.

    Returns:
        list of dict: A list of dictionaries where each dictionary contains:
            - 'title' (str): The title of the course.
            - 'url' (str): Web access url of the course.
            - 'description' (str): The description of the course.
            - 'curriculum' (list of str): A list of curriculum items/topics.

    """
    # Fetch the main page
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all course list items
    course_items = soup.find_all('li', class_='products__list-item')

    course_details = []
    for item in course_items:
        # Extracting the course link
        course_link_tag = item.find('a', class_='course-card')
        if course_link_tag:
            course_link = course_link_tag['href']
            full_course_url = 'https://courses.analyticsvidhya.com' + course_link

            # Extracting course details from the individual course page using another function
            title, description, curriculum = extract_course_details(full_course_url)

            # Appending the course details to the list of dictionaries
            course_details.append({
                'title': title,
                'url': full_course_url,
                'description': description,
                'curriculum': curriculum
            })

    return course_details


def scrape_all_courses(base_url):
    """
    Scraping all pages across multiple pages from a given base URL.

    Args:
        base_url (str): The base URL of the courses page, where pagination is handled via a query parameter.

    Returns:
        list of dict: A list of dictionaries where each dictionary contains:
            - 'title' (str): The title of the course.
            - 'url' (str): Web access url of the course.
            - 'description' (str): The description of the course.
            - 'curriculum' (list of str): A list of curriculum items/topics.

    """
    page_number = 1
    all_courses = []

    while True:
        try:
            print(f"Scraping page {page_number}...")
            # Constructing the URL for the current page
            page_url = f"{base_url}?page={page_number}"
            
            # Scraping all courses from the current page using another function
            courses_on_page = scrape_courses_from_page(page_url)

            if not courses_on_page:  # Exit loop if no more courses are found
                break

            # Adding the courses from the current page to the aggregated list for storage.
            all_courses.extend(courses_on_page)

            # Increment the page number for the next page
            page_number += 1

            # Adding a delay to avoid overwhelming the server for any ddos attack
            time.sleep(2)
        except Exception as e:
            print(f"An exception occurred: {e}")
            break

    return all_courses



if __name__ == "__main__":
    """
    Main script to scrape course details from the Analytics Vidhya courses page.

    Steps included:
    1. Setting up the base URL for the course list.
    2. Scraping all courses across multiple pages using `scrape_all_pages`.
    3. Printing the details like title, description, curriculum of each course.
    """
    # Base URL of the course list
    base_url = "https://courses.analyticsvidhya.com/collections/courses"

    # Scrape all courses
    all_courses = scrape_all_courses(base_url)

    # Printing extracted details of each course
    for idx, course in enumerate(all_courses, 1):
        print(f"Course {idx}:")
        print(f"Title: {course['title']}")
        print(f"Description: {course['description']}")
        print(f"Curriculum: {', '.join(course['curriculum'])}")
        print("-" * 50)

