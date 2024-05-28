from crewai import Task
from textwrap import dedent
from models import CustomerQuery
from jira import JIRA
from dotenv import load_dotenv
import json
import os
import requests

load_dotenv()

jira_server = os.getenv('JIRA_SERVER')
jira_email = os.getenv('JIRA_EMAIL')
jira_api_token = os.getenv('JIRA_API_TOKEN')
project_key = os.getenv('PROJECT_KEY')

jira = JIRA(server=jira_server, basic_auth=(jira_email, jira_api_token))

class CustomTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def resolve_inquiry(self, agent, customer, inquiry):
        def callback_function_to_print(output):
            print(f"""
                Here is the email draft: {output.raw_output}
            """)
        return Task(
            description=dedent(
                f"""
                {customer} just reached out with a super important ask:
                {inquiry}

                Make sure to use everything you know to provide the best support possible.
                You must strive to provide a complete and accurate response to the customer's inquiry.
                """
            ),
            expected_output=dedent(
                """
                A detailed, informative response to the customer's inquiry that addresses all aspects of their question.
                The response should include references to everything you used to find the answer, including external data or solutions.
                Ensure the answer is complete, leaving no questions unanswered, and maintain a helpful and friendly tone throughout.
                """
            ),
            agent=agent,
            callback=callback_function_to_print
        )

    def quality_assurance_review(self, agent, customer):
        return Task(
            description=dedent(
                f"""
                Review the response drafted by the Senior Support Representative for {customer}'s inquiry.
                Ensure that the answer is comprehensive, accurate, and adheres to the high-quality standards expected for customer support.
                Verify that all parts of the customer's inquiry have been addressed thoroughly, with a helpful and friendly tone.
                Check for references and sources used to find the information, ensuring the response is well-supported and leaves no questions unanswered.
                """
            ),
            expected_output=dedent(
                """
                A final, detailed, and informative response ready to be sent to the customer.
                This response should fully address the customer's inquiry, incorporating all relevant feedback and improvements.
                Don't be too formal, we are a chill and cool company but maintain a professional and friendly tone throughout.
                """
            ),
            agent=agent,
        )


    def classify_query(self, agent, customer_query):
        def callback_function(output):
            customer_query = output.exported_output  # Get the Pydantic output
            with open('customer_query_classifications.json', 'a') as f:
                json.dump(customer_query.dict(), f)
                f.write('\n')
            issue_type_name = None
            if customer_query.category == 'feature request':
                issue_type_name = 'Epic'
                with open('customer_feedback/feature_requests.txt', 'a') as fr:
                    fr.write(f"{customer_query.summary} - {customer_query.priority}\n")
            elif customer_query.category == 'bug report':
                issue_type_name = 'Task'
                with open('customer_feedback/bugs.txt', 'a') as br:
                    br.write(f"{customer_query.summary} - {customer_query.priority}\n")
            else:
                issue_type_name = 'Subtask'

            # Create Jira issue based on the category
            if issue_type_name:
                jira_issue = jira.create_issue(
                    fields={
                        'project': {'key': project_key},
                        'summary': customer_query.summary,
                        'description': customer_query.description,
                        'issuetype': {'name': issue_type_name},
                    }
                )
        return Task(
            description=dedent(
                f"""
                Classify the following customer query into either a feature request or a bug report. Extract relevant details and 
                determine the urgency for the roadmap. Set the original_message field to be the exact same as {customer_query}, and the details
                as to what your interpretation of the message was, as a feature request or bug report. If it's neither, just have the details
                be the feature the customer was enquiring about.
                You will only classify a request as a feature request if it's NOT present in our product, as you can find in the current
                product info or the customer feedback that we maintain. You will only classify a request as a bug report if
                it is already present in our product, and the customer reports a complaint when using the feature.
                If neither is the case, just have the category be no action
                Customer Query:
                {customer_query}
                """
            ),
            expected_output="All the details of a specifically chosen"
                            "feature request or bug report extracted from the customer query.",
            output_pydantic=CustomerQuery,
            agent=agent,
            callback=callback_function,
        )
