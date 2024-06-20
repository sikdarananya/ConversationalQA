import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        return [f"Error: {str(e)}"]

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Chatbot", layout="centered", initial_sidebar_state="collapsed")
st.title("Gemini Chatbot")

# Custom CSS for better styling
st.markdown("""
    <style>
        .main {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
        }
        .chat-container {
            background-color: white;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .user-message {
            background-color: #e0f7fa;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 5px;
        }
        .bot-message {
            background-color: #ffe0b2;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 5px;
        }
        .input-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 10px;
        }
        .input-container input {
            flex: 1;
            margin-right: 10px;
        }
        .clear-button {
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input form
with st.form(key='question_form'):
    st.subheader("Ask a question:")
    input_question = st.text_input("Your question here...")
    submit_button = st.form_submit_button(label='Submit')

# Clear chat history button
if st.button('Clear Chat', key='clear', help='Clear the chat history'):
    st.session_state['chat_history'] = []

# Handle question submission
if submit_button and input_question:
    with st.spinner('Waiting for response...'):
        response = get_gemini_response(input_question)
        st.session_state['chat_history'].append(("You", input_question))
        for chunk in response:
            st.session_state['chat_history'].append(("Bot", chunk.text))

# Display chat history
st.subheader("Chat History")
chat_container = st.container()
with chat_container:
    for role, text in st.session_state['chat_history']:
        if role == "You":
            st.markdown(f"<div class='chat-container user-message'><strong>{role}:</strong> {text}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-container bot-message'><strong>{role}:</strong> {text}</div>", unsafe_allow_html=True)
