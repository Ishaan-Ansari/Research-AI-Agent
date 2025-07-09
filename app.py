import streamlit as st
from dotenv import load_dotenv

from main import main

load_dotenv()

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

if "blog_post" not in st.session_state:
    st.session_state.blog_post = ""


st.title('Chronicle')
st.subheader('Your friendly researcher & content writer agent')

topic = st.text_input('Enter the topic',
                      label_visibility=st.session_state.visibility,
                      placeholder="Eg. Generate a blog post about Generative AI in healthcare",
                      key="topic_input")

if st.button("Let's go"):
    if topic:
        with st.spinner('Generating your post... This might take a few moment.'):
            try:
                st.session_state.blog_post = main(topic)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.session_state.blog_post = ""
    else:
        st.warning('Please enter a topic')

if st.session_state.blog_post:
    st.subheader('Generated Post')
    st.markdown(st.session_state.blog_post)
