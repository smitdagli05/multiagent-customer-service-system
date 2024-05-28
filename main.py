import os
from crewai import Crew, Process
from decouple import config
from agents import CustomAgents
from tasks import CustomTasks
from textwrap import dedent

os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")
os.environ["OPENAI_ORGANIZATION_ID"] = config("OPENAI_ORGANIZATION_ID")
os.environ["SERPER_API_KEY"] = config("SERPER_API_KEY")

class CustomCrew:
    def __init__(self, customer, inquiry):
        self.customer = customer
        self.inquiry = inquiry

    def run(self):
        agents = CustomAgents()
        tasks = CustomTasks()

        support_agent = agents.support_agent()
        support_quality_assurance_agent = agents.support_quality_assurance_agent()
        query_classifier_agent = agents.query_classifier_agent()

        resolve_inquiry_task = tasks.resolve_inquiry(support_agent, self.customer, self.inquiry)
        quality_assurance_review_task = tasks.quality_assurance_review(support_quality_assurance_agent, self.customer)
        query_classification_task = tasks.classify_query(query_classifier_agent, self.inquiry)
        #agents=[support_agent, support_quality_assurance_agent, query_classifier_agent]
        #tasks=[resolve_inquiry_task, quality_assurance_review_task, query_classification_task]
        crew = Crew(
            agents=[support_agent, support_quality_assurance_agent, query_classifier_agent],
            tasks=[resolve_inquiry_task, quality_assurance_review_task, query_classification_task],
            verbose=True,
            process=Process.sequential,
            memory=True
        )

        result = crew.kickoff(inputs={})
        return result

if __name__ == "__main__":
    print("## Welcome to MatterMost Customer Support")
    print("-------------------------------")
    customer = input(dedent("""Enter customer name: """))
    inquiry = input(dedent("""Enter the customer inquiry: """))

    custom_crew = CustomCrew(customer, inquiry)
    result = custom_crew.run()
    print("\n\n########################")
    print(f"""
    Task completed!
""")
    print("########################\n")
    print(result)

