from crewai import Agent
import json
import re # Import the regular expression library

def create_data_analysis_agent():
    return Agent(
        role='DeFi Research Analyst',
        goal='Analyze scraped data to provide insightful reports on DeFi protocols',
        backstory="""You are a highly skilled DeFi Research Analyst with a knack for extracting key insights from complex data.
        You meticulously analyze information to identify trends, features, and potential opportunities within the Decentralized Finance space.
        Your reports are highly valued for their clarity and actionable intelligence.""",
        verbose=True,
        allow_delegation=False
        # No tools needed initially for analysis itself
    )

def analyze_data(json_data_string: str) -> str:
    """
    Analyzes the JSON data string (from web scraping) and extracts key information
    about the DeFi protocol, focusing on services and features, 
    now extracting directly from the JSON structure.

    Args:
        json_data_string: JSON string containing scraped data.

    Returns:
        A formatted string report summarizing the analysis, or an error message.
    """
    try:
        data = json.loads(json_data_string)

        if "error" in data:
            return f"Error in scraped data: {data['error']}"

        aries_markets_data = data.get("AriesMarkets", {}) # Get "AriesMarkets" data

        report = "## DeFi Protocol Analysis Report:\n\n"

        # **Extract Services from "CoreFeatures"**
        core_features = aries_markets_data.get("CoreFeatures", {})
        extracted_services = list(core_features.keys()) # Services are keys in "CoreFeatures"

        report += "### Key Services Identified:\n"
        if extracted_services:
            report += "- " + "\n- ".join(extracted_services) + "\n"
        else:
            report += "No specific services identified in the scraped content.\n"

        # **Extract User Experience Features from "UserExperience"**
        user_experience_features = aries_markets_data.get("UserExperience", {})
        extracted_features_ux = list(user_experience_features.keys()) # UX features are keys in "UserExperience"


        report += "\n### User Experience Features Identified:\n" # Changed heading
        if extracted_features_ux:
            report += "- " + "\n- ".join(extracted_features_ux) + "\n"
        else:
            report += "No specific user experience features identified.\n"


        # **Documentation Keyword Check (keeping this for now, but less relevant)**
        docs_keywords = ["documentation", "docs", "api", "developers", "guide", "tutorial"] # Added "guide", "tutorial"
        overview_content = aries_markets_data.get("Overview", "") # Get "Overview" content for keyword check
        found_docs = [keyword for keyword in docs_keywords if keyword.lower() in overview_content.lower()]

        report += "\n### Documentation/Developer Resources:\n"
        if found_docs:
            report += "Keywords related to documentation or developer resources were found in the overview content.\n" # Adjusted message
        else:
            report += "No explicit documentation/developer resource keywords found in the overview.\n" # Adjusted message

        report += "\n**Please note:** This analysis extracts services and user experience features directly from the structured JSON output.  Documentation keyword check is still based on the 'Overview' section.\n" # Updated note

        return report

    except json.JSONDecodeError as e:
        return f"Error decoding JSON data for analysis: {e}"
    except Exception as e:
        return f"An error occurred during data analysis: {e}"