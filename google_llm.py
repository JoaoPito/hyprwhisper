import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold, GenerationConfig
from PIL import Image

import os

GOOGLE_ENV_VAR = "GOOGLE_API_KEY"
SUPPORTED_IMG_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}

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
        self.tools = self.__build_tool_dict__(tools)

    def invoke(self, text_prompt, images=[]):
        contents = self.__create_prompt_contents__(text_prompt, images)
        response = self.__invoke_with_history__(contents)
        
        try:
            return response.text
        except AttributeError:
            tools_results = self.__use_tools__(response)
            response_parts = self.__build_tool_responses__(tools_results)
            response_parts = response_parts + self.__build_tools_attachment_responses__(tools_results)
            response = self.__invoke_with_history__(response_parts)
        return response.text
    
    def clear_chat(self):
        self.chat = None
    
    def __invoke_with_history__(self, contents):
        if self.chat == None:
                self.chat = self.model.start_chat()
        return self.chat.send_message(contents, 
                                    safety_settings=self.safety_settings,
                                    generation_config=self.gen_config)
        
    def __invoke_without_history__(self, contents):
        return self.model.generate_content(contents, 
                                            safety_settings=self.safety_settings,
                                            generation_config=self.gen_config)
    
    def __create_prompt_contents__(self, text, images):
        contents = []
        for img_url in images:
            if(self.__validate_img_extension__(img_url)):
                image = Image.open(img_url)
                contents.append(image)
        contents.append(text)
        return contents
    
    def __validate_img_extension__(self, file):
        _, ext = os.path.splitext(file)
        return ext.lower() in SUPPORTED_IMG_EXTENSIONS
        
    def __build_tool_dict__(self, tools):
        return {tool.__name__: tool for tool in tools}
    
    def __has_called_tools__(self, response):
        return "function_call" in response.parts
    
    def __use_tools__(self, response):
        tool_results = {}
        for part in response.parts:
            if fn := part.function_call:
                args = {key: val for key, val in fn.args.items()}
                result = self.tools[fn.name](**args) # Call tool
                print(f"{fn.name}: {result}")
                tool_results[fn.name] = result # Tools always should return with format (result, attachments)
        return tool_results
    
    def __build_tool_responses__(self, results):
        return [
            genai.protos.Part(function_response=genai.protos.FunctionResponse(name=fn, response={"result": val}))
            for fn, (val, _) in results.items()
        ]
        
    def __build_tools_attachment_responses__(self, results):
        return [Image.open(att) for _, (_, att_list) in results.items() 
                            for att in att_list 
                            if self.__validate_img_extension__(att)]