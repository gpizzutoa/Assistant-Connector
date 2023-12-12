from openai import OpenAI
import time
import sys
sys.path.append('C:/Users/Gianfranco Pizzuto/OneDrive/Escritorio/Assistant_1')

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

def main():
    # Create a new thread for the entire session
    thread = client.beta.threads.create()
    last_index = 0  # Keep track of the last message index

    while True:
        # Read user input from command line
        user_input = input("Enter your message (type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        # Submit user message to the same thread
        run = submit_message(assistant_id, thread, user_input)

        # Wait for response and pretty print
        run = wait_on_run(run, thread)
        all_messages = list(get_response(thread))

        # Print only new messages since the last index
        new_messages = all_messages[last_index:]
        pretty_print(new_messages)

        # Update the last index
        last_index = len(all_messages)

# Check if the script is run directly (and not imported)
if __name__ == "__main__":
    main()

