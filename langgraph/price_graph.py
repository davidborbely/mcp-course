import asyncio
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent


load_dotenv('/Users/davidborbely/Desktop/mcp-course/.env', override=True)

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)


ROOT_FOLDER = Path(__file__).parent.parent.absolute()
MCP_PATH = str(
    ROOT_FOLDER / "binance_mcp" / "binance_mcp.py"
)

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

        query = HumanMessage(content="What are the current prices of Bitcoin and Ethereum?")

        # Send the message to the model and get the response
        response = await agent.ainvoke({"messages": [query]})

        # Return the response content
        answer = response["messages"][-1].content
        return answer


if __name__ == "__main__":
    # Run the main async function
    response = asyncio.run(get_crypto_prices())
    print(response)
