import os
from dotenv import load_dotenv, find_dotenv
import openai
from langchain.chains.summarize import load_summarize_chain
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

# set value of OpenAIAPI Key
load_dotenv(find_dotenv())
openai.api_key = os.environ.get('OPENAI_API_KEY')

#This is Function for check about information Email 
def check_consulting_email(lates_reply:str):
    prompt = f"""
    EMAIL: {lates_reply}
    ---

    Above is an email about Job offer / consulting; Your goal is identify if all information above is mentioned:
    1. What's the problem the prospect is trying to solve? 
    2. Their budget

    If all info above is collected, return YES, otherwise, return NO; (Return ONLY YES or NO)

    ANSWER: 
    """

    all_needs_collected_result = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    all_needs_collected = all_needs_collected_result["choices"][0]["message"]["content"]

    return all_needs_collected

def print_result():
    file_name = "example.txt"
    with open(file_name, "w") as file:
        # Write text to the file
        file.write("This is some text written to a file.\n")
        file.write("You can add more lines as needed.\n")

#this function use for decisoin what to do in next state
def categorise_email(lates_reply:str):
    categorise_prompt = f"""
    EMAIL: {lates_reply}
    ---
    Your goal is to categorise the email based on categories below:

    1. COLLABORATION/SPONSORSHIP: These are emails where companies or individuals are reaching out to propose a collaboration or sponsorship opportunity with AI Jason. They often include details about their product or service and how they envision the partnership.

    2. JOB_OFFER/CONSULTING: These emails involve individuals or companies reaching out to AI Jason with a specific job or project they want him to work on. This could range from developing an AI application to leading a specific activity.

    3. QUESTIONS: These emails involve individuals reaching out to AI Jason with specific questions or inquiries. This could be about his videos, his knowledge on a specific topic, or his thoughts on a specific AI tool or technology.

    4. NON_REPLY: These are auto emails that don't need any response or involve companies or individuals reaching out to AI Jason to offer their services. This could be a marketing agency offering to help him find sponsorship opportunities or a company offering a specific tool or service they think he might find useful.

    5. OTHER: These are emails that don't fit into any of the above categories.


    CATEGORY (Return ONLY the category name in capital):
    """

    category_result = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "user", "content": categorise_prompt}
        ]
    )

    category = category_result["choices"][0]["message"]["content"]
    print(f"####### {category} ######")
    if category == "JOB_OFFER/CONSULTING":
        all_needs_collected = check_consulting_email(lates_reply)
        if all_needs_collected == "YES":
            return {
                "Step 1": """print("XXX")"""
            }
        else:
            return {
                "Step 1": "print('YYY')"
            }
    else:
        if category == "COLLABORATION/SPONSORSHIP":
            return {
                "Step 1": "Research about the prospect & company",
                "Step 2": "Forward the email to jason.zhou.design@gmail.com, with the research results included"
            }
        else:
            if category == "NON_REPLY":
                return { "Step 1": "use"}       
            else:
                return {
                    "Step 1": "use function print_result ",
                }


    
class CategoriseEmailInput(BaseModel):
    lates_reply:str = Field(description='Latest reply from the prospect')

class CategoriseEmailTool(BaseTool):
    name = 'categorise_email'
    description = 'use this to categorise email to decide what to do next'
    args_schema: Type[BaseModel] = CategoriseEmailInput

    def _run(self, lates_reply:str):
        return categorise_email(lates_reply)
    
    def _arun(self, url:str):
        raise NotImplementedError('does not support async')
    
class PrintInput(BaseModel):
    lates_reply:str = Field(description='Latest reply from the prospect')

class PrintTool(BaseTool):
    name = 'print_result'
    description = 'use this to print or show message to user'
    args_schema: Type[BaseModel] = CategoriseEmailInput

    def _run(self, lates_reply:str):
        return print_result()
    
    def _arun(self, url:str):
        raise NotImplementedError('does not support async')