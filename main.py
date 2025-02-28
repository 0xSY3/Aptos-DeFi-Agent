import os
import json
from crewai import Crew, Task
from agents.data_collector_agent import create_data_collector_agent
from agents.data_analysis_agent import create_data_analysis_agent, analyze_data
from tools.web_scraper_tool import WebScraperTool
import dotenv

dotenv.load_dotenv() 



if __name__ == "__main__":
    # 0. Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # 1. Initialize Agents
    data_collector_agent = create_data_collector_agent()
    data_analysis_agent = create_data_analysis_agent()

    # 2. Define Tasks
    website_url = "https://docs.ariesmarkets.xyz/" # Changed to documentation URL
    scrape_website_task = Task(
        description=f"""Scrape the content from the website: {website_url} of the Aptos DeFi protocol Aries Markets.
        Focus on extracting information about their services, features, and any available documentation links. Return the result as a JSON object. """,
        agent=data_collector_agent,
        expected_output="A JSON object containing detailed report on Aries Markets services, features, and documentation links."
    )

    analyze_data_task = Task(
        description="""Analyze the scraped data from the Aries Markets website to identify key services, features, and documentation resources.
        Provide a concise report summarizing your findings. """,
        agent=data_analysis_agent,
        expected_output="A concise report summarizing the key services, features, and documentation resources of Aries Markets based on the scraped data."
    )

    # 3. Create Crew
    defi_research_crew = Crew(
        agents=[data_collector_agent, data_analysis_agent],
        tasks=[scrape_website_task, analyze_data_task],
        verbose=True
    )

    # 4. Run Crew and Get Results
    print("Starting Crew...")
    research_report_output = defi_research_crew.kickoff() # Store CrewOutput object
    research_report_json_string = research_report_output.tasks_output[0].raw # Extract JSON from TaskOutput

    # **NEW: Clean up markdown wrapping if present**
    if research_report_json_string.startswith("```json") and research_report_json_string.endswith("```"):
        research_report_json_string = research_report_json_string[7:-3]
    elif research_report_json_string.startswith("```") and research_report_json_string.endswith("```"):
         research_report_json_string = research_report_json_string[3:-3]
    research_report_json_string = research_report_json_string.strip()

    print("\n\n------------------------ Raw Task Output (JSON, Cleaned) ------------------------\n\n")
    print(research_report_json_string)

    print("\n\n------------------------ Research Report (Agent's Summary - Scrape Output JSON) ------------------------\n\n")
    print(repr(research_report_output)) # Keep printing repr for debugging

    # 5. Save JSON data to file
    try:
        research_report_data = json.loads(research_report_json_string)
        filename = "aries_markets_data.json"
        filepath = os.path.join("data", filename)
        with open(filepath, 'w') as f:
            json.dump(research_report_data, f, indent=4)
        print(f"\nScraped data saved to: {filepath}")

        # **NEW: Analyze and Print Analysis Report**
        analysis_report = analyze_data(research_report_json_string)
        print("\n\n------------------------ Data Analysis Report ------------------------\n\n")
        print(analysis_report)
        print(f"\nAnalysis report printed above.")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON output: {e}")
        print(f"Raw output that caused the error (cleaned): {research_report_json_string}")
        print(f"Original raw output: {research_report_output.tasks_output[0].raw}")
    print("\n\n------------------------ End Report ------------------------\n\n")