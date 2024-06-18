## Overview

This system is an end-to-end workflow that takes as input a customer support request, and generates an appropriate response to the inquiry, mimicking a senior support agent for the company/product. Additionally, it convert customer inquiries into product insights by automatically creating JIRA tickets for feature requests and bug reports based on the inquiry.

## Usecase

Teams maintaining popular open-source projects are often under-resourced and perenially pressed for time. As a result, they lack the bandwith to satisfactorily address customer questions, and tend to miss product insights that arise from such questions/feedback. A production grade version of this tool would be helpful in such cases

## Key Components

### Custom Agents

This system is built around three specialized agents, each tailored to fulfill a specific role within the support process:

1. **Support Agent**: This agent acts as the frontline responder to all incoming customer queries. It performs RAG on a detailed directory of current product information and customer feedback, in addition to internet searches to provide precise and informed responses. It can also perform RAG on a Github Repo, Code docs or PDF's if your knowledge base lives on these. For the purposes of this project, I created a mock knowledge base to simulate a response to a customer support request.

2. **Support Quality Assurance Agent**: After the initial response by the Support Agent, this agent reviews the draft to ensure that the final response to the customer is accurate, friendly and professional, enhancing the customer's experience. It verifies accuracy by making sure there's no hallucinations, by performing another RAG on the knowledge base. Additionally, if you have templates on how to respond to customer requests, you could also have this agent perform a RAG on the template to make sure the response adheres to your preferences.

3. **Query Classifier Agent**: This agent classifies incoming queries into categories such as feature requests, bug reports, or general inquiries, and automatically creates a JIRA ticket with a summary, description and issue type. You could additionally augment this to automatically assign it to a particular person on your team, based on the issue type/other parameters. It adds these requests to the knowledge base, for the other two agents to refer to. This agent ensures that customer requests are converted into actionable insights for your engineering and product teams, ensuring your product roadmap reflects customer needs.

### Custom Tasks

Each agent is assigned specific tasks that define their responsibilities:

- **Resolve Inquiry**: Managed by the Support Agent to draft a comprehensive and accurate initial response based on the customer's inquiry.
- **Quality Assurance Review**: Conducted by the Support Quality Assurance Agent to refine the response, ensuring it meets all required standards before reaching the customer.
- **Classify Query**: Handled by the Query Classifier Agent, this task involves analyzing and categorizing the customer's query to streamline the support process and facilitate easier management of feedback and requests.

### Integration Tools

To support these agents and tasks, the system employs several integration tools:

- **DirectorySearchTool**: Enables agents to quickly search through directories containing current product information and customer feedback, ensuring that all responses are backed by up-to-date data.
- **SerperDevTool**: Enables agents to search the internet

## Configuration

Set up your environment variables by creating a `.env` file in your project directory and adding the following lines:

```plaintext
OPENAI_API_KEY='your-openai-api-key'
OPENAI_ORGANIZATION_ID='your-openai-organization-id'
SERPER_API_KEY='your-serper-api-key'
JIRA_SERVER='your-jira-server'
JIRA_EMAIL='your-jira-email'
JIRA_API_TOKEN='your-jira-api-token'
PROJECT_KEY='your-jira-project-key'
```

Run the system by executing the main script:

```
python3 main.py

```

Follow the interactive prompts to enter the customer name and their inquiry. The system will process the inquiry and provide a detailed output.

