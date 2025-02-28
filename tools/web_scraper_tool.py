from crewai.tools import BaseTool
from bs4 import BeautifulSoup
import requests
import json  # Import the json library

class WebScraperTool(BaseTool):
    name: str = "WebScraperTool"
    description: str = "Scrapes content from a given URL and returns structured data."

    def _run(self, url: str) -> str: #  Return type is still string for CrewAI tool output, but we'll return JSON string
        """Scrape content from a given URL and returns structured data in JSON format."""
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = soup.get_text(separator='\n', strip=True)
            data = { # Create a dictionary to hold structured data
                "url": url,
                "content": text_content[:5000] + "..." if len(text_content) > 5000 else text_content
            }
            return json.dumps(data) # Return the dictionary as a JSON string
        except requests.exceptions.RequestException as e:
            error_data = {"url": url, "error": str(e)} # Structure error info
            return json.dumps(error_data) # Return error as JSON string