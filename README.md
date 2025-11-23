# Notion MCP Chatbot

A simple Streamlit application that interacts with Notion using the Model Context Protocol (MCP) and Google's Gemini AI.

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables:**
    Ensure you have a `.env` file with your API keys:
    ```
    GEMINI_API_KEY=your_gemini_api_key
    ```

3.  **MCP Configuration:**
    Ensure `mcp_config.json` is present and configured for your Notion MCP server.

## Running the App

Run the Streamlit app directly:

```bash
streamlit run app.py
```
