import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

st.title('Chronicle')
st.subheader('Your friendly researcher & content writer agent')

st.text_input('Enter the topic',
              label_visibility=st.session_state.visibility,
              placeholder="Eg. Generate a blog post about Generative AI in healthcare",
              key="topic_input")
