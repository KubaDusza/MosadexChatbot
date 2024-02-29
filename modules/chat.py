import json
import stat

import pandas
import streamlit

from imports import *
from constants import *
from utils.emotion_classification import EmotionClassifier
openai.api_key = st.secrets["OPENAI_API_KEY"]


@st.cache_resource(show_spinner=False)
def get_emotion_classifier():
    return EmotionClassifier()


TOOLS = [{
    "type": "function",
    "function": {
        "name": "manipulate_dataframe",
        "description": "Use only when asked to manipulate a record by default do not use it. Modifies a specified field in a DataFrame by setting it to a new value and provides a response to the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "response": {
                    "type": "string",
                    "description": "The response to the user before the operation is performed, informing, what action is being performed, but shortly."
                },
                "row": {
                    "type": "integer",
                    "description": "The index (row number) of the DataFrame where the change is to be applied."
                },
                "column": {
                    "type": "string",
                    "description": "The name of the column in the DataFrame where the change is to be applied."
                },
                "new_value": {
                    "type": "string",
                    "description": "The new value to set for the specified field (cell) in the DataFrame. If you want to set an empty field, use \"None\" "
                }

            },
            "required": ["response", "dataframe", "row", "column", "new_value"]
        }
    }
    },
    {
      "type": "function",
      "function": {
        "name": "notify_pharmacist",
        "description": "Sends a notification message to the pharmacist and provides a predetermined response to the user to confirm the action. User can also request to send this message",
        "parameters": {
          "type": "object",
          "properties": {
            "response": {
              "type": "string",
              "description": "The response to the user after the notification is sent, informing them about the action taken in a brief manner."
            },
            "message": {
              "type": "string",
              "description": "The message to be sent to the pharmacist. This should be clear and concise, providing all necessary information."
            },
            "notification_type": {
              "type": "string",
              "enum": ["warning", "info"],
              "description": "The type of notification to send. Can be either 'warning' for urgent matters or 'info' for informational messages."
            }

          },
          "required": ["message", "response", "notification_type"]
        }
      }
    },
{
  "type": "function",
  "function": {
    "name": "get_pharmacy_opening_hours",
    "description": "Retrieves and displays the opening hours for a specified pharmacy.",
    "parameters": {
      "type": "object",
      "properties": {
        "store_code": {
          "type": "string",
          "description": f"The unique identifier for the pharmacy whose opening hours are to be retrieved. For demonstration purposes, unless a valid id given, use \"GV-001\", or use this dict to find the code: {MOCK_PHARMACY_STORE_IDS} "
        },
        #"day":{
        #    "type": "string",
        #    "description": "The day of which we want the opening hours of. Don't use, if a specific day is not requested"
        #}
      },
      "required": ["store_code"]
    }
  }
}

]







def get_response(messages, model = None, stream = True, temperature = 1.0, tools = None):
    if model is None:
        model = st.session_state["openai_model"]

    return  st.session_state.openai_client.chat.completions.create(
        model=model,
        messages=messages,
        stream=stream,
        temperature=temperature,
        tools = tools)


def display_chat():

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.markdown(message["content"])
            if message.get("function_call") is not None:
                st.markdown(message["function_call"])


def ask_question(container):
    # prompt = st.session_state.prompt
    notifications = None

    prompt = st.chat_input("Ask a question")  # , key="prompt")

    st.session_state.prompts.append(prompt)

    if st.session_state.regenerate:
        last_non_null_text = next((text for text in reversed(st.session_state.prompts) if text is not None), None)

        prompt = last_non_null_text
        st.session_state.regenerate = False


    with container:

        if prompt:
            avatar = get_emotion_classifier().classify(prompt)

            with st.chat_message("user", avatar=avatar):
                st.markdown(prompt)

            st.session_state.messages.append({"role": "user", "content": prompt, "avatar": avatar})

            json_string_record_data = st.session_state.pharmacy_example_record_data.to_json(orient='records')

            docs = [st.session_state.pharmacy_example_text_info, json_string_record_data]

            # st.write(docs)

            notifications = ai_message(docs)

            x = '''any_expanded = False
            for i, column in enumerate(columns):
                if not any_expanded:
                    with column:
                        with st.expander(docs[i].page_content[:10] + "..."):
                            any_expanded = True
                            write_atsize(docs[i].page_content, 12)'''
    return notifications


