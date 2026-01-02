import streamlit as st
import pandas as pd
import altair as alt
import matplotlib as plt
from src.agents.master_agent import agent_creation
from src.llm_instance import LLM_INSTANCES
from src.db_utils.load_metadata import load_metadata
from src.tools.graph_generation import generate_graph


# 1. Page Configuration
st.set_page_config(page_title="Pharma SQL Agent", page_icon="💊")
st.title("💊 Pharma Database Assistant")


# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []


# --- 2. Helper Functions ---


@st.cache_resource
def initialize_agent():
    try:
        model = LLM_INSTANCES["GPT_4_1"]["MODEL"]
        db_path = 'pharma.db'
        with open("./src/prompts/agent_system_prompt.txt", "r") as f:
            system_prompt = f.read()
        metadata = load_metadata('./data/metadata.yaml')
        return agent_creation(model=model, db_path=db_path, system_prompt=system_prompt, metadata=metadata)
    except Exception as e:
        st.error(f"Error initializing agent: {e}")
        return None


def create_chart_for_message(msg_index):
    """
    Callback function to generate chart code for a specific message index.
    """
    message = st.session_state.messages[msg_index]
   
    # 1. Generate the code using your tool
    # We retrieve the data specifically saved for THIS message
    try:
        chart_code_response = generate_graph(
            final_result=message["content"],
            intermediate_steps=message["intermediate_steps"]
        )
       
        # 2. Clean the code string
        start_tag = "python"
        end_tag = "```"
        if start_tag in chart_code_response:
            start_index = chart_code_response.find(start_tag) + len(start_tag)
            end_index = chart_code_response.rfind(end_tag)
            chart_code_response = chart_code_response[start_index:end_index].strip()
           
        # 3. SAVE the code into the message history
        st.session_state.messages[msg_index]["chart_code"] = chart_code_response
       
    except Exception as e:
        st.session_state.messages[msg_index]["chart_error"] = str(e)


agent = initialize_agent()


# --- 3. Main Chat Loop (Display History & Charts) ---


# We use enumerate so we have the index 'i' for our unique button keys
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
       
        # Only check for charts if it is an assistant message
        if message["role"] == "assistant":
           
            # CASE A: Chart code already exists in history -> Execute it
            if "chart_code" in message:
                try:
                    # Retrieve the specific dataframe for this message
                    df = message["raw_data"]
                   
                    # Create a container for the chart
                    with st.container():
                        # Execute the stored code
                        exec(message["chart_code"], {"st": st, "pd": pd, "alt": alt, "df": df})
                except Exception as e:
                    st.error(f"Could not render stored chart: {e}")
           
            # CASE B: No chart yet, but we have data -> Show Button
            elif "raw_data" in message and not message.get("chart_error"):
                # The callback 'create_chart_for_message' will run before the page reloads
                st.button(
                    "📊 Generate Chart",
                    key=f"chart_btn_{i}",
                    on_click=create_chart_for_message,
                    args=(i,) # Pass the index of this message to the function
                )
           
            # CASE C: Error happened previously
            if message.get("chart_error"):
                st.error(f"Chart generation failed: {message['chart_error']}")


# --- 4. Handle New User Input ---


if user_input := st.chat_input("Ask a question about the database..."):
   
    # Add User Message to History
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)


    # Process Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if agent:
                    # Run Agent
                    response = agent.invoke({"messages": st.session_state.messages})
                    final_ai_message = response['messages'][-1].content
                   
                    st.markdown(final_ai_message)


                    # --- CRITICAL STEP: SAVE CONTEXT TO HISTORY ---
                    # We create a dictionary for the message that holds ALL necessary context
                    # to generate a chart later (Data, Steps, Content).
                   
                    # NOTE: Ensure you are retrieving the 'last_raw_data' from wherever
                    # your custom agent stores it during execution.
                    current_raw_data = st.session_state.get("last_raw_data", pd.DataFrame())


                    assistant_msg_data = {
                        "role": "assistant",
                        "content": final_ai_message,
                        "intermediate_steps": response['messages'][-1],
                        "raw_data": current_raw_data  # Store the dataframe HERE
                    }
                   
                    st.session_state.messages.append(assistant_msg_data)
                   
                    # Rerun to show the "Generate Chart" button for this new message
                    st.rerun()
                else:
                    st.error("Agent failed to load.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
# Sidebar Reset
with st.sidebar:
    if st.button("Reset Conversation"):
        st.session_state.messages = []
        st.session_state.last_final_result = None
        st.session_state.last_intermediate_steps = None
        st.session_state.last_raw_data = pd.DataFrame()
        st.session_state.show_chart = False
        st.session_state.generated_chart_code = None
        st.rerun()