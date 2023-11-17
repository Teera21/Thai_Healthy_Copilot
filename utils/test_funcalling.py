import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
import json
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

function_descriptions = [
    {
        "name": "extract_info_from_email",
        "description": "categorise & extract key info from in sentence",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "names of people found in sentences"
                },                                        
                "weight": {
                    "type": "string",
                    "description": "weight of people found in sentences"
                },
                "height":{
                    "type": "string",
                    "description": "height of people found in sentences"
                },
                "happened": {
                    "type": "string",
                    "description": "what happend of people found in sentneces"
                },
                "ikes":{
                    "type": "string",
                    "description": "Things you like to eat found in sentences"
                },
                "birthday": {
                    "type": "string",
                    "description": "Date of birth found in sentences"
                },
                "health information": {
                    "type": "string",
                    "description": "health information found in sentences"
                },
            },
        }
    }
    ]


email = """
Dear Jason 
I hope this message finds you well.
he hight 166 and weight 56
"""

prompt = f"Please extract key information from this email: {email} "
message = [{"role": "user", "content": prompt}]

response = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=message,
    functions = function_descriptions,
    function_call="auto"
)

result = {}
result = vars(response)
# print(result)

result =  {
    "companyName": "sgf",
    "product": "asgf",

}
print(result)
with open("sample.json", "w") as outfile: 
    json.dump(result, outfile)


# print(response['choices'][0]['message']['function_call']['arguments'])

# class Email(BaseModel):
#     from_email: str
#     content: str

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.post("/")
# def analyse_email(email: Email):
#     content = email.content
#     query = f"Please extract key information from this email: {content} "

#     messages = [{"role": "user", "content": query}]

#     response = openai.ChatCompletion.create(
#         model="gpt-4-0613",
#         messages=messages,
#         functions = function_descriptions,
#         function_call="auto"
#     )

