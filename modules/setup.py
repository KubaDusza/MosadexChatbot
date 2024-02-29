import stat

import openai
import pandas as pd

from constants import *
from imports import *


def setup():
    st.set_page_config(
        page_title=NAME_OF_THE_SITE,
        page_icon=MAIN_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "About": "mailto: jacob.dusza@gmail.com linkedin:https://www.linkedin.com/in/jakub-dusza-041a9023b/",
            # "Get help": "https://www.youtube.com/",
            # "Report a bug": "https://www.youtube.com/"
        }
    )

    if 'display_clear_button' not in st.session_state:
        st.session_state.display_clear_button = False

    if 'pharmacy_example_record_data' not in st.session_state:
        st.session_state.pharmacy_example_record_data = pd.DataFrame(PHARMACY_EXAMPLE_RECORD_DATA)
        print("ADDED!!!")

    if 'pharmacy_example_text_info' not in st.session_state:
        st.session_state.pharmacy_example_text_info = PHARMACY_EXAMPLE_TEXT_INFO

    if 'whoami' not in st.session_state:
        st.session_state.whoami = WHOAMI


    if "openai_client" not in st.session_state:
        st.session_state.openai_client = openai.OpenAI()

    if "my_avatar" not in st.session_state:
        st.session_state.my_avatar = "🤠"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "openai_model" not in st.session_state:
        st.session_state.openai_model = GPT_MODEL

    if "first_question_asked" not in st.session_state:
        st.session_state.first_question_asked = False

    if "prompt" not in st.session_state:
        st.session_state.prompt = FIRST_MESSAGE

    if "prompts" not in st.session_state:
        st.session_state.prompts = []

    if "regenerate" not in st.session_state:
        st.session_state.regenerate = False

    if "access_key" not in st.session_state:
        st.session_state.access_key = ""


def grant_access():
    allowed_emails = st.secrets.get("ALLOWED_EMAILS")
    allowed_access_keys = st.secrets.get("ALLOWED_ACCESS_KEYS")

    query_dict = st.experimental_get_query_params()

    query_access_key = query_dict.get("access_key", None)

    if query_access_key:
        st.session_state.access_key = query_access_key[0]

    if (st.experimental_user.email in allowed_emails) or (
            st.session_state.access_key in allowed_access_keys) or REMOVE_RESTRICTIONS:
        return True
    else:
        if st.experimental_user.email is None:
            st.write("streamlit removed ability to see logged in account (?), so use an access key instead.")
            #st.write(
            #    "You are not logged in. You can log in or create streamlit accout here:\n https://share.streamlit.io/")
        else:
            st.write(f"sorry, email {st.experimental_user.email}has no access. Log in to an allowed account")

        st.write("Paste an access key:")

        st.session_state.access_key = st.text_input(label="access key", label_visibility="collapsed", type="password",
                                                    placeholder="access key")

        if st.session_state.access_key in allowed_access_keys:
            st.rerun()
