

# 💊 Mosadex Pharmacy Chatbot Demo 👩‍⚕️
[duckyai.mosadexchatbotdemo.app](https://mosadexchatbotdemo.streamlit.app/?access_key=9bdc3ed9-4837-4c73-925c-dd6eb1850601)
# Pharmacy Assistant Chatbot Demo

Created for the Software Engineering class, this demo showcases the capabilities of a sophisticated chatbot system designed to assist in the pharmacy industry by interacting with patients and pharmacists alike.

## How it Works

1. Interacts with patients through a chat interface for queries regarding pharmacy records or services.
2. Retrieves and modifies patient records as per user requests.
3. Notifies pharmacists about updates or critical alerts through the system.
4. Identifies urgent user messages and activates warning notifications for immediate attention.

## What Can It Do?

- **Retrieve Information**: Works with serialized record data and unorganized text data like pharmacy web pages.
- **Modify Records**: Can add new data or change existing record information upon request.
- **Pharmacist Notifications**: Capable of sending notifications to pharmacists with necessary updates or messages.
- **Warning System**: Automatically sends alerts in response to critical messages to ensure prompt attention.


## Installation

To get started with the Pharmacy Assistant Chatbot:

1. **Clone the repository**:
    ```
    git clone https://github.com/yourgithub/pharmacy-assistant-chatbot.git
    ```

2. **Set up a virtual environment** and activate it:
    - **MacOS/Linux**:
        ```
        python3 -m venv venv && source venv/bin/activate
        ```
    - **Windows**:
        ```
        python -m venv venv && venv\Scripts\activate
        ```

3. **Install dependencies**:
    ```
    pip install -r requirements.txt
    ```

4. **Run the application**:
    ```
    streamlit run app.py
    ```
