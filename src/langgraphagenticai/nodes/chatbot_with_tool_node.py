from src.langgraphagenticai.state.state import State

class ChatbotWithToolNode:
    """ Basic Chatbot login implementation """
    def __init__(self,model):
        self.llm = model
    def proccess(self,state:State)->dict:
        """  Processess the input state and generates a response with tool integration  """

        user_input = state['messages'][-1] if state['messages']else ""
        llm_response = self.llm.invoke([{"role":"user","content":user_input}])

        # simulte tool-specific logic 

        tools_response = f"Tool integration for: '{user_input}' "
        return {"messages":[llm_response,tools_response]}
    
    def create_chatbot(self,tools):
        """  Return a chatbot node function """

        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state:State):
            """ Chatbot logic for processing the input state and running a response  """ 
            return{"messages":[llm_with_tools.invoke(state["messages"])]}
    
        return chatbot_node