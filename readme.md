# README for Python OpenAI Assistant Script

## Overview
This Python script integrates with OpenAI's API to create a conversational assistant. It manages messaging threads, sends user inputs, and receives responses from the OpenAI assistant. The script is designed for interactive use and includes functions for pretty-printing responses.

## Requirements
- Python 3.x
- `openai` Python package

## Installation
1. Install the OpenAI Python package:
   ```bash
   pip install openai
   ```

2. Clone or download this script to your local machine.

3. Add the file path to your Python system path:
   ```python
   sys.path.append('C:/Users/YourUsername/PathToScript')
   ```

## Configuration
Set your OpenAI API key in the `constants.py` file:
```python
client = OpenAI_API_Client(your_api_key)
```

## Usage
Run the script using Python:
```bash
python main.py
```

You will be prompted to enter your message. After entering a message, the script will handle the communication with the OpenAI API and display the assistant's response.

## Key Functions
- `submit_message`: Submits a message to the OpenAI API.
- `get_response`: Retrieves messages from a thread.
- `create_thread_and_run`: Creates a new thread and submits the initial user message.
- `pretty_print`: Formats and prints messages for readability.
- `wait_on_run`: Waits for the OpenAI API to process a submitted message.
- `main`: Main function to start the conversational assistant.

## Contributing
Contributions to this script are welcome. Please ensure that your code adheres to the project's coding standards and include appropriate tests.

## License
MIT

---

*Note: Replace placeholders like `YourUsername` and `PathToScript` with your actual username and script path. Also, ensure you have a valid OpenAI API key.*
