from openai import OpenAI
import time
import sys
sys.path.append('C:/Users/Gianfranco Pizzuto/OneDrive/Escritorio/Assistant_1')

from constants import client, assistant_id

# Rest of your main.py code


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

def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(assistant_id, thread, user_input)
    return thread, run

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
    # Read user input from command line
    user_input = input("Enter your message: ")

    # Create thread and submit user message
    thread, run = create_thread_and_run(user_input)

    # Wait for response and pretty print
    run = wait_on_run(run, thread)
    messages = get_response(thread)
    pretty_print(messages)

# Check if the script is run directly (and not imported)
if __name__ == "__main__":
    main()