def notify_pharmacist(function_arguments):
    response = function_arguments['response']
    notification_type = function_arguments['notification_type']
    notification = {notification_type: function_arguments['message']}
    return response, notification




def hanhandle_function_calls(function_name, function_arguments_json, message_placeholder,functioncall_placeholder):
    response = ""
    notifications = None
    if function_name == "manipulate_dataframe":
        st.session_state.pharmacy_example_record_data, response, notifications = manipulate_dataframe(
            dataframe=st.session_state.pharmacy_example_record_data, args=function_arguments_json)

    if function_name == "notify_pharmacist":
        response, notifications = notify_pharmacist(function_arguments=function_arguments_json)

    if function_name == "get_pharmacy_opening_hours":

        store_code = function_arguments_json.get("store_code")

        print("function_arguments_json:", function_arguments_json)

        print("!!!STORE CODE:", store_code)

        opening_hours = OPENING_HOURS_MOCK_PHARMACY_API_RESPONSE.get(store_code)

        day = getattr(function_arguments_json, "day", "")

        if day != "":
            day = f"day: {day}"

        if opening_hours is None:
            return f"couldn't find a store code \"{store_code}\" in the database", None

        INSTRUCTION_MESSAGE = {
            "role": "system",
            "content": SYSTEM_MESSAGE.format(
                ASSISTANT_IDENTITY=st.session_state.whoami) + f" current date and time: {get_current_datetime()}"

        }
        chat_history_footer = [
            {"role": "system",
             "content": f"### give the opening hours to the user given this data: {day, opening_hours}"}]

        messages = [INSTRUCTION_MESSAGE] + [
            {"role": m["role"], "content": m["content"]} for m in
            st.session_state.messages[-SLIDING_CHAT_WINDOW_SIZE:] + chat_history_footer]



        notifications = {"info": f"made a call to the API with arguments: \n \n 'store_code': '{store_code}' \n\n and got a response:\n\n {opening_hours}"}

        for chunk in get_response(messages):
            chunk = chunk.choices[0].delta

            content = getattr(chunk, "content", "")
            if content:
                response += content
            # full_response += chunk.choices[0].delta.get("content", "")
            message_placeholder.markdown(response + "▌")



    return response, notifications


def manipulate_dataframe(dataframe, args):
    """
    Updates a specified cell in a pandas DataFrame.

    Parameters:
    - dataframe: A pandas DataFrame to be modified.
    - args: A dictionary containing the 'response', 'row', 'column', and 'new_value' keys.

    Returns:
    - A tuple containing the updated DataFrame and the response message.
    """
    # Extract arguments
    response = args['response']
    row = args['row']
    column = args['column']
    new_value = args['new_value']



    if isinstance(new_value, str) and new_value.strip().lower() in ["none", "null", ""]:
        new_value = None

    # Check if the specified column exists in the DataFrame
    if column not in dataframe.columns:
        return dataframe, response,  {"error": "Column not found."}

    # Check if the specified row index is within the DataFrame's range
    if row >= len(dataframe) or row < 0:
        return dataframe, response, {"error": "Row index out of range."}

    # Update the DataFrame
    dataframe.at[row, column] = new_value

    print(dataframe)

    # Return the updated DataFrame and the response message
    return dataframe, response, {"success": f" succesfully changed field [{row},{column}] to {new_value}"} #df, response, notificaion




