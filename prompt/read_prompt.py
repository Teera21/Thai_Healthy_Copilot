from prompt.read_json import read_name

def Prompt_Text():
    txt = ''
    with open('./prompt/prompt.txt') as f:
        contents = f.read()
        txt += contents
    name = read_name()
    txt += f"  this is name of user : '{name}' "
    return txt 
