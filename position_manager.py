from datetime import datetime
from typing import List, Dict


class Position:
    def __init__(self, id: str, asset: str, amount: float, entry_price: float, current_price: float):
        self.id = id
        self.asset = asset
        self.amount = amount
        self.entry_price = entry_price
        self.current_price = current_price
        self.timestamp = datetime.now()

    def calculate_value(self) -> float:
        """Calculates the current value of the position based on the current price and amount."""
        return self.current_price * self.amount

    def update_current_price(self, price: float):
        """Updates the current price of the asset."""
        self.current_price = price
        self.timestamp = datetime.now()  # Update the timestamp whenever the price is updated


class PositionManager:
    def __init__(self):
        self.positions: Dict[str, List[Position]] = {}
        self.portfolio_value_cache: Dict[str, float] = {}

    def add_position(self, agent_id: str, position: Position):
        """Adds a new position to an agent's portfolio."""
        if agent_id not in self.positions:
            self.positions[agent_id] = []
        self.positions[agent_id].append(position)
        self.portfolio_value_cache.pop(agent_id, None)  # Invalidate the cache for this agent

    def get_positions(self, agent_id: str) -> List[Position]:
        """Retrieves all positions for a specific agent."""
        return self.positions.get(agent_id, [])

    def remove_position(self, agent_id: str, position_id: str):
        """Removes a position from the agent's portfolio using the position ID."""
        if agent_id in self.positions:
            self.positions[agent_id] = [pos for pos in self.positions[agent_id] if pos.id != position_id]
            self.portfolio_value_cache.pop(agent_id, None)  # Invalidate the cache for this agent

    def get_portfolio_value(self, agent_id: str) -> float:
        """Computes the total value of all positions held by the agent."""
        if agent_id in self.portfolio_value_cache:
            return self.portfolio_value_cache[agent_id]

        total_value = sum(pos.calculate_value() for pos in self.get_positions(agent_id))
        self.portfolio_value_cache[agent_id] = total_value  # Cache the computed value
        return total_value

    def update_position(self, agent_id: str, position_id: str, new_current_price: float):
        """Updates the current price of a position for an agent."""
        if agent_id in self.positions:
            for pos in self.positions[agent_id]:
                if pos.id == position_id:
                    pos.update_current_price(new_current_price)
                    self.portfolio_value_cache.pop(agent_id, None)  # Invalidate the cache for this agent
                    break