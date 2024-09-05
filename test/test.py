# tests/test_agent.py

import unittest
from neoagent.agent import NeoAgent


class TestNeoAgent(unittest.TestCase):
    def test_agent_initialization(self):
        agent = NeoAgent(apikey="dummy_key")
        self.assertIsNotNone(agent)

    def test_agent_run(self):
        agent = NeoAgent(apikey="dummy_key")
        result = agent.run(
            path=["dummy_path"],
            username="user",
            password="pass",
            url="dummy_url",
            data="dummy_data",
        )
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
