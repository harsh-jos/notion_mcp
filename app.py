import streamlit as st
import asyncio
import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp_use import MCPClient, MCPAgent
# Note: The import paths for mcp_use might vary slightly depending on the exact version, 
# but based on standard python packaging, this is the most likely structure.
# If mcp_use exposes them differently, we might need to adjust.

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found in .env")
    st.stop()



# Streamlit App Config
st.set_page_config(page_title="Notion MCP Chatbot", page_icon="Rb")
st.title("Notion MCP Chatbot")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Cache the Agent initialization to avoid recreating it on every rerun
@st.cache_resource
def get_agent():
    # Initialize MCP Client from config file
    client = MCPClient.from_config_file("mcp_config.json")
    
    # Initialize Gemini Model using LangChain wrapper
    # Using gemini-2.5-flash as requested
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GEMINI_API_KEY)
    
    # Initialize MCP Agent
    # We pass the client and the model. 
    agent = MCPAgent(
        llm=model,
        client=client,
    )
    
    return agent

# Async function to handle chat
async def chat_handler(prompt):
    agent = get_agent()
    
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Call the agent
            # Assuming agent.chat or agent.process is the method
            # and it returns a response or a stream
            response = await agent.run(prompt)
            
            # If response is a string
            if isinstance(response, str):
                full_response = response
                message_placeholder.markdown(full_response)
            else:
                # If it's an object with .content or similar
                full_response = str(response)
                message_placeholder.markdown(full_response)
                
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")

# Main UI Logic
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask something about your Notion workspace..."):
    asyncio.run(chat_handler(prompt))
