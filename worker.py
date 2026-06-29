# To call watsonx's LLM, we need to import the library of IBM Watson Machine Learning
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.foundation_models import Model

# Define the model parameters
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import DecodingMethods

import requests

# placeholder for Watsonx_API and Project_id incase you need to use the code outside this environment
# API_KEY = "Your WatsonX API"
PROJECT_ID= "skills-network"

# Define the credentials 
CREDENTIALS = {
    "url": "https://us-south.ml.cloud.ibm.com"
	#"apikey": API_KEY
}

PARAMETERS = {
    GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
    GenParams.MIN_NEW_TOKENS: 1,
    GenParams.MAX_NEW_TOKENS: 1024
}

# Specify MODEL_ID that will be used for inferencing
MODEL_ID = "mistralai/mistral-medium-2505"

model = Model(
    model_id = MODEL_ID,
    params = PARAMETERS,
    credentials = CREDENTIALS,
    project_id = PROJECT_ID
)

def speech_to_text(audio_binary):
    # Set up Watson Speech-to-Text HTTP Api url
    base_url = "https://sn-watson-stt.labs.skills.network"
    api_url = base_url + "/speech-to-text/api/v1/recognize"

    # Set up parameters for our HTTP reqeust
    params = {
        'model' : 'en-US_Multimedia',
    }

    # Set up the body of our HTTP request
    audio_data = audio_binary

    # Send a HTTP Post request (.json())
    response = requests.post(api_url, params = params, data = audio_data).json()

    # Parse the response to get our transcribed text
    text = 'null'
    while bool(response.get('results')):
        print('STT response: ', response)
        text = response.get('results').pop().get('alternatives').pop().get('transcript')
        print('recognized text: ', text )
        return text

def text_to_speech(text, voice=""):
    return None

def watsonx_process_message(user_message):
    # Set the prompt for Watsonx API - using a strict translation instruction
    prompt = f"""
    Translate the following English sentence into Spanish.
    Reply ONLY with the translation, no explanations, no formatting, no extra text.
     
    English: {user_message}
    Spanish:
    """
    response_text = model.generate_text(prompt = prompt)
    return response_text.strip()
