import streamlit as st
from openai import OpenAI
import time
import sys
sys.path.append('C:/Users/Gianfranco Pizzuto/OneDrive/Escritorio/Assistant_1')
# Include other necessary imports

# Assuming other functions (submit_message, get_response, wait_on_run, etc.) are defined here
from constants import client, assistant_id

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

# Pretty printing helper
def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()

# Waiting in a loop
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def send_message():
    user_input = st.session_state.user_input
    if user_input:
        # Display user message
        st.session_state['messages'].append(f"You: {user_input}")

        # Submit user message to the thread
        run = submit_message(assistant_id, st.session_state['thread'], user_input)

        # Wait for response
        run = wait_on_run(run, st.session_state['thread'])

        # Get and process the response
        new_messages = get_response(st.session_state['thread'])
        # Convert SyncCursorPage to a list and get the last message
        messages_list = list(new_messages)
        if messages_list:
            last_message = messages_list[-1]
            if last_message.role == 'assistant':
                st.session_state['messages'].append(f"Bot: {last_message.content[0].text.value}")

        # Clear the input box
        st.session_state.user_input = ""

def main():
    # Initialize session state for storing messages if not already set
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # Initialize thread only once
    if 'thread' not in st.session_state:
        st.session_state['thread'] = client.beta.threads.create()

    # Chat display area
    st.write("Chat:")
    chat_container = st.container()
    with chat_container:
        for i, message in enumerate(st.session_state['messages']):
            st.text_area("Message", value=message, height=50, disabled=True, key=f"message_{i}", label_visibility="collapsed")

    # User input
    st.text_input("Enter your message", key="user_input", on_change=send_message, label_visibility="collapsed")


if __name__ == "__main__":
    st.title("Chatbot")
    main()
