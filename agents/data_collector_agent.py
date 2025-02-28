from crewai import Agent
from tools.web_scraper_tool import WebScraperTool

def create_data_collector_agent():
    return Agent(
        role='Data Collector',
        goal='Collect data from web sources to provide insights for DeFi research',
        backstory="""You are an expert data collector, skilled in web scraping and information extraction.
        You meticulously gather data from various online sources to support the DeFi research team.
        Your attention to detail ensures the accuracy and relevance of the data collected.""",
        verbose=True,
        tools=[WebScraperTool()],
        allow_delegation=False
    )