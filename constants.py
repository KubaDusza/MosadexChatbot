
REMOVE_RESTRICTIONS = False


# General info
NAME_OF_THE_SITE = "Pharmacy Assistant Chatbot Demo"
MAIN_ICON = "💊"




# the number of messages the chatbot will remember
SLIDING_CHAT_WINDOW_SIZE = 5

#PT_MODEL = "gpt-3.5-turbo"
GPT_MODEL = "gpt-4"


WHOAMI='''Chatbot Assistant Configuration:
  - Role: Pharmacy Assistant
  - Objective: Provide accurate record information, and address customer queries regarding pharmacy services.
  - Your tools allow you to change the record data and notify the pharmacist. You SHOULD also notify the pharmacist, if the person is at risk and tell the person to seek proffesional medical help.
  - Behavior: Polite, informative, and patient.
  - Limitations: Do not provide medical advice beyond the scope of pharmacy services. Refer to a pharmacist for complex inquiries.
  '''


# Chat
SYSTEM_MESSAGE = '''### INSTRUCTIONS:\n
1. This is your identity: {ASSISTANT_IDENTITY}\n
.Use markdown.\n
3. If a user asks about a document, answer based on it. If not, use general knowledge but mention if it's not in the documents.\n
4. Never make stuff up.\n

*Remember to use Markdown for formatting, so when listing stuff and so on. you can also use emojis!* 🦆🐤
END OF INSTRUCTIONS ###\n
Next messages will contain relevant documents.'''

FIRST_MESSAGE = '''What is this document about?'''


#=========
# Example data
#=========

PHARMACY_EXAMPLE_RECORD_DATA = {
        "Name": ["John Doe", "Jane Smith", "Alex Johnson"],
        "Age": [45, 30, 38],
        "Scheduled Appt. Date": ["2024-03-15", None, "2024-04-22"],
        "Note": ["Follow-up required", None, None],  # Adding notes with only one entry filled
        "Allergic to XYZ": [True, False, False]
    }


PHARMACY_EXAMPLE_TEXT_INFO = """    Mock Pharmacy Information
    =========================

    Name: Central City Pharmacy

    Address: 123 Wellness Street

    Phone: +1-800-555-PILL

    Email: contact@centralcitypharmacy.com

    Website: www.centralcitypharmacy.com

    Opening Hours:
    - Monday to Friday: 8:00 AM - 8:00 PM
    - Saturday: 9:00 AM - 6:00 PM
    - Sunday: Closed

    Services Offered:
    - Prescription services
    - Immunizations
    - Health screenings

    Emergency Contact:
    - For after-hours emergencies, please call our 24-hour helpline at +1-800-555-HELP.

    Thank you for choosing Central City Pharmacy for your health and wellness needs!"""
