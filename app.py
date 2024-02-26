import streamlit

from imports import *
from modules.setup import setup, grant_access
from modules.page import sticky_header, display_chat_buttons
from modules.chat import display_chat, ask_question
from constants import *

import pandas as pd


def display_notifications(notifications):
    """
    Displays notifications in Streamlit with corresponding icons.

    Parameters:
    - notifications: A dictionary with keys 'error', 'info', 'warning', and 'success',
                     where each key maps to a string message to be displayed.
    """
    if notifications is None:
        return

    if 'info' in notifications:
        st.info(notifications['info'], icon="ℹ️")

    if 'success' in notifications:
        st.success(notifications['success'], icon="✅")

    if 'warning' in notifications:
        st.warning(notifications['warning'], icon="⚠️")

    if 'error' in notifications:
        st.error(notifications['error'], icon="🚨")


def main():
    col1, col2 = st.columns([1, 1])
    notifications = None



    with st.sidebar:

        st.markdown("""
        # Pharmacy Assistant Chatbot Capabilities
        
This demo was made to showcase the possibilities of use of the chatbot.
key features:

- **Serialized Record Data Interactions**: Retrieve or modify record data
- **Text, Unorganized Data Interactions**: retrieve information from unprocessed, already avaliable data, like pharmacy webpage
- **Pharmacist Notifications**: notify pharmacists with updates
- **Warning Notification System**: Sends alerts in response to critical messages for immediate attention
        """)

        with st.expander("System Prompt"):
            system_prompt = st.text_area(label="write a system message, that tells the model how to act",
                                         value=WHOAMI,
                                         height=350)
            st.session_state.whoami = system_prompt

        with st.expander("Things to try"):
            st.write("1. add behaviour to the chatbot by inserting some requirement to the system message, like:\n"
                     "  - act like a duck, by adding *quack!* to your sentences\n\n"
                     "2. Try asking for the data in the patients records or from the text information about the pharmacy\n\n"
                     "3. Ask it to add new or change existing record data, like changing the age, scheduling an appointment, taking a note, or saying, that you are allergicn\n\n"
                     "4. Ask it to notify the pharmacist about something\n\n"
                     "5. Send a worrying message on the chat, like:\n\n "
                     "'i think i overdosed' to test the warning notification system")



    with col1:
        display_chat()





    notifications = ask_question(col1)

    with col1:
        display_chat_buttons()

    with col2:
        display_notifications(notifications)

        st.header("Example Record Data")
        edited_record_data = st.data_editor(data=st.session_state.pharmacy_example_record_data,
                                num_rows="dynamic",
                                column_config={
                                    "Allergic to XYZ": st.column_config.CheckboxColumn(
                                        label="Allergic to XYZ",
                                        help="Select your **favorite** widgets",
                                        default=False,
                                    ),


                                }
                                )

        st.session_state.pharmacy_example_record_data = edited_record_data


        st.header("Example Text Data")
        editable_text_data = st.text_area("",
                                          height=500,
                                          value=PHARMACY_EXAMPLE_TEXT_INFO)

        st.session_state.pharmacy_example_text_info = editable_text_data


        #notifications

        #if notifications is not None:


    # with st.sidebar:
    # display_pdfs()


if __name__ == '__main__':
    load_dotenv()
    setup()

    sticky_header()

    # st.write(st.session_state.access_key in allowed_access_keys)
    # st.write("allowed access keys:", allowed_access_keys)
    # st.write("access key:", st.session_state.access_key)

    if grant_access():
        main()
