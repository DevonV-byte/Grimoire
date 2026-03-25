# This file contains the Streamlit frontend for the AutoQuizzer application.
# It allows users to input a topic and receive a quiz on it.
#
# Created: 2026-03-25
# Author: Devon Vanaenrode
# Updated: 2026-03-25

# --- Imports ---
import streamlit as st
import sys
import os

# Adjust path to import from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from RAG_Pipeline.rag_chain import get_quiz_generation_chain

st.markdown("""
<style>
    /* Target the text inside the radio button labels */
    div[role="radiogroup"] label p {
        font-size: 20px !important; 
    }
</style>
""", unsafe_allow_html=True)

# --- Main loop ---
st.title("AutoQuizzer")

topic = st.text_input("Enter the topic you want to be quizzed on:")

if 'quiz' not in st.session_state:
    st.session_state.quiz = None

if st.button("Generate Quiz"):
    if topic:
        with st.spinner("Generating your quiz..."):
            try:
                # Get the chain
                quiz_chain = get_quiz_generation_chain()
                if quiz_chain:
                    # Invoke the chain and store the result
                    st.session_state.quiz = quiz_chain.invoke(topic)
                else:
                    st.error("Failed to initialize the quiz generation chain. Please check the logs.")
            except Exception as e:
                st.error(f"An error occurred while generating the quiz: {e}")
    else:
        st.warning("Please enter a topic first.")

# Display the quiz if it exists in the session state
if st.session_state.quiz:
    st.subheader("Here is your quiz!")
    quiz_data = st.session_state.quiz

    # The prompt seems to generate a list containing a single dictionary.
    if isinstance(quiz_data, list):
        if quiz_data:
            quiz_data = quiz_data[0]
        else:
            st.warning("Generated quiz is empty.")
            quiz_data = {}

    if isinstance(quiz_data, dict):
        if 'quiz_title' in quiz_data:
            st.title(quiz_data['quiz_title'])

        if 'questions' in quiz_data and isinstance(quiz_data['questions'], list):
            for question in quiz_data['questions']:
                if isinstance(question, dict):
                    question_text = question.get('question', 'No question text provided.')
                    question_number = question.get('question_number')
                    options_dict = question.get('options')
                    
                    options_list = []
                    if isinstance(options_dict, dict):
                        options_list = list(options_dict.values())
                    elif isinstance(options_dict, list):
                        for opt in options_dict:
                            if isinstance(opt, dict):
                                options_list.extend(opt.values())

                    if question_text and options_list:
                        question_header = f"### {question_number}. {question_text}" if question_number else f"### {question_text}"
                        st.markdown(question_header)
                        st.radio(
                            "Options", # label
                            options=options_list,
                            key=f"q_{question_number or id(question)}",
                            label_visibility="hidden"
                        )
                else:
                    st.warning(f"Found a question item that is not a dictionary: {question}")
        else:
            st.error("Could not find 'questions' in the quiz, or it's not a list.")
            st.json(quiz_data) # Show raw data for debugging
    else:
        st.error("Generated quiz is not in the expected dictionary format.")
        st.json(quiz_data)
