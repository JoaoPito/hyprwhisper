import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold, GenerationConfig
from PIL import Image

import os

GOOGLE_ENV_VAR = "GOOGLE_API_KEY"

class GoogleLLM():
    messages = []
    chat = None

    gen_config = GenerationConfig(temperature=0.75)

    safety_settings = {
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    }

    def __init__(self, model_name='gemini-1.5-flash',
                system='You are an exceptional AI assistant.',
                tools=None):
        genai.configure(api_key=os.getenv(GOOGLE_ENV_VAR))
        self.model = genai.GenerativeModel(model_name=model_name, 
                                            system_instruction=system,
                                            tools=tools)

    def invoke(self, text_prompt, images=[], use_history=True):
        contents = self.__create_prompt_contents__(text_prompt, images)
        if(use_history):
            if self.chat == None:
                self.chat = self.model.start_chat()
            response = self.chat.send_message(contents, 
                                                safety_settings=self.safety_settings,
                                                generation_config=self.gen_config)
        else:
            response = self.model.generate_content(contents, 
                                                safety_settings=self.safety_settings,
                                                generation_config=self.gen_config)
        return response
    
    def __create_prompt_contents__(self, text, images):
        contents = []
        for img_url in images:
            image = Image.open(img_url)
            contents.append(image)
        contents.append(text)
        return contents
    
    def clear_history(self):
        self.chat = None