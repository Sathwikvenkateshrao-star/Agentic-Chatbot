import streamlit as st 
import os 

from src.langgraphagenticai.UI.uiconfig import Config 

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_control = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title=self.config.get_page_title(),layout="wide")
        st.header(self.config.get_page_title())
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False


        with st.sidebar:
            # get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()


            # llm sekection
            self.user_control["select_llm"] = st.selectbox("Select LLM",llm_options)

            if self.user_control["select_llm"] =='Groq':

                # Model selection
                model_options = self.config.get_groq_model_options()
                self.user_control["selected_groq_model"] = st.selectbox("Select Model",model_options)
                self.user_control["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"]=st.text_input("API Key",type="password")
                # validate api key
                if not self.user_control["GROQ_API_KEY"]:
                    st.warning(" Please enter your GROQ API key to proceed. Don't have? reffer : https://console.groq.com/keys")

            # use case selections 
            self.user_control["selected_usecase"] = st.selectbox("Select usecases",usecase_options)
            
            if self.user_control["selected_usecase"] == "Chatbot With Web" or self.user_control["selected_usecase"] == "AI News":
                os.environ["TAVILY_API_KEY"]=self.user_control["TAVILY_API_KEY"]=st.session_state["TAVLY_API_KEY"]=st.text_input("TAVILY API KEY",type="password")

                # validate
                if not self.user_control["TAVILY_API_KEY"]:
                    st.warning("Please enter your TAVILY_API_KEY key to proceed.Don't have ? reffer : https://app.tavily.com/home")
            
            if self.user_control["selected_usecase"] == "AI News":
                st.subheader("AI News Explorer")

                with st.sidebar:
                    time_frame = st.selectbox(
                        "Select Time Frame",["Daily","Weekly","Mothly"],
                        index=0
                    )
                if st.button ("Fetch latest Ai News" , use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame

        return self.user_control