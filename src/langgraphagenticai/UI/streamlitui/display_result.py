import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage 
import json

class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message
     
    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        
        if usecase == "Basic Chatbot":
            # Display user message once
            with st.chat_message('user'):
                st.write(user_message)
            
            # Create placeholder for assistant response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # Stream the response
                for event in graph.stream({'messages': ("user", user_message)}):
                    try:
                        # Handle different event formats
                        if isinstance(event, dict):
                            for value in event.values():
                                if isinstance(value, dict) and 'messages' in value:
                                    message = value['messages']
                                    # Check if message has content attribute
                                    if hasattr(message, 'content') and message.content:
                                        full_response += message.content
                                        message_placeholder.write(full_response)
                    except Exception as e:
                        st.error(f"Error processing event: {e}")
                        
        elif usecase == "Chatbot With Web":
            try:
                # Prepare state and invoke the graph
                initial_state = {"messages": [user_message]}
                res = graph.invoke(initial_state)
                
                # Display all messages in order
                for message in res.get('messages', []):
                    if isinstance(message, HumanMessage):
                        with st.chat_message("user"):
                            st.write(message.content)
                    elif isinstance(message, ToolMessage):
                        with st.chat_message("ai"):
                            st.write("🔧 Tool Call Start")
                            st.code(message.content)  # Use code block for tool output
                            st.write("🔧 Tool Call End")
                    elif isinstance(message, AIMessage) and message.content:
                        with st.chat_message("assistant"):
                            st.write(message.content)
            except Exception as e:
                st.error(f"Error processing chat with web: {e}")
        else:
            st.error(f"Unknown usecase: {usecase}")