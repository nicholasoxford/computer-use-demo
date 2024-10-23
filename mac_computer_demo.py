import asyncio
import os
from datetime import datetime
from computer_use_demo.tools.mac_computer import MacComputerTool
from computer_use_demo.loop import sampling_loop, APIProvider, PROVIDER_TO_DEFAULT_MODEL_NAME
import streamlit as st
from functools import partial
from typing import Any, cast
from computer_use_demo.streamlit import (
    setup_state, 
    _render_message, 
    _tool_output_callback, 
    _api_response_callback,
    Sender,
    WARNING_TEXT,
    STREAMLIT_STYLE
)

async def main():
    setup_state()
    
    st.markdown(STREAMLIT_STYLE, unsafe_allow_html=True)
    st.title("MacBook Control Interface")
    
    if not os.getenv("HIDE_WARNING", False):
        st.warning(WARNING_TEXT)
    
    # Sidebar configuration
    with st.sidebar:
        st.text_input(
            "Anthropic API Key",
            value=st.session_state.api_key,
            type="password",
            key="api_key_input",
        )
        st.session_state.api_key = st.session_state.api_key_input
        
        st.number_input(
            "Only send N most recent images",
            min_value=0,
            key="only_n_most_recent_images"
        )
        
        st.text_area(
            "Custom System Prompt Suffix",
            key="custom_system_prompt"
        )
        
        st.checkbox("Hide screenshots", key="hide_images")
    
    # Initialize computer tool
    computer_tool = MacComputerTool()
    
    chat, http_logs = st.tabs(["Chat", "HTTP Exchange Logs"])
    
    with chat:
        # Chat interface
        for message in st.session_state.messages:
            if isinstance(message["content"], str):
                _render_message(message["role"], message["content"])
            elif isinstance(message["content"], list):
                for block in message["content"]:
                    if isinstance(block, dict) and block["type"] == "tool_result":
                        _render_message(
                            Sender.TOOL, st.session_state.tools[block["tool_use_id"]]
                        )
                    else:
                        _render_message(message["role"], block)

        # Get user input
        user_input = st.chat_input("Type a command for controlling your MacBook...")
        
        if user_input:
            st.session_state.messages.append({
                "role": Sender.USER,
                "content": user_input
            })
            
            _render_message(Sender.USER, user_input)
            
            # Run the agent loop
            with st.spinner("Running Agent..."):
                messages = await sampling_loop(
                    # Required parameters from function signature
                    model=PROVIDER_TO_DEFAULT_MODEL_NAME[APIProvider.ANTHROPIC],
                    provider=APIProvider.ANTHROPIC,
                    system_prompt_suffix=st.session_state.custom_system_prompt,
                    messages=st.session_state.messages,
                    output_callback=partial(_render_message, Sender.BOT),
                    tool_output_callback=partial(
                        _tool_output_callback,
                        tool_state=st.session_state.tools
                    ),
                    api_response_callback=partial(
                        _api_response_callback,
                        tab=http_logs,
                        response_state=st.session_state.responses,
                    ),
                    api_key=st.session_state.api_key,
                    only_n_most_recent_images=st.session_state.only_n_most_recent_images,
                    max_tokens=4096,
                )
                
                # Update messages
                st.session_state.messages = messages

if __name__ == "__main__":
    asyncio.run(main())