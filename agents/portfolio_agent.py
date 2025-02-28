from crewai import Agent
from pydantic import Field, ConfigDict
from position_manager import PositionManager, Position

class PortfolioReportingAgent(Agent): # Inherit from crewai.Agent
    """
    Agent responsible for generating reports about DeFi portfolios,
    utilizing the PositionManager to fetch and summarize portfolio data.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True) # Allow arbitrary types

    position_manager: PositionManager = Field(default_factory=PositionManager) # Define position_manager as a Field

    def __init__(self, **kwargs): # Accept kwargs to pass to Agent.__init__
        """
        Initializes the Portfolio Reporting Agent with a PositionManager and CrewAI Agent configurations.
        """
        super().__init__(**kwargs) # Initialize CrewAI Agent - position_manager is initialized as a Field

    def generate_portfolio_report(self):
        """
        Generates a portfolio report by:
        1. Adding simulated positions to the PositionManager.
        2. Retrieving positions from the PositionManager.
        3. Calculating the portfolio value (placeholder for now).
        4. Formatting the data into a human-readable report.

        Returns:
            str: A text-based report summarizing the DeFi portfolio.
        """
        self._add_simulated_positions()
        positions = self.position_manager.get_positions(agent_id=self.name) # Use agent's name as agent_id
        portfolio_value = self.position_manager.get_portfolio_value(agent_id=self.name) # Placeholder value

        report = f"## DeFi Portfolio Report\n\n"
        report += f"**Total Portfolio Value (Placeholder):** ${portfolio_value:.2f}\n\n"
        report += "**Positions:**\n"

        if not positions:
            report += "No positions held in the portfolio.\n"
        else:
            for position in positions:
                report += f"- **Position ID:** {position.id}\n"
                report += f"  - **Asset:** {position.asset}\n"
                report += f"  - **Amount:** {position.amount}\n"
                report += f"  - **Entry Price:** ${position.entry_price:.2f}\n"
                report += f"  - **Current Price:** ${position.current_price:.2f}\n"
                report += f"  - **Value:** ${position.calculate_value():.2f}\n\n"

        return report

    def _add_simulated_positions(self):
        """
        Adds a few simulated DeFi positions to the PositionManager for demonstration.
        """
        position1 = Position(
            id="apt-aries-1", asset="APT", amount=100, entry_price=8.50, current_price=9.20
        )
        position2 = Position(
            id="apt-usdc-lp-pancake-1", asset="APT-USDC LP", amount=50, entry_price=1.00, current_price=1.05
        )
        self.position_manager.add_position(agent_id=self.name, position=position1) # Use agent's name as agent_id
        self.position_manager.add_position(agent_id=self.name, position=position2)


def create_portfolio_reporting_agent():
    """
    Creates and returns an instance of the Portfolio Reporting Agent, now as a CrewAI Agent.
    """
    portfolio_reporting_agent = PortfolioReportingAgent(
        role='Portfolio Reporting Agent',
        goal='To create clear and concise reports summarizing DeFi portfolio holdings and their value.',
        backstory="Expert in summarizing financial data, particularly for DeFi portfolios. Skilled at presenting complex information in an easy-to-understand way."
    )
    return portfolio_reporting_agent

if __name__ == '__main__':
    # Example usage to demonstrate the PortfolioReportingAgent
    reporting_agent = create_portfolio_reporting_agent()
    report = reporting_agent.generate_portfolio_report()
    print(report)