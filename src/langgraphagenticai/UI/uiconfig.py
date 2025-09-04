from configparser import ConfigParser

class Config:
    def __init__(self, config_file="C:/htdocs/AgenticAIWorkspace/Agentic Chatbot/src/langgraphagenticai/UI/uiconfigfile.ini"):
        self.config = ConfigParser()
        loaded_files = self.config.read(config_file)

        if not loaded_files:
            print(f"⚠️ Could not load config file: {config_file}")

    def get_llm_options(self):
        llm_option = self.config["DEFAULT"].get("LLM_OPTION", "")
        print("DEBUG: LLM_OPTION =", llm_option)  # 👈 Add debug
        return llm_option.split(", ") if llm_option else []

    def get_usecase_options(self):
        usecase_option = self.config["DEFAULT"].get("USECASE_OPTION", "")
        return usecase_option.split(", ") if usecase_option else []

    def get_groq_model_options(self):
        groq_model_option = self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS", "")
        return groq_model_option.split(", ") if groq_model_option else []

    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE", "Agentic AI App")
