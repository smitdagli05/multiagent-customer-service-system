from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool, DirectorySearchTool, TXTSearchTool
from models import CustomerQuery

class CustomAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo")
        self.current_product_info_search_tool = DirectorySearchTool(directory='current_product_info')
        self.customer_feedback_search_tool = DirectorySearchTool(directory='customer_feedback')
        self.serper_tool = SerperDevTool()


    def support_agent(self):
        return Agent(
            role="Senior Support Representative",
            backstory=dedent("""
                You work at Mattermost, an open-source, self-hosted messaging platform that brings all your team communication 
                into one place, making it searchable and accessible anywhere. It’s designed to improve collaboration and 
                productivity within organizations of all sizes, and are now working on providing
                support to {customer}, a super important customer for your company.
                You need to make sure that you provide the best support! The way you do this is by carefully looking at current
                product info and making sure you draw your answer from in there. Or, if the customer has a question/request that
                is already present in feature requests or the bugs list inside of customer feedback, make sure you let 
                them know that we're already working on it, and their request is on the roadmap already.
                Make sure to provide full complete answers, and make no assumptions.
            """),
            goal=dedent("""
                Be the most friendly and helpful support representative in your team.
            """),
            tools=[self.current_product_info_search_tool, self.customer_feedback_search_tool, self.serper_tool],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    def support_quality_assurance_agent(self):
        return Agent(
            role="Support Quality Assurance Specialist",
            backstory=dedent("""
                You work at Mattermost and are now working with your team
                on a request from {customer}, ensuring that the support representative is
                providing the best support possible. You need to make sure that the support representative
                is providing full, complete answers, and make no assumptions. If there is relevant information about
                the customer query in our current product info or customer feedback, the support representative's 
                answer should adhere to it.
            """),
            goal=dedent("""
                Get recognition for providing the best support quality assurance in your team.
            """),
            tools=[self.current_product_info_search_tool, self.customer_feedback_search_tool, self.serper_tool],
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    def query_classifier_agent(self):
        return Agent(
            role="Product Owner",
            backstory=dedent("""
                You're the Product Owner at Mattermost, an open-source, self-hosted messaging platform that brings all your team communication 
                into one place, making it searchable and accessible anywhere. It’s designed to improve collaboration and 
                productivity within organizations of all sizes. Your job is to read incoming customer queries and classify them 
                into either feature requests or bug reports, extracting the relevant details and determining their urgency. ou will only classify a request as a feature request if it's NOT present in our product, as you can find in the current
                product info or the customer feedback that we maintain. You will only classify a request as a bug report if
                it is already present in our product, and the customer reports a complaint when using the feature.
                If it's already present in our product and the customer is simply asking something about
                the feature, I want the you to have the category for the customer query object be Current Feature Query, 
                not a Feature Request or Bug Report. 
                Customer Query:
            """),
            goal=dedent("""
                Accurately classify customer queries and extract detailed information to aid the development team and best enhance your product.
            """),
            tools=[self.current_product_info_search_tool, self.customer_feedback_search_tool],
            verbose=True,
            llm=self.OpenAIGPT35,
        )
