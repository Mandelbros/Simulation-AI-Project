from src.agents.Agent import Agent

class Rule():
    def __init__(self, weight, description=''):
        self.weight = weight
        self.description = description

    def evaluate(self, agent: Agent, time, verbose):
        pass

    def __str__(self) -> str:
        return f"Weight: {self.weight}, Description: {self.description})"
    