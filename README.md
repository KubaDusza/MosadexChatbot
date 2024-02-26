

# 🦆 Ducky Chatbot 🐤
[duckyai.streamlit.app](https://duckyai.streamlit.app/?access_key=bbe22d09-e2dc-40ce-8617-82421a285b05)
An AI assistant created to be helpful, harmless, and honest. Just like a friendly duck! *quack!*

This chatbot allows users to upload documents and chat with the bot to get information from the documents. The bot will search the uploaded documents and use relevant excerpts to answer your questions.

## How it works *quack!*

1. Upload PDF documents using the file uploader button
2. Type a question in the chat interface
3. The bot will search the documents and try to find the best answer
4. You can also ask it general questions

## What can it do?
- Take in multiple PDFs
- Answer general and detailed questions to the best of its duck abilities.
- Provide context and excerpts from uploaded documents
- your emoji will be based on the emotion of the message!

## Technologies used
This chatbot is built using:

- Streamlit for the web interface
- Langchain for NLP features:
    - text splitting
    - embedding
    - vectorizing, etc.
- Transformers and Huggingface API for the emoji emotion display
- OpenAI API for embeddings and the LLM

## TODOs
- Add OCR support
- Support additional file formats like docx, txt, csv, xslx etc
- Add multiprocessing when vectorizing document text
- Save user messages and session state per user
- Improve information extraction/retrieval

## Installation
you can use it on [duckyai.streamlit.app](https://duckyai.streamlit.app/?access_key=bbe22d09-e2dc-40ce-8617-82421a285b05) or host it by yourself! it's so easy!

1. Clone the repo
2. Create a virtualenv and activate:
    - on MacOS/Linux:
        python3 -m venv myenv && source myenv/bin/activate
    - on Windows:
        python -m venv myenv && myenv\Scripts\activate
 
4. Install dependencies: pip install -r requirements.txt
5. Create a credentials file in the .streamlit directory and add OpenAI API key
6. change the REMOVE_RESTRICTIONS flag in the constants.py to True
7. Run the app: streamlit run app.py

So come on and give it a quack! The friendliest chatbot around won't quack you up but will do its best to help out. 🦆🐤
