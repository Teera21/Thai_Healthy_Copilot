from dotenv import find_dotenv, load_dotenv
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import SystemMessage
from tool.custom_tools import Save_Information_Tool
from prompt.read_prompt import Prompt_Text
from langchain.callbacks import get_openai_callback

# from googletrans import Translator

# translator = Translator()
# doc1 = translator.translate(xc['matches'][0]['metadata']['Description'][:1500], to_lang='en')
# doc2 = translator.translate(xc['matches'][1]['metadata']['Description'][:1500], to_lang='en')
# question = translator.translate(question, to_lang='en')

load_dotenv()
llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview")

system_prompt = Prompt_Text()
system_message = SystemMessage(
    content=f"""
    {system_prompt}
    """
)

tools = [
    Save_Information_Tool()
]

agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    "system_message": system_message,
}

memory = ConversationSummaryBufferMemory(
    memory_key="memory", return_messages=True, llm=llm, max_token_limit=100)

while True:
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        agent_kwargs=agent_kwargs,
        memory=memory,
    )

    user_input = input('user_input: ')
    if user_input == "Q":
        break
    with get_openai_callback() as cb:
        result = agent.invoke({"input": user_input})
        print(cb)
    # print(result['output'])