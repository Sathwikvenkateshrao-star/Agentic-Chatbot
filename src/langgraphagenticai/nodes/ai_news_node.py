from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate


class AINewsNode:
    def __init__(self,llm):
        """  initialize the AINEws with API keys for tavily and groq  """


        self.tavily = TavilyClient()
        self.llm = llm
        # this is used to capture various steps in this file so that later can be use for steps shown 
        self.state = {}

    def fetch_news(self,state:dict)->dict:

        """  Fetch Ai news based on the specific frquesncy  
        
            Args:
                state (dict):the state dictionary containing 'frequency'

            Returns:
                dict: Update state with 'news_data' key containing fetched news.
        
        """
    # this is tavily client 

        frequency = state['messages'][0].content.lower()
        self.state['frequency'] = frequency
        time_range_map = {'daily':'d','weekly':'w','monthly':'m','year':'y'}
        days_map = {'daily':1,'weekly':7,'month':30,'year':366}


        responce = self.tavily.search(
            query= "Top Artificial Intelligence (AI) technology news India and globally",
            topic= "news"   ,
            time_range= time_range_map[frequency],
            include_answer="advanced",
            max_results=15,
            days=days_map[frequency],
            # include_domains = ["techcrunch.com","venturebeat.com/ai,...."] ## uncomment and add if needded
        )


        state['news_data'] = responce.get('results',[])
        self.state['news_data']= state['news_data']
        return state
    

    def summarize_news(self,state : dict)-> dict:
        """" Summarize the fetched news using an LLM  
        Args:
            state (dict):the state dictionary containing 'news_data'

        Returns:
            dict: Updated state with 'summary' key containing summarized news.
        
        
        """

        news_items = self.state['news_data']

        prompt_template = ChatPromptTemplate.from_messages([
            (
                "system", """  Summarize AI news article into markdown format . For each item include :
                Date in format in 1ST timezone
                - concise sentences summary from latest news
                - Sort news by date wise (latest first)
                - source URL as link
                Use format :
                ### [Date]
                -[Summary](URL),
              """
            ),("user","Articles:\n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Content:{item.get('content','')}\nURL:{item.get('url','')}\nDate:{item.get('published_date','')}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format(articles = articles_str))
        state['summary'] = response.content
        self.state['summary'] = state['summary']
        return self.state
    
    def save_result(self,state):
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./AINews/{frequency}_summary.md"
        with open(filename,'w')as f:
            f.write(f"#{frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        self.state['filename'] = filename
        return self.state
