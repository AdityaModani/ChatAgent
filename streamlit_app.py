import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title of the app
st.title("Your Health Assistant")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Collect user input for symptoms
user_input = st.chat_input("Describe your symptoms here...")

# Function to get a response from OpenAI with health advice
def get_response(prompt):
    # System prompt to keep assistant within the medical domain
    system_message = {
        "role": "system",
        "content": (
            "You are a helpful and knowledgeable health assistant. "
            "Only provide information, guidance, or general advice related to medical and health topics. "
            "If the user asks something outside the medical domain, politely decline to answer by saying something like: "
            "'I'm here to help with health-related questions. Could you please share a medical concern?'"
        )
    }

    # Build the message history with the system prompt at the start
    messages = [system_message] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ] + [{"role": "user", "content": prompt}]

    # Get the assistant's response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response.choices[0].message.content

# Process and display response if there's input
if user_input:
    # Append user's message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant's response
    assistant_prompt = f"User has reported the following symptoms: {user_input}. Provide a general remedy or advice."
    assistant_response = get_response(assistant_prompt)

    # Append assistant's message to history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
