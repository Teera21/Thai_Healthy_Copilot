import os

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import ChatOpenAI
from langchain.agents import tool
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain.prompts import MessagesPlaceholder
from langchain.schema.messages import AIMessage, HumanMessage

chat_history = []
os.environ["OPENAI_API_KEY"] = "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"
OPENAI_API_KEY = "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"

llm = ChatOpenAI(model="gpt-4", temperature=0)

@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)


tools = [get_word_length]


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant, but bad at calculating lengths of words.",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

MEMORY_KEY = "chat_history"
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant, but bad at calculating lengths of words.",
        ),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)


agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

while True:

  input = input("User Input:")
  result = agent_executor.invoke({"input": input, "chat_history": chat_history})
  chat_history.extend(
      [
          HumanMessage(content=input),
          AIMessage(content=result["output"]),
      ]
  )
  output = agent_executor.invoke({"input": "is that a real word?", "chat_history": chat_history})
  if input=="Q":
        break
  else:
    final_result = output.return_values["output"]
    print(final_result)