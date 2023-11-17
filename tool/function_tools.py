import openai
import json

def retreiver_memory(user_input:str):
    function_descriptions = [
    {
        "name": "extract_info_from_sentence",
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
                "health": {
                    "type": "string",
                    "description": "health information found in sentences"
                },
            },
        }
    }
    ]

    prompt = f"Please extract key information from this email: {user_input} "
    message = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=message,
        functions = function_descriptions,
        function_call="auto"
    )
    result = vars(response)
    
    if 'function_call' in result['_previous']['choices'][0]['message']:
        arguments = result['_previous']['choices'][0]['message']["function_call"]["arguments"]
        name = eval(arguments).get("name")
        weight = eval(arguments).get("weight")
        height = eval(arguments).get("height")
        happended = eval(arguments).get("happended")
        likes = eval(arguments).get("likes")
        birthday = eval(arguments).get("birthday")
        health = eval(arguments).get("health")

        result =  {
            "name": name,
            "weight":weight,
            "height":height,
            "happended":happended,
            "likes":likes,
            "birthday":birthday,
            "health":health
        }

        with open("information.json", "w") as outfile: 
            json.dump(result, outfile)

def core_memory_append(user_input:str):
    file_name = "Information.txt"
    with open(file_name, "w") as file:
        # Write text to the file
        file.write(f"{user_input}")
    retreiver_memory(user_input)





    