def detect_inside_response(current_string):
    # Regular expression to find the "response" key and its value up to the current point
    # This regex handles cases where the "response" string is partially received
    response_regex = r'"response":\s*"((?:[^"\\]|\\.)*)'

    # Search for the "response" pattern in the current string
    match = re.search(response_regex, current_string)

    if match:
        response_content = match.group(1)  # Extract the content of the "response" up to this point
    else:

        response_content = ""  # No content since we're not inside "response"

    return response_content


def get_current_datetime():
    # Capturing the current moment
    now = datetime.now()

    # Crafting the string representation
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_now

def ai_message(docs):
    notifications = None

    INSTRUCTION_MESSAGE = {
        "role": "system",
        "content": SYSTEM_MESSAGE.format(ASSISTANT_IDENTITY = st.session_state.whoami) + f" current date and time: {get_current_datetime()}"

    }
    if docs: # TODO: add a doc object with metadata to pass to the model
        relevant_docs_messages = [{"role": "assistant", "content": "content of document fragment:\n" + doc} for doc in docs]
    else:
        relevant_docs_messages = [{"role": "system", "content": "there are no available documents from the user"}]

    chat_history_header = [
        {"role": "system", "content": "### end of relevant documents. the next messages contain the chat history ###"}]

    with (st.chat_message("assistant", avatar=MAIN_ICON)):

        message_placeholder = st.empty()
        functioncall_placeholder = st.empty()

        full_response = ""
        messages = [INSTRUCTION_MESSAGE] + relevant_docs_messages + chat_history_header + [
            {"role": m["role"], "content": m["content"]} for m in
            st.session_state.messages[-SLIDING_CHAT_WINDOW_SIZE:]]

        function_name = None
        function_arguments = None

        # Flag to indicate if the function name has been captured
        function_name_captured = False
        detected_tool_call = False

        for chunk in get_response(messages, tools=TOOLS):
            chunk = chunk.choices[0].delta

            if chunk.tool_calls:
                detected_tool_call = True
                # If we haven't captured the function name yet, get it from the first tool call
                if not function_name_captured:
                    function_name = chunk.tool_calls[0].function.name
                    if function_name is not None:
                        function_arguments = ""
                        function_name_captured = True


                # Iterate through each tool call in the chunk
                for tool_call in chunk.tool_calls:
                    # If the tool call has arguments, append them to the function_arguments string
                    if tool_call.function.arguments:
                        function_arguments += tool_call.function.arguments

                message_placeholder.markdown(detect_inside_response(function_arguments)+ "▌")

                functioncall_placeholder.markdown(f"```python\n"
                                                  f"function_name: {function_name}, arguments: {function_arguments}\n"
                                                  f"```")



            else:
                content = getattr(chunk, "content", "")
                if content:
                    full_response += content
                #full_response += chunk.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")

        if detected_tool_call:
            try:
                function_arguments_json = json.loads(function_arguments)
            except json.JSONDecodeError:
                # If JSON parsing fails, keep the raw string
                function_arguments_json = function_arguments

        if detected_tool_call:
            functioncall_placeholder.markdown(f"```python\n"
                                              f"function_name: {function_name}, arguments: {function_arguments}\n"
                                              f"```")
            full_response, notifications = hanhandle_function_calls(function_name, function_arguments_json=function_arguments_json, message_placeholder=message_placeholder, functioncall_placeholder=functioncall_placeholder)

            #parsed_json = json.loads(function_arguments_json)


        message_placeholder.markdown(full_response)


    function_call_record = None

    if function_name is not None:
        function_call_record = f"```python\n"\
                               f"function_name: {function_name}, arguments: {function_arguments}\n"\
                               f"```"


    st.session_state.messages.append({"role": "assistant", "content": full_response,"function_call":function_call_record, "avatar": MAIN_ICON})
    return notifications



REPHRASE_QUESTION_INSTRUCTION_TEXT = """###INSTRUCTIONS: Construct a query from the last question in the provided chat history, suitable for a similarity search in a vector store, using keywords and context from the history.You can also add other keywords you think will help. Respond only with the query, without any additional prefixes or labels.###"""
