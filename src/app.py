import streamlit as st
import requests

def wide_space_default():
    st.set_page_config(
        layout="wide",
        page_title="Search Free Courses",
    )

wide_space_default()

css_for_text = """
<style>
    p, li, strong, ul {
        font-size: 18px !important;
    }

    h1 {
        font-size: 28px;
    }

    .text {
        font-size: 22px !important
    }
</style>
"""

# Applying the custom CSS for styling
st.markdown(css_for_text, unsafe_allow_html=True)

st.header("Analytics Vidya Free Courses", anchor=False)
# desc = st.write("This is a search engine to search among free courses of Analytics Vidya")

def sending_keyword(keyword):
    response =  requests.get("http://0.0.0.0:8000/get_courses", params={"keyword": keyword}).json()
    return response['results']

response = "This ia a search engine project created for Analytics Vidya Free Courses. The project helps users to type any keyword related to the free courses they are looking for."

with st.sidebar:

    keyword = st.text_input("Enter course keyword:")

    submit_button = st.button("Press me")

    if keyword or submit_button:
        st.write("Your entered keyword is ", keyword)
        st.snow()

if keyword or submit_button:

        response = sending_keyword(keyword)

st.markdown(response, unsafe_allow_html=True)