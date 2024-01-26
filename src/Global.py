import os
import openai
from enum import Enum
import google.generativeai as genai
#### My Microsoft’s  Azure OpenAI Service
# openai.api_type = "azure"
# openai.api_base = "https://bzgpt35.openai.azure.com/"
# openai.api_version = "2023-07-01-preview"
src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(src_dir)
keydir = os.path.join(project_dir,'Keys')
keyfile = os.path.join(keydir, "oai_key.txt")
key = open(keyfile).readline().strip("\n")
openai.api_key = key

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
gemini_keyfile = os.path.join(keydir, "gemini_key.txt")
gemini_key = open(gemini_keyfile).readline().strip("\n")
GOOGLE_API_KEY= gemini_key
genai.configure(api_key=GOOGLE_API_KEY)
Gemini_model = genai.GenerativeModel('gemini-pro')
#K-similiary
# similar_neighbour_num = 10



class STATUS(Enum):
    SUCCESS = 1
    NULL = 0
    ERROR = -1
    GPT_ERROR = -2
    def __json__(self):
        return {
            'name': self.name,
            'value': self.value
        }
    
status = STATUS.NULL
global_prompt_file = ""
global_natual_language = ""

def set_global_prompt_file(file):
    global global_prompt_file
    global_prompt_file = file

def get_global_prompt_file():
    global global_prompt_file
    return global_prompt_file



def set_global_natual_language(nl):
    global global_natual_language
    global_natual_language = nl

def get_global_natual_language():
    global global_natual_language
    return global_natual_language
