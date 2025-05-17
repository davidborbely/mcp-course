import asyncio
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# For Google Gemini, use:
# from langchain_google_genai import ChatGoogleGenerativeAI
# model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

ROOT_FOLDER = Path(__file__).parent.parent.absolute()
MCP_PATH = str(ROOT_FOLDER / "binance_mcp_reference_implementation" / "binance_mcp.py")

mcp_config = {
    "binance": {
        "command": "python",
        "args": [MCP_PATH],
        "transport": "stdio",
    }
}


async def get_crypto_prices():
    async with MultiServerMCPClient(mcp_config) as client:
        tools = client.get_tools()

        agent = create_react_agent(model, tools)

        query = "What are the current prices of Bitcoin and Ethereum?"
        message = HumanMessage(content=query)

        response = await agent.ainvoke({"messages": [message]})

        answer = response["messages"][-1].content

        return answer


if __name__ == "__main__":
    # Run the main async function
    response = asyncio.run(get_crypto_prices())
    print(response)
