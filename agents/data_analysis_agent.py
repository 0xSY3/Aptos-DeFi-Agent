from crewai import Agent
import json

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
    about the DeFi protocol.

    Args:
        json_data_string: JSON string containing scraped data.

    Returns:
        A formatted string report summarizing the analysis, or an error message.
    """
    try:
        data = json.loads(json_data_string)

        if "error" in data:
            return f"Error in scraped data: {data['error']}"

        content = data.get("content", "") # Get content, default to empty string if missing

        if not content:
            return "No content scraped from the website to analyze."

        # **Basic Analysis - You can expand this to be much more sophisticated**
        # For now, let's just look for keywords related to services and features
        services_keywords = ["lending", "borrowing", "swap", "trading", "margin", "amm", "dex", "order book"]
        features_keywords = ["user-friendly", "account management", "composability", "flexibility", "security", "performance", "flash loans"]
        docs_keywords = ["documentation", "docs", "api", "developers"]

        found_services = [keyword for keyword in services_keywords if keyword.lower() in content.lower()]
        found_features = [keyword for keyword in features_keywords if keyword.lower() in content.lower()]
        found_docs = [keyword for keyword in docs_keywords if keyword.lower() in content.lower()]

        report = "## DeFi Protocol Analysis Report:\n\n"
        report += "### Key Services Identified:\n"
        if found_services:
            report += "- " + "\n- ".join(found_services) + "\n"
        else:
            report += "No specific services keywords identified in the scraped content.\n"

        report += "\n### Key Features Identified:\n"
        if found_features:
            report += "- " + "\n- ".join(found_features) + "\n"
        else:
            report += "No specific feature keywords identified in the scraped content.\n"

        report += "\n### Documentation/Developer Resources:\n"
        if found_docs:
            report += "Keywords related to documentation or developer resources were found in the content.\n" # In a real agent, you would extract actual links
        else:
            report += "No explicit documentation/developer resource keywords found.\n"

        report += "\n**Please note:** This is a basic keyword-based analysis. More advanced techniques could be used for deeper insights.\n"

        return report

    except json.JSONDecodeError as e:
        return f"Error decoding JSON data for analysis: {e}"
    except Exception as e:
        return f"An error occurred during data analysis: {e}"