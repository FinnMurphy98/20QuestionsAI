from app import create_app
from config import TestConfig
from app.openai.chat import chatgpt_response
import unittest
import openai

class TestCharGPTResponse(unittest.TestCase):
    """
    Test case for the chatgpt_response function
    """
    def setUp(self):
        """
        Set test fixtures.
        """
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        openai.api_key = self.app.config.get('OPENAI_KEY')
    
    def tearDown(self):
        """
        Clear fixtures.
        """
        self.app_context.pop()

    def test_chatgpt_response(self):
        """
        GIVEN an array of messages
        WHEN calling the chatpgt_response
        THEN it should return a message that is not None
        """
        messages = [{'role': 'user', 'content': 'Hello there.'}]
        reply = chatgpt_response(messages)
        self.assertNotEqual(reply, None)

if __name__ == '__main__':
    unittest.main()