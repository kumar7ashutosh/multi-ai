from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent


def get_response_from_ai_agents(llm_id, query, system_prompt, allow_search=False):
    llm = ChatOpenAI(model=llm_id)

    tools = []
    if allow_search:
        tools = [TavilySearch(max_results=2)]

    agent = create_react_agent(
        model=llm,
        tools=tools
    )

    messages = []

    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))

    # 🔥 supports both dict + pydantic Message
    for m in query:
        if isinstance(m, dict):
            if m["role"] == "user":
                messages.append(HumanMessage(content=m["content"]))
            elif m["role"] == "assistant":
                messages.append(AIMessage(content=m["content"]))
        else:
            if m.role == "user":
                messages.append(HumanMessage(content=m.content))
            elif m.role == "assistant":
                messages.append(AIMessage(content=m.content))

    response = agent.invoke({"messages": messages})

    final_messages = response.get("messages", [])

    for m in reversed(final_messages):
        if isinstance(m, AIMessage):
            return m.content

    return "No response generated"