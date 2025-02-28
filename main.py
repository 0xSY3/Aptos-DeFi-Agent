import os
from crewai import Crew, Task, Process
from dotenv import load_dotenv

from agents.infrastructure_agents import create_infrastructure_architect_agent, create_python_developer_agent, create_software_qa_agent
from agents.portfolio_agent import create_portfolio_reporting_agent

load_dotenv()

def main():
    # 1. Agents
    architect_agent = create_infrastructure_architect_agent()
    developer_agent = create_python_developer_agent()
    qa_agent = create_software_qa_agent()
    reporting_agent = create_portfolio_reporting_agent() # Now this is a CrewAI Agent

    # 2. Tasks
    design_task = Task(
        description="Design the architecture for the position_manager.py module. ...",
        agent=architect_agent,
        expected_output="Architectural blueprint for position_manager.py"
    )

    develop_task = Task(
        description="Based on the architecture blueprint ..., write the Python code ...",
        agent=developer_agent,
        expected_output="Python code for position_manager.py module"
    )

    qa_task = Task(
        description="Create a comprehensive test plan for the position_manager.py module. ...",
        agent=qa_agent,
        expected_output="Test plan and unit tests for position_manager.py"
    )

    # Portfolio Reporting Task
    portfolio_report_task = Task(
        description="Generate a portfolio report using the PortfolioReportingAgent.",
        agent=reporting_agent, # Assign the CrewAI Agent here
        expected_output="Portfolio report in text format"
    )

    # 3. Crew
    infrastructure_crew = Crew(
        agents=[architect_agent, developer_agent, qa_agent],
        tasks=[design_task, develop_task, qa_task],
        process=Process.sequential  # Tasks will be executed in order
    )

    # Portfolio Reporting Crew (Single agent for now)
    portfolio_report_crew = Crew(
        agents=[reporting_agent], # Use the PortfolioReportingAgent
        tasks=[portfolio_report_task],
        process=Process.sequential
    )

    # 4. Run crew and get tasks outputs
    infrastructure_crew_result = infrastructure_crew.kickoff()
    print("\n\nInfrastructure Crew Task Output:")
    print(infrastructure_crew_result)

    # Run Portfolio Reporting Crew and get report
    portfolio_report_crew_result = portfolio_report_crew.kickoff() # Run the portfolio reporting crew
    print("\n\nPortfolio Report:")
    print(portfolio_report_crew_result) # Print the crew's result, which should be the report

if __name__ == "__main__":
    main